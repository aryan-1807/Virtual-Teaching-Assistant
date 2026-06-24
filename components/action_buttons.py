import streamlit as st

def render_buttons():

    c1, c2, c3, c4, c5 = st.columns(5)

    summarize = c1.button("Summarize")
    mcq = c2.button("Frame MCQ")
    flashcard = c3.button("Flashcards")
    qa = c4.button("Q/A")
    read = c5.button("Read Aloud")

    return summarize, mcq, flashcard, qa, read