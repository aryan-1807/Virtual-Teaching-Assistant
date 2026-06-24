import streamlit as st
from components.uploader import render_uploaders

def render_sidebar():
    st.subheader("📜 Chat History")
    
    # Render active list elements with multi-schema structural safety guards
    if "chat_history" in st.session_state and st.session_state.chat_history:
        for idx, item in enumerate(reversed(st.session_state.chat_history)):
            # Guard check: Ensure item is a dictionary before reading keys
            if isinstance(item, dict):
                # Fallback extraction to read safely from BOTH old and new data schemas
                role = item.get("role")
                content = item.get("content") or item.get("query") or "Action Trigger"
                
                # Only display user questions to keep history clean
                if role == "user" or "role" not in item:
                    preview_text = str(content)[:25]
                    if st.button(f"💬 {preview_text}...", key=f"hist_{idx}"):
                        pass
    else:
        st.caption("No active history items saved in this session.")
        
    st.divider()
    
    # Return exactly 4 items
    image, pdf, handdrawn, video = render_uploaders()
    return image, pdf, handdrawn, video