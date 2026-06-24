import streamlit as st

def render_header():

    st.markdown(
        "<div class='main-title'>Virtual Teaching Assistant</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='logo-box'>🎓</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>Ask From Your Own File</div>",
        unsafe_allow_html=True
    )

    st.write("")