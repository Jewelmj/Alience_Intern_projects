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

def render_sidebar():
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
                        files=files,
                        data={
                            "session_id": st.session_state.session_id
                        }
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

def render_chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if (
                message["role"] == "assistant"
                and "interaction_id" in message
            ):

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                        "👍 Helpful",
                        key=f"helpful_{message['interaction_id']}"
                    ):

                        requests.post(
                            f"{API_BASE_URL}/feedback",
                            json={
                                "interaction_id":
                                message["interaction_id"],
                                "feedback":
                                "helpful"
                            }
                        )

                        st.success(
                            "Feedback recorded"
                        )

                with col2:
                    if st.button(
                        "👎 Not Helpful",
                        key=f"not_helpful_{message['interaction_id']}"
                    ):

                        requests.post(
                            f"{API_BASE_URL}/feedback",
                            json={
                                "interaction_id":
                                message["interaction_id"],
                                "feedback":
                                "not_helpful"
                            }
                        )

                        st.success(
                            "Feedback recorded"
                        )

            if (
                message["role"] == "assistant"
                and "sources" in message
                and message["sources"]
            ):

                with st.expander("Sources"):
                    for source in (message["sources"]):
                        st.write(f"File: {source['source_file']}")

                        st.write(f"Chunk: {source['chunk_id']}")

                        st.write(f"Similarity: {source['similarity_score']}")

                        st.write(source["text_preview"])

                        st.divider()

    prompt = st.chat_input(
        "Ask a question about your documents"
    )

    if prompt:
        if not st.session_state.session_id:
            st.warning("Upload documents before chatting.")
        else:
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )

            try:
                response = requests.post(
                    f"{API_BASE_URL}/chat",
                    json={
                        "query": prompt,
                        "session_id":
                            st.session_state.session_id
                    }
                )

                response.raise_for_status()
                data = response.json()
                

                if data["status"] == "success":

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": data["answer"],
                            "sources": data["sources"],
                            "interaction_id": data["interaction_id"]
                        }
                    )

                elif data["status"] == "not_found":
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": data["answer"],
                            "sources": [],
                            "interaction_id": data["interaction_id"]
                        }
                    )

                else:
                    st.error(data["message"])

            except requests.exceptions.ConnectionError:
                st.error("Unable to connect to FastAPI backend.")
            except Exception as exc:
                st.error(str(exc))

            st.rerun()

def render_dashboard():
    st.header(
        "Retrieval Dashboard"
    )

    try:
        response = requests.get(
            f"{API_BASE_URL}/analytics/retrieval"
        )

        data = response.json()
        records = data["records"]

        if not records:
            st.info("No retrieval data available.")
            return

    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to backend.")
        return

    except Exception as exc:
        st.error(str(exc))
        return
    
    # Calculate Metrics
    total_queries = len(records)

    latencies = [
        record["retrieval_latency_ms"]
        for record in records
        if "retrieval_latency_ms" in record
    ]

    avg_latency = (
        sum(latencies) / len(latencies)
        if latencies
        else 0
    )

    scores = []

    for record in records:
        scores.extend(
            record.get(
                "similarity_scores",
                []
            )
        )

    avg_similarity = (
        sum(scores) / len(scores)
        if scores
        else 0
    )

    chunk_counts = [
        record["filtered_chunk_count"]
        for record in records
        if "filtered_chunk_count" in record
    ]

    avg_chunks = (
        sum(chunk_counts) / len(chunk_counts)
        if chunk_counts
        else 0
    )

    successes = [
        record["retrieval_success"]
        for record in records
        if "retrieval_success" in record
    ]

    success_rate = (
        (
            sum(successes)
            / len(successes)
        ) * 100
        if successes
        else 0
    )

    # Display Metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Queries",
            total_queries
        )

        st.metric(
            "Average Similarity Score",
            f"{avg_similarity:.3f}"
        )

        st.metric(
            "Average Retrieved Chunks",
            f"{avg_chunks:.1f}"
        )

    with col2:
        st.metric(
            "Average Retrieval Latency",
            f"{avg_latency:.1f} ms"
        )

        st.metric(
            "Retrieval Success Rate",
            f"{success_rate:.1f}%"
        )

        st.metric(
            "Tracked Retrievals",
            len(latencies)
        )

    st.caption(
        f"Detailed retrieval metrics are available for "
        f"{len(latencies)} of {total_queries} interactions."
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

render_sidebar()

chat_tab, dashboard_tab = st.tabs(
    ["💬 Chat","📊 Retrieval Dashboard"]
)

with chat_tab:
    render_chat()

with dashboard_tab:
    render_dashboard()