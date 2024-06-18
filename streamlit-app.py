import streamlit as st
import PyPDF2
from dotenv import load_dotenv
from utils import *
from streamlit.components.v1 import html
from sentence_transformers import SentenceTransformer

load_dotenv()

if "text" not in st.session_state:
    st.session_state.text = ""
# if "summary" not in st.session_state:
#     st.session_state.summary = ""
if "embed_model" not in st.session_state:
    st.session_state.embed_model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")

st.title("Summarization")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf", "txt"])

if uploaded_file and not st.session_state.text:
    # read text from pdf to session state
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    st.session_state.text = text

elif not uploaded_file:
    # remove text from session state if pdf was removed
    st.session_state.text = ""
    st.write("Or")

if not st.session_state.text:
    # get text from input field if no pdf is given
    st.session_state.text = st.text_area("Enter text to summarize:")

# if not st.session_state.text:
#     st.session_state.summary = ''

selected_sections = st.multiselect(
    "Select sections to include in the summary:", SECTIONS.keys()
)

if st.button("Summarize"):
    if st.session_state.text:
        input_text = st.session_state.text
        if selected_sections:
            # if not st.session_state.summary:
            wrapped_summary, wrapped_text = get_summary_and_text(
                input_text, selected_sections
            )

            html_code = get_text_display_html(wrapped_summary, wrapped_text)
            html(html_code, height=600, width=800)
        else:
            st.warning("Please select at least one section to include in the summary.")
    else:
        st.warning("Please enter some text to summarize.")
