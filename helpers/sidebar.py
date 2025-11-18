import streamlit as st

def show() -> None:
    with st.sidebar:
        st.markdown(f"""
            <a href="/" style="color:yellow;text-decoration: none;">
                <div style="display:flex;align-items:center;margin-top:1rem;">
                    <img src="/app/static/logo.png" width="30"><span> Ducky</span>
                    <span style="font-size: 0.8em; color: grey">&nbsp;&nbsp;v0.1.0</span>
                </div>
            </a>
            <br>
                """, unsafe_allow_html=True)

        reload_button = st.button("↪︎  Reload Page")
        if reload_button:
            st.session_state.clear()
            st.rerun()