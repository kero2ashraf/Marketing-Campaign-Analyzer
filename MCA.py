import os
import streamlit as st
from google import genai
from google.genai import types

# ─── Configuration ────────────────────────────────────────────────────
API_KEY  = "AIzaSyDrhFxXARTxMSb-0DgQFkqrIDuZQscVgSE"
MODEL    = "gemini-2.0-flash-lite"
CHUNK_SZ = 1_000_000

# ─── Initialize Gemini client ─────────────────────────────────────────
try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Failed to initialize Gemini client: {e}")
    st.stop()

# ─── Helpers ───────────────────────────────────────────────────────────
def read_in_chunks(data: bytes, chunk_size: int = CHUNK_SZ):
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]

def analyze_file_and_prompt(uploaded, prompt_text):
    raw = uploaded.read()
    name = uploaded.name.lower()
    if name.endswith(".csv"):
        mime = "text/csv"
    elif name.endswith(".txt"):
        mime = "text/plain"
    elif name.endswith(".pdf"):
        mime = "application/pdf"
    elif name.endswith(".xlsx"):
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    else:
        mime = "application/octet-stream"

    parts = [
        types.Part.from_bytes(data=chunk, mime_type=mime)
        for chunk in read_in_chunks(raw)
    ]
    parts.append(prompt_text)

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=parts
        )
        return response.text
    except Exception as e:
        return f"❗️ API error: {e}"

# ─── Streamlit UI ───────────────────────────────────────────────────────
st.set_page_config(page_title="Marketing Campaign Analyzer", layout="centered")
st.markdown("## 📊 Marketing Campaign Analyzer (MCA)")
st.markdown("---")
st.info("Upload XLSX, CSV, PDF or TXT and enter a message to start.")

uploaded_file = st.file_uploader("Upload your file", type=["xlsx","csv"])
user_prompt   = st.text_input("Enter your message", placeholder="e.g., Summarize key findings")

st.markdown("### 🧠 Gemini Result")
if uploaded_file and user_prompt:
    with st.spinner("Analyzing..."):
        answer = analyze_file_and_prompt(uploaded_file, user_prompt)
    if answer.startswith("❗️ API error"):
        st.error(answer)
    else:
        st.success("✅ Analysis Complete!")
        st.markdown("#### 📌 Response:")
        st.write(answer)
        st.markdown("---")
        st.markdown("🎉 **Thanks for using MCA**")
