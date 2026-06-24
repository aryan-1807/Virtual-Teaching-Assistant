import streamlit as st

def render_uploaders():
    # Initialize version key counters if not present
    if "img_version" not in st.session_state:
        st.session_state.img_version = 0
    if "pdf_version" not in st.session_state:
        st.session_state.pdf_version = 0
    if "hand_version" not in st.session_state:
        st.session_state.hand_version = 0
    if "vid_version" not in st.session_state:
        st.session_state.vid_version = 0

    # 1. Image Uploader
    image = st.file_uploader(
        "Upload Image", 
        type=["png", "jpg", "jpeg"], 
        key=f"img_uploader_{st.session_state.img_version}"
    )
    
    # 2. PDF Uploader
    pdf = st.file_uploader(
        "Upload PDF", 
        type=["pdf"], 
        key=f"pdf_uploader_{st.session_state.pdf_version}"
    )
    
    # 3. Hand-Drawn Uploader
    handdrawn = st.file_uploader(
        "Upload Hand Drawn", 
        type=["png", "jpg", "jpeg"], 
        key=f"hand_uploader_{st.session_state.hand_version}"
    )
    
    # 4. Video Uploader
    video = st.file_uploader(
        "Upload Video", 
        type=["mp4"], 
        key=f"vid_uploader_{st.session_state.vid_version}"
    )
    
    return image, pdf, handdrawn, video