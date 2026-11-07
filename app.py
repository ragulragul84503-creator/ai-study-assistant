import os
import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #101426 0%, #171b35 55%, #202044 100%); }
    [data-testid="stSidebar"] { background: #11162b; }
    .hero { padding: 1.4rem 1.6rem; border: 1px solid #343b67; border-radius: 18px;
            background: linear-gradient(120deg, #242b52, #30264e); margin-bottom: 1rem; }
    .hero h1 { margin: 0; color: #fff; }
    .hero p { color: #c8ccec; margin: .45rem 0 0; }
    .stButton button { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

def get_api_key():
    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return os.getenv("GEMINI_API_KEY", "")

def ask_ai(prompt: str) -> str:
    key = get_api_key()
    if not key:
        raise RuntimeError(
            "Gemini API key is missing. Add GEMINI_API_KEY to "
            ".streamlit/secrets.toml locally or to your app's Cloud Secrets."
        )
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )
    return response.text or "I couldn't generate a response. Please try again."

st.markdown("""
<div class="hero">
  <h1>📚 AI Study Assistant</h1>
  <p>Your friendly learning companion — ask questions, simplify topics, summarize text, and create notes.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("✨ Study tools")
    mode = st.radio(
        "Choose a tool",
        ["AI Chat", "Explain a Topic", "Summarize Text", "Create Study Notes"],
    )
    st.divider()
    st.caption("Powered by Google's Gemini API")
    st.caption("Keep your API key private. Never add it to GitHub.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if mode == "AI Chat":
    st.subheader("💬 Ask anything")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask a study question...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    history = "\n".join(
                        f'{m["role"].upper()}: {m["content"]}'
                        for m in st.session_state.messages[-10:]
                    )
                    answer = ask_ai(
                        "You are a clear, friendly study assistant. Explain accurately "
                        "at a student-friendly level. If unsure, say so.\n\n" + history
                    )
                    st.markdown(answer)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )
                except Exception as exc:
                    st.error(str(exc))
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

elif mode == "Explain a Topic":
    st.subheader("🧠 Explain a difficult topic")
    topic = st.text_input("Topic", placeholder="Example: Database normalization")
    level = st.selectbox("Explanation level", ["Beginner", "School student", "College student"])
    if st.button("Explain topic", type="primary"):
        if topic.strip():
            with st.spinner("Preparing your explanation..."):
                try:
                    result = ask_ai(
                        f"Explain '{topic}' for a {level}. Use a short definition, "
                        "simple points, one practical example, and a quick recap."
                    )
                    st.markdown(result)
                except Exception as exc:
                    st.error(str(exc))
        else:
            st.warning("Please enter a topic.")

elif mode == "Summarize Text":
    st.subheader("📝 Summarize long text")
    source_text = st.text_area("Paste your text", height=230, placeholder="Paste notes, an article, or a lesson here...")
    style = st.selectbox("Summary style", ["Short bullet points", "One paragraph", "Detailed study summary"])
    if st.button("Summarize", type="primary"):
        if source_text.strip():
            with st.spinner("Summarizing..."):
                try:
                    result = ask_ai(
                        f"Summarize the text below as {style}. Preserve important facts "
                        "and do not invent details.\n\nTEXT:\n{source_text}"
                    )
                    st.markdown(result)
                except Exception as exc:
                    st.error(str(exc))
        else:
            st.warning("Please paste some text first.")

else:
    st.subheader("📖 Generate study notes")
    subject = st.text_input("Subject or chapter", placeholder="Example: SQL Joins")
    marks = st.selectbox("Answer length", ["Quick revision", "5-mark answer", "8-mark answer", "13-mark answer"])
    if st.button("Create notes", type="primary"):
        if subject.strip():
            with st.spinner("Creating your notes..."):
                try:
                    result = ask_ai(
                        f"Create clear study notes about '{subject}' for {marks}. "
                        "Include a definition, organized headings, key points, and a simple example. "
                        "Use original wording and keep it appropriate for a student."
                    )
                    st.markdown(result)
                except Exception as exc:
                    st.error(str(exc))
        else:
            st.warning("Please enter a subject or chapter.")

st.divider()
st.caption("AI can make mistakes. Check important information with your textbook or teacher.")
