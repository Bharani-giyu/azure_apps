# GPT-5 Microsoft Foundry Streamlit Chat

A local Streamlit chat app that calls a GPT-5 deployment through the Microsoft Foundry `AIProjectClient`. Authentication uses a Microsoft Entra service principal (`tenant ID`, `client ID`, and `client secret`); no API key or manually configured bearer-token scope is required.

## Prerequisites

- Python 3.10+
- A Microsoft Foundry/Azure OpenAI-compatible resource with a GPT-5 deployment
- An Entra app registration/service principal with permission to invoke the model

## Configure

1. Create a virtual environment and install dependencies from `requirements.txt`.
2. Copy `.env.example` to `.env`.
3. Set these values in `.env`:
   - `AZURE_TENANT_ID`: Entra tenant ID
   - `AZURE_CLIENT_ID`: app registration/application ID
   - `AZURE_CLIENT_SECRET`: client secret value
   - `AZURE_AI_PROJECT_ENDPOINT`: Microsoft Foundry project endpoint, for example `https://<resource>.services.ai.azure.com/api/projects/<project-name>`
   - `AZURE_OPENAI_DEPLOYMENT`: the exact deployment name for GPT-5
   - `AZURE_OPENAI_ENDPOINT`: legacy fallback for the project endpoint if `AZURE_AI_PROJECT_ENDPOINT` is not set

The app registration must have the appropriate Azure OpenAI/Foundry data-plane role, such as **Cognitive Services OpenAI User**, on the resource or project. A client secret is sensitive: do not commit `.env`, paste it into source code, or expose it in the browser.

## Run

Start Streamlit with:

```text
streamlit run app.py
```

Then open the local URL shown by Streamlit.

## Notes

- `AZURE_OPENAI_DEPLOYMENT` is the deployment name, not necessarily the model name `gpt-5`.
- The app streams assistant output and keeps conversation history in the current browser session.
- For production, prefer managed identity or another secret store over a client secret.
