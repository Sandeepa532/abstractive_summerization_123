# app.py

import streamlit as st
from model import (
    load_summarization_model,
    generate_summary,
    get_important_sentences,
    get_excluded_facts
)
from utils import read_uploaded_file, clean_text
from keybert import KeyBERT

# Load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page settings
st.set_page_config(page_title="🧠 FOE Summarizer", page_icon="📝", layout="wide")
local_css("styles.css")

st.title("🧠 Fact Omission Explanation (FOE) Summarizer")
st.markdown("Summarize documents and explain **what facts were omitted and why** ✨")

# Load models
st.sidebar.title("⚙️ Settings")
tokenizer, model = load_summarization_model()
kpm_model = KeyBERT()

# Input
st.subheader("📄 Input Your Document")
# app.py

uploaded_file = st.file_uploader(
    "Upload a document (.txt, .pdf, .docx)", 
    type=["txt", "pdf", "docx"]
)

text_input = st.text_area("Or paste your text here:", height=300)

text = ""
if uploaded_file:
    text = read_uploaded_file(uploaded_file)
elif text_input:
    text = text_input

# Actions
if text:
    if st.button("🔍 Summarize"):
        cleaned_text = clean_text(text)
        summary = generate_summary(cleaned_text, tokenizer, model)

        st.subheader("📝 Generated Summary")
        st.success(summary)

        option = st.radio(
            "Select what you want to see:",
            ("Important Sentences", "Excluded Facts with Reasons")
        )

        if option == "Important Sentences":
            st.subheader("📌 Important Sentences")
            important_sentences = get_important_sentences(cleaned_text, summary)
            for idx, sentence in enumerate(important_sentences, 1):
                st.markdown(f"**{idx}.** {sentence}")

        elif option == "Excluded Facts with Reasons":
            st.subheader("❌ Excluded Facts and Their Reasons")
            excluded_facts = get_excluded_facts(cleaned_text, summary, kpm_model)
            for idx, (fact, reasons) in enumerate(excluded_facts.items(), 1):
                st.markdown(f"**{idx}. Fact:** {fact}")
                for reason in reasons:
                    st.write(f"  - **Reason:** {reason}")

# Clear button
if st.button("🧹 Clear All"):
    st.experimental_rerun()
