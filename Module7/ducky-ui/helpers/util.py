import io
import os
import pandas as pd
import numpy as np
from typing import List, Dict
from sklearn.neighbors import NearestNeighbors
import tiktoken as tkn
from openai import OpenAI
from PyPDF2 import PdfFileReader
from streamlit.delta_generator import DeltaGenerator
import services.llm
import services.prompts as prompts


async def run_conversation(messages: List[Dict[str, str]], message_placeholder: DeltaGenerator) \
        -> List[Dict[str, str]]:
    # Remove any messages with the role "evidence"
    messages = [m for m in messages if m["role"] != "evidence"]
    full_response = ""
    message_placeholder.markdown("Thinking...")
    chunks = services.llm.converse(messages)
    
    try:
        chunk = await anext(chunks, "END OF CHAT")
        while chunk != "END OF CHAT":
            # print(f"Received chunk from LLM service: {chunk}")
            if chunk.startswith("EXCEPTION"):
                full_response = ":red[We are having trouble generating advice.  Please wait a minute and try again.]"
                break
            full_response = full_response + chunk
            message_placeholder.markdown(full_response + "▌")
            chunk = await anext(chunks, "END OF CHAT")
        message_placeholder.markdown(full_response)
        messages.append({"role": "assistant", "content": full_response})
    except Exception as e:
        message_placeholder.markdown(f"Error occurred: {e}")
    return messages


# Run prompt to generate initial messages and pass through run_conversation
async def run_prompt(prompt: str,
                     message_placeholder: DeltaGenerator) \
        -> List[Dict[str, str]]:
    messages = services.llm.create_conversation_starter(prompt)
    messages = await run_conversation(messages, message_placeholder)
    return messages

# Convert DataFrame to CSV-like string
def copy_as_csv_string(data_frame: pd.DataFrame) -> str:
    csv_string_io = io.StringIO()
    data_frame.to_csv(csv_string_io, index=False, sep=',')
    return csv_string_io.getvalue()


# Extract text from each page of the PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfFileReader(file)
        pages_text = [reader.getPage(i).extractText() for i in range(reader.getNumPages())]
    return pages_text


# Chunk prompt into pieces of approximately `chunk_size` tokens with overlap
def chunk_prompt(prompt: str, chunk_size: int = 1500, overlap: int = 50) -> List[str]:
    """
    Splits a prompt into chunks of approximately `chunk_size` tokens, with a given overlap.

    Parameters:
    - prompt (str): The text to be chunked.
    - chunk_size (int): The desired number of tokens for each chunk.
    - overlap (int): The number of tokens for overlap between chunks.

    Returns:
    - List[str]: A list of prompt chunks.
    """

    encoding = tkn.encoding_for_model("gpt-3.5-turbo")
    tokens = list(encoding.encode(prompt))

    if len(tokens) <= chunk_size:
        return [prompt]

    chunks = []
    position = 0

    while position < len(tokens):
        start_pos = max(0, position - overlap)
        end_pos = min(position + chunk_size, len(tokens))

        chunk_tokens = tokens[start_pos:end_pos]
        chunk_text = ''.join(encoding.decode_bytes(chunk_tokens).decode('utf-8', errors='ignore'))
        chunks.append(chunk_text)
        position += chunk_size

    return chunks


# Generate embeddings for a list of documents
def generate_embeddings(documents: List[str]):
    client = OpenAI(
    # This is the default and can be omitted
    base_url = 'http://aitools.cs.vt.edu:7860/openai/v1',
    api_key="aitools"
    )
    
    # calculate embeddings
    EMBEDDING_MODEL = "text-embedding-3-small"  # OpenAI's best embeddings as of Feb 2024
    BATCH_SIZE = 20  # you can submit up to 2048 embedding inputs per request

    embeddings = []
    for batch_start in range(0, len(documents), BATCH_SIZE):
        batch_end = batch_start + BATCH_SIZE
        batch = documents[batch_start:batch_end]
        print(f"Batch {batch_start} to {batch_end - 1}")
        response = client.embeddings.create(
            model=EMBEDDING_MODEL, input=batch, encoding_format="float")
        
        for i, be in enumerate(response.data):
            assert i == be.index  # double check embeddings are in same order as input
        batch_embeddings = [e.embedding for e in response.data]

        embeddings.extend(batch_embeddings)

    return embeddings


# Load or generate embeddings for The Pragmatic Programmer book
def get_or_generate_embeddings():
    embeddings_file = "data/ThePragmaticProgrammer.embeddings.csv"
    if os.path.exists(embeddings_file):
        print("Embeddings loaded from file.")
        return pd.read_csv(embeddings_file)

    # Extract text from the book page by page
    book_path = "data/ThePragmaticProgrammer.pdf"
    pages_content = extract_text_from_pdf(book_path)

    # Chunk each page and track the corresponding page number
    documents = []
    page_numbers = []

    for page_number, page_content in enumerate(pages_content, start=1):
        chunks = chunk_prompt(page_content, chunk_size=500, overlap=50)
        documents.extend(chunks)
        page_numbers.extend([page_number] * len(chunks))  # Associate each chunk with the page number

    # Generate embeddings for all chunks
    df_embeddings = generate_embeddings(documents)

    print("Embeddings generated.")

    # Save embeddings to CSV
    output_path = "data/ThePragmaticProgrammer.embeddings.csv"
    data = []
    for i, (doc, embedding, page_number) in enumerate(zip(documents, df_embeddings, page_numbers)):
        data.append({
            "document_name": "data/ThePragmaticProgrammer.pdf",
            "page_number": page_number,
            "embedding": ','.join(map(str, embedding)),
            "context": doc
        })
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)

    return df


# Function to handle semantic search and evidence retrieval
async def semantic_search(messages: List[Dict[str, str]], query: str, threshold: float = 0.8) -> Dict[str, str]:
    embeddings_data = get_or_generate_embeddings()
    
    # Generate embedding for the user's query
    query_embedding = generate_embeddings([query])
    query_embedding = np.array(query_embedding).reshape(1, -1)

    embeddings = embeddings_data["embedding"].apply(lambda x: list(map(float, x.strip('[]').split(',')))).tolist()
    nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(embeddings)
    
    # Perform nearest-neighbor search
    distances, indices = nbrs.kneighbors(query_embedding)

    relevant_document = embeddings_data.iloc[indices[0][0]]
    page_number = relevant_document["page_number"]
    context = relevant_document["context"]

    # Return the relevant document's context along with the page number
    print(f"Semantic Search Returns: Page {page_number}")
    return {"context": context, "page_number": page_number}

    nearest_distance = distances[0][0]

    # Check if the nearest neighbor is below the defined threshold
    if nearest_distance < threshold:
        relevant_document = embeddings_data.iloc[indices[0][0]]
        page_number = relevant_document["page_number"]
        context = relevant_document["context"]
        print(f"Semantic Search Returns: Page {page_number}")
        return {"context": context, "page_number": page_number}
    else:
        print("No relevant neighbors found.")
        return None