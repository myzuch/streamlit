import streamlit as st
import PyPDF2
import time


def summarize_text(input_text, sections):
    summary = f"Summary for sections: {', '.join(sections)}"
    return summary

def get_html_page(summary, input_text):
    with open("styles.css", "r") as css_file:
        css_code = css_file.read()

    with open("script.js", "r") as js_file:
        js_code = js_file.read()

    with open("index.html", "r") as html_file:
        html_page = html_file.read()

    return html_page.format(summary=summary, input_text=input_text,
                            js_code=js_code, css_code=css_code)


sections = ['Subject & demographics', 'Allergies', 'Medications', 'Problems', 'Author of transaction']

if "text" not in st.session_state:
    st.session_state.text = ""
# if "summary" not in st.session_state:
#     st.session_state.summary = ""

st.title("Summarization")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file and not st.session_state.text:
    # read text from pdf to session state
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    st.session_state.text = text

elif not uploaded_file:
    # remove text from session state if pdf was removed
    st.session_state.text = ''
    st.write("Or")

if not st.session_state.text:
    # get text from input field if no pdf is given
    st.session_state.text = st.text_area("Enter text to summarize:")

# if not st.session_state.text:
#     st.session_state.summary = ''

selected_sections = st.multiselect("Select sections to include in the summary:", sections)

if st.button("Summarize"):
    if st.session_state.text:
        text = st.session_state.text
        if selected_sections:
            # if not st.session_state.summary:
            time.sleep(3)
            summary = summarize_text(text, selected_sections)
            wrapped_summary = f'<span class="sentence" ref="1">{summary}</span>\n<span class="sentence" ref="2">{summarize_text(text, selected_sections)}</span>'
            wrapped_text = f'<span class="chunk" id="1">{text}</span>\n<span class="chunk" id="2">{text}</span>'

            html_code = get_html_page(wrapped_summary, wrapped_text)
            st.components.v1.html(html_code, height=600)
        else:
            st.warning("Please select at least one section to include in the summary.")
    else:
        st.warning("Please enter some text to summarize.")