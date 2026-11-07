# AI Study Assistant

A beginner-friendly AI web app built with Streamlit and Google's Gemini API.

## Features
- AI chat for study questions
- Explain a topic at a selected level
- Summarize pasted text
- Generate revision notes and mark-based answers

## 1. Run locally (Windows PowerShell)

```powershell
cd ai-study-assistant
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml` and add:

```toml
GEMINI_API_KEY = "PASTE_YOUR_API_KEY_HERE"
```

Start the app:

```powershell
streamlit run app.py
```

Open the local URL shown in the terminal (usually http://localhost:8501).

## 2. Get a Gemini API key
Create a key in [Google AI Studio](https://aistudio.google.com/app/apikey).
Keep the key private. Do not paste it into `app.py` or commit it to GitHub.
API access and usage limits depend on Google's current terms and quotas.

## 3. Deploy free using Streamlit Community Cloud

1. Create a GitHub repository, for example `ai-study-assistant`.
2. Upload `app.py`, `requirements.txt`, `README.md`, and `.gitignore`.
3. Open [Streamlit Community Cloud](https://share.streamlit.io/) and sign in with GitHub.
4. Choose **Create app**, select your repository and branch, and set the main file to `app.py`.
5. Open **Advanced settings** → **Secrets** and add:

```toml
GEMINI_API_KEY = "PASTE_YOUR_API_KEY_HERE"
```

6. Click **Deploy**. Streamlit will provide a public `streamlit.app` URL.

## Project structure

```text
ai-study-assistant/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml   # create locally; do not upload
```
