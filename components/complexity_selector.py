import streamlit as st

def render_complexity():

    return st.radio(
        "Complexity",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ],
        index=1
    )