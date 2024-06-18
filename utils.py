from typing import Dict, List
from bs4 import BeautifulSoup
import re
import streamlit as st
from markdown import markdown
from chains import *
from sentence_transformers import util

@st.cache_data(show_spinner=False)
def get_summary_and_text(input_text, sections, embed_model=None):
    html_summary = markdown(get_summary(input_text, sections))
    input_sentences = input_text.split("\n")

    return match_li_to_sentences(html_summary, input_sentences, embed_model)

def get_text_display_html(summary, input_text):
    with open("text-display/styles.css", "r") as css_file:
        css_code = css_file.read()

    with open("text-display/script.js", "r") as js_file:
        js_code = js_file.read()

    with open("text-display/index.html", "r") as html_file:
        html_page = html_file.read()

    return html_page.format(
        summary=summary, input_text=input_text, js_code=js_code, css_code=css_code
    )


def get_top_matches(sents_a: list[str], sents_b: list[str], embed_model=st.session_state.embed_model) -> list[list[int]]:
    """
    Return a list of lists with indexes of sentences from `sents_b`
    that contain `sents_a`.
    """

    regex_matches = []
    for i, sent_a in enumerate(sents_a):
        matches = []
        for j, sent_b in enumerate(sents_b):
            match = re.search(r"(?i)" + re.escape(sent_a), sent_b)
            if match:
                matches.append(j)
        if not matches:
            matches.append(-1)
            regex_matches.append(matches)
        else:
            regex_matches.append(matches)

    if embed_model:
        emb_a, emb_b = embed_model.encode(sents_a), embed_model.encode(sents_b) 
        cos_matches = get_cosine_matches(emb_a, emb_b, top_k=1)
        for i in range(len(regex_matches)):
            if regex_matches[i] == [-1]:
                regex_matches[i] = cos_matches[i]
                
    assert len(regex_matches) == len(sents_a)
    return regex_matches


def get_cosine_matches(emb_a, emb_b, top_k=3):
    """
    Find the top `k` most similar elements between two sets of embeddings based on cosine similarity.

    Args:
        emb_a (2D array-like): A set of embeddings.
        emb_b (2D array-like): Another set of embeddings.
        top_k (int, optional): The number of top matches to return for each element in `emb_a`. Defaults to 3.

    Returns:
        list: A list of lists, where each inner list contains the indices of the top `k` most similar elements in `emb_b` for the corresponding element in `emb_a`.
    """
    scores = util.cos_sim(emb_a, emb_b)

    all_matches = []
    for row in scores:
        matches = [(j, score) for j, score in enumerate(row)]  # if score >= threshold]
        matches = sorted(matches, key=lambda x: x[1], reverse=True)
        matches = [(x[0]) for x in matches[:top_k]]
        all_matches.append(matches)
    return all_matches


def wrap_input_text_sentences(text_sentences: str) -> str:
    """Wraps each sentence in the original text with <span class="chunk" id="...">"""
    original_text_html = ""
    for i, sentence in enumerate(text_sentences):
        begin_tag = f'<span class="chunk" id="{i}">'
        end_tag = "</span>"
        original_text_html += f"{begin_tag}{sentence}{end_tag}"
    return original_text_html


def match_li_to_sentences(html_summary, text_sentences, embed_model, threshold=0.1):
    """
    Wrap each <li> element in the given HTML summary with <span> tag
    that contains reference(s) to the corresponding sentences in the original text.

    Then wrap each sentence in the original text with a <span> tag containing its index.

    Args:
        html_summary (str): The HTML summary to be processed. (only <li> tags are processed)
        original_text (str): The original text from which the summary was generated.

    Returns:
        Tuple[str, str]: The processed HTML summary and the original text with sentences wrapped in <span> tags.
    """
    soup = BeautifulSoup(html_summary, "html.parser")
    li_elements = soup.find_all("li")
    summary_elements = [x.get_text() for x in li_elements]
    references = get_top_matches(summary_elements, text_sentences)
    # Wrap each <li> element with <span class="sentence" ref="...">
    for i, li in enumerate(li_elements):
        ref_indices = references[i]
        span_tag = soup.new_tag("span", attrs={"class": "sentence"})
        if li.get_text():
            span_tag.string = li.get_text()
            ref_attrs = " ".join([f"{idx}" for idx in ref_indices])
            span_tag["ref"] = ref_attrs
            li.contents = []
            li.append(span_tag)

    return str(soup), wrap_input_text_sentences(text_sentences)
