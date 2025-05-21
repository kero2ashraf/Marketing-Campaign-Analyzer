import streamlit as st
from google import genai
from google.genai import types

# Initialize Gemini client
genai_client = genai.Client(api_key="AIzaSyDrhFxXARTxMSb-0DgQFkqrIDuZQscVgSE")

# Function to analyze file and user prompt
def analyze_file_and_prompt(file, user_prompt):
    file_data = file.read()
    response = genai_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            types.Part.from_bytes(
                data=file_data,
                mime_type='text/csv' if file.name.endswith('.csv') else 'text/plain'
            ),
            user_prompt
        ]
    )
    return response.text

# === Streamlit UI ===
st.set_page_config(page_title="Marketing Campaign Analyzer", layout="centered")

# === Logo and Project Name ===
logo_path = r"C:\Users\kirol\OneDrive - Arab Open University - AOU\Desktop\Test\logo.png"
col1, col2 = st.columns([1, 6])
with col1:
    st.image(logo_path, width=80)
with col2:
    st.markdown("## Marketing Campaign Analyzer (MCA)")

st.markdown("---")

# === Info Message ABOVE Upload ===
st.info("Please upload a file and enter a message to start analysis.")

# === Small Page 1: File Upload ===
st.markdown("### 🗂️ Upload Data")
uploaded_file = st.file_uploader("Upload your file (CSV or TXT)", type=["csv", "txt"])

# === Small Page 2: User Prompt ===
st.markdown("### 💬 Ask a Question")
user_prompt = st.text_input("Enter your message", placeholder="e.g., Analyze the campaign performance")

# === Small Page 3: Output Display ===
st.markdown("### 🧠 Gemini Result")

if uploaded_file and user_prompt:
    with st.spinner("Analyzing..."):
        result = analyze_file_and_prompt(uploaded_file, user_prompt)
        st.success("✅ Analysis Complete!")
        st.markdown("#### 📌 Response:")
        st.write(result)
        st.markdown("---")
        st.markdown("🎉 **Thanks for using MCA**")
