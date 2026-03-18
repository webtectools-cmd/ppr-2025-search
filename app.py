import streamlit as st
import google.generativeai as genai
import time

# Securely get API Key from Streamlit Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("📑 PPR 2025 Search Panel")
st.write("Upload the Gazette and search for any Rule (বিধি).")

# Permanent Upload for your session
uploaded_file = st.file_uploader("Upload your PPR-2025 PDF", type=['pdf'])

if uploaded_file:
    with open("doc.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    if 'file_id' not in st.session_state:
        with st.spinner("Gemini is reading the PPR 2025..."):
            file_ref = genai.upload_file(path="doc.pdf")
            while file_ref.state.name == "PROCESSING":
                time.sleep(2)
                file_ref = genai.get_file(file_ref.name)
            st.session_state.file_id = file_ref
        st.success("Ready!")

    query = st.text_input("Enter Rule number or Keyword (e.g., বিধি ৩৬ বা পারফরম্যান্স সিকিউরিটি):")
    if query:
        model = genai.GenerativeModel("gemini-1.5-flash")
        # Directing Gemini to act as a PE/Procurement Expert
        response = model.generate_content([st.session_state.file_id, f"Answer in Bengali as a procurement expert based on this PDF: {query}"])
        st.info(response.text)
