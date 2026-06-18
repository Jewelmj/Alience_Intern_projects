from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
import requests

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

    uploaded_files = st.file_uploader(
        "Upload Documents",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    upload_button = st.button(
        "Upload Files"
    )

    if upload_button:
        if not uploaded_files:
            st.warning("Please select at least one file.")
        else:
            try:
                files = [
                    (
                        "files",
                        (
                            file.name,
                            file,
                            file.type
                        )
                    )
                    for file in uploaded_files
                ]

                response = requests.post(
                    f"{API_BASE_URL}/upload",
                    files=files
                )

                data = response.json()

                if data["status"] == "success":
                    st.session_state.session_id = (
                        data["session_id"]
                    )

                    st.success(
                        "Upload completed successfully."
                    )

                    st.info(
                        f"Session ID: {data['session_id']}"
                    )

                    for file in data["files"]:
                        st.write(
                            f"✓ {file['filename']}"
                        )

                    for warning in data.get(
                        "warnings",
                        []
                    ):

                        st.warning(
                            warning
                        )

                else:
                    st.error(
                        data["message"]
                    )

            except requests.exceptions.ConnectionError:
                st.error(
                    "Unable to connect to FastAPI backend."
                )

            except Exception as exc:
                st.error(
                    str(exc)
                )
    
    if st.session_state.session_id:
        st.success(
            f"Active Session:\n{st.session_state.session_id}"
        )

st.write(
    "Chat functionality coming next."
)