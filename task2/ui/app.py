from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st

from config.settings import (
    API_BASE_URL
)

st.set_page_config(
    page_title="Chat Engine",
    page_icon="💬",
    layout="wide"
)

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title(
    "Chat Engine"
)

st.caption(
    "RAG-powered document chat"
)

with st.sidebar:

    st.header(
        "Document Upload"
    )

    st.info(
        f"Backend: {API_BASE_URL}"
    )

    st.write(
        "Upload functionality coming next."
    )

st.write(
    "Chat functionality coming next."
)