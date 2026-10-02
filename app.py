import os
from typing import Any

import streamlit as st
from azure.ai.projects import AIProjectClient
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="GPT-5 Foundry Chat", page_icon="💬")


def required_setting(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


@st.cache_resource
def get_client():
    credential = ClientSecretCredential(
        tenant_id=required_setting("AZURE_TENANT_ID"),
        client_id=required_setting("AZURE_CLIENT_ID"),
        client_secret=required_setting("AZURE_CLIENT_SECRET"),
    )
    project_client = AIProjectClient(
        endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT")
        or required_setting("AZURE_OPENAI_ENDPOINT"),
        credential=credential,
    )
    return project_client.get_openai_client()


def stream_reply(messages: list[dict[str, Any]]):
    client = get_client()
    response = client.chat.completions.create(
        model=required_setting("AZURE_OPENAI_DEPLOYMENT"),
        messages=messages,
        max_completion_tokens=int(os.getenv("MAX_COMPLETION_TOKENS", "2048")),
        stream=True,
    )
    for chunk in response:
        content = chunk.choices[0].delta.content if chunk.choices else None
        if content:
            yield content


st.title("💬 GPT-5 Foundry Chat")
st.caption("Authenticated with Microsoft Entra ID using a client ID and client secret.")

with st.sidebar:
    st.header("Settings")
    system_prompt = st.text_area(
        "System prompt",
        value="You are a helpful assistant.",
        help="This prompt is sent with every new conversation.",
    )
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": system_prompt}]
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Message GPT-5"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            answer = st.write_stream(stream_reply(st.session_state.messages))
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as exc:
            st.error(f"Request failed: {exc}")
            st.info("Check the endpoint, deployment name, Entra credentials, and app registration permissions.")
