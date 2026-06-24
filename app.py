import sys
import subprocess

# --- INLINE ENVIRONMENT GUARD ---
try:
    from moviepy.editor import VideoFileClip
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "decorator==4.4.2", "moviepy==1.0.3", "SpeechRecognition==3.10.0"])

import os
import streamlit as st

from components.sidebar import render_sidebar
from components.header import render_header
from components.action_buttons import render_buttons
from components.complexity_selector import render_complexity

from utils.helpers import load_css
from utils.constants import PAGE_TITLE, LAYOUT_STYLE
from services.pdf_processor import extract_pdf_text
from services.image_processor import extract_image_text
from services.video_processor import extract_video_text
from services.mcq_service import parse_mcqs
from services.flashcard_service import parse_flashcards
from services.summary_service import parse_summary_blocks
from services.qa_service import convert_to_qa_format
from services.tts_service import speak_text
from services.document_store import (
    save_document,
    load_document,
    save_vector_store,
    load_vector_store
)
from services.rag_service import (
    create_vector_store,
    search_document
)
from services.llm_service import ask_gemini

# 1. Base Initialization
st.set_page_config(page_title=PAGE_TITLE, layout=LAYOUT_STYLE)
load_css()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "processed_file_identifier" not in st.session_state:
    st.session_state.processed_file_identifier = None
if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""
if "last_level" not in st.session_state:
    st.session_state.last_level = "Intermediate"
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "QA"
if "active_file_type" not in st.session_state:
    st.session_state.active_file_type = None
if "last_execution_query" not in st.session_state:
    st.session_state.last_execution_query = ""

# 2. UI Layout Structures
left, middle, right = st.columns([1.3, 4, 1.2])

with left:
    image, pdf, handdrawn, video = render_sidebar()

with right:
    level = render_complexity()

with middle:
    render_header()
    
    incoming_text = ""
    current_source_name = None
    detected_type = None

    if pdf:
        current_source_name = f"PDF: {pdf.name}"
        detected_type = "pdf"
    elif image:
        current_source_name = f"Image: {image.name}"
        detected_type = "image"
    elif handdrawn:
        current_source_name = f"HandDrawn Sketch: {handdrawn.name}"
        detected_type = "handdrawn"
    elif video:
        current_source_name = f"Video: {video.name}"
        detected_type = "video"

    # --- TOP PRIORITY BLANKET CLEAN SWEEP TRIGGER ---
    if detected_type and detected_type != st.session_state.active_file_type:
        if detected_type != "image": st.session_state.img_version += 1
        if detected_type != "pdf": st.session_state.pdf_version += 1
        if detected_type != "handdrawn": st.session_state.hand_version += 1
        if detected_type != "video": st.session_state.vid_version += 1
        
        st.session_state.last_answer = ""
        st.session_state.current_mode = "QA"
        st.session_state.chat_history = []
        st.session_state.active_file_type = detected_type
        st.session_state.last_execution_query = ""
        save_document("")
        st.rerun()

    if current_source_name is None and st.session_state.processed_file_identifier is not None:
        st.session_state.last_answer = ""
        st.session_state.current_mode = "QA"
        st.session_state.chat_history = []
        st.session_state.processed_file_identifier = None
        st.session_state.active_file_type = None
        st.session_state.last_execution_query = ""
        save_document("")
        st.rerun()

    # --- PROCESSING PIPELINE ENGINE & AUTO-SOLVER ---
    if current_source_name and st.session_state.processed_file_identifier != current_source_name:
        with st.spinner(f"Reading content from {current_source_name}..."):
            if pdf:
                incoming_text = extract_pdf_text(pdf)
            elif image:
                incoming_text = extract_image_text(image)
            elif handdrawn:
                incoming_text = extract_image_text(handdrawn)
            elif video:
                incoming_text = extract_video_text(video)

        if incoming_text and incoming_text.strip() and "Error" not in incoming_text:
            save_document(incoming_text)
            index, chunks = create_vector_store(incoming_text)
            save_vector_store(index, chunks)
            st.session_state.processed_file_identifier = current_source_name
            
            # --- CUSTOM CENTER TOP FLASH TOAST INJECTION ---
            st.markdown(f"""
                <div id="custom-toast" style="
                    position: fixed;
                    top: 25px;
                    left: 50%;
                    transform: translateX(-50%);
                    background-color: #10b981;
                    color: white;
                    padding: 12px 24px;
                    border-radius: 8px;
                    font-weight: 500;
                    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
                    z-index: 999999;
                    animation: fadeout 1.5s forwards;
                    font-family: sans-serif;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                ">
                    🎯 Loaded and indexed {current_source_name}!
                </div>
                <style>
                    @keyframes fadeout {{
                        0% {{ opacity: 1; top: 25px; }}
                        75% {{ opacity: 1; top: 25px; }}
                        100% {{ opacity: 0; top: -60px; display: none; }}
                    }}
                </style>
            """, unsafe_allow_html=True)
            
            # AUTO-SOLVE PIPELINE FOR SKETCHES
            if detected_type == "handdrawn":
                with st.spinner("Analyzing and solving your sketch content..."):
                    execution_query = f"Analyze, process, solve, and explain the following handwritten data step-by-step: {incoming_text}"
                    answer = ask_gemini(execution_query, incoming_text, level=level, task_type="QA")
                    
                    cleaned_answer = answer.replace("===START_STUDY_GUIDE_FINAL_ANSWER===", "").strip()
                    st.session_state.last_answer = cleaned_answer
                    st.session_state.last_level = level
                    st.session_state.current_mode = "QA"
                    st.session_state.last_execution_query = execution_query
                    
                    st.session_state.chat_history.append({"role": "user", "content": f"📝 *Uploaded Handwritten Sketch:* \"{incoming_text.strip()}\"", "mode": "QA"})
                    st.session_state.chat_history.append({"role": "assistant", "content": cleaned_answer, "mode": "QA", "level": level})
            
            st.rerun()
        elif incoming_text and "Error" in incoming_text:
            st.error(incoming_text)

    # Action Toolbar
    summarize, mcq, flashcard, qa_mode, read = render_buttons()

    if st.session_state.processed_file_identifier:
        if st.button("🗑️ Clear Active Source Cache"):
            st.session_state.img_version += 1
            st.session_state.pdf_version += 1
            st.session_state.hand_version += 1
            st.session_state.vid_version += 1
            st.session_state.processed_file_identifier = None
            st.session_state.active_file_type = None
            st.session_state.last_answer = ""
            st.session_state.last_execution_query = ""
            st.session_state.chat_history = []
            save_document("")
            st.rerun()

    task_mode = None
    active_trigger = False
    execution_query = ""

    if summarize:
        task_mode = "SUMMARIZE"
        execution_query = "Generate Summary"
        active_trigger = True
    elif mcq:
        task_mode = "MCQ"
        execution_query = "Generate Multiple Choice Assessment Questions"
        active_trigger = True
    elif flashcard:
        task_mode = "FLASHCARD"
        execution_query = "Generate Concepts Flashcards"
        active_trigger = True
    elif qa_mode:
        task_mode = "CONVERT_QA"
        active_trigger = True
    elif st.session_state.last_answer and level != st.session_state.last_level:
        task_mode = st.session_state.current_mode
        execution_query = st.session_state.last_execution_query
        active_trigger = True

    # --- CHAT INPUT INTERFACE WIDGET ---
    user_chat_input = st.chat_input("Ask anything about your active file layout...")
    if user_chat_input and user_chat_input.strip():
        task_mode = "QA"
        execution_query = user_chat_input.strip()
        active_trigger = True

    # Processing Core Loops
    if active_trigger and task_mode and (execution_query or task_mode == "CONVERT_QA"):
        index, chunks = load_vector_store()
        
        if index is not None:
            with st.spinner(f"Processing request in {level} Mode..."):
                if task_mode == "CONVERT_QA":
                    full_context = load_document()
                    answer = convert_to_qa_format(full_context, level=level)
                else:
                    context = search_document(execution_query, index, chunks)
                    answer = ask_gemini(execution_query, context, level=level, task_type=task_mode)
                
                cleaned_answer = answer.replace("===START_STUDY_GUIDE_FINAL_ANSWER===", "").strip()
                
                st.session_state.last_answer = cleaned_answer
                st.session_state.last_level = level
                st.session_state.current_mode = task_mode
                st.session_state.last_execution_query = execution_query
                
                if task_mode == "QA":
                    st.session_state.chat_history.append({"role": "user", "content": execution_query, "mode": "QA"})
                else:
                    st.session_state.chat_history.append({"role": "user", "content": f"🎯 Triggered Action: {task_mode} Tool", "mode": task_mode})
                    
                st.session_state.chat_history.append({"role": "assistant", "content": cleaned_answer, "mode": task_mode, "level": level})
                st.rerun()
        else:
            st.warning("Please upload a file source in the left sidebar to activate analysis.")

    # --- 4. RENDER PERSISTENT ALTERNATING CHAT WITH UNIFIED LOGOS ---
    if st.session_state.chat_history:
        st.divider()
        
        st.markdown("""
            <style>
                .stChatMessage[data-testid="stChatMessageUser"] {
                    margin-left: auto !important;
                    width: fit-content !important;
                    max-width: 80% !important;
                }
                .stChatMessage[data-testid="stChatMessageAssistant"] {
                    margin-right: auto !important;
                    width: 100% !important;
                    max-width: 85% !important;
                }
                .stChatMessage .stMarkdown p {
                    margin-top: 0px !important;
                    padding-top: 0px !important;
                }
            </style>
        """, unsafe_allow_html=True)

        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.markdown(message["content"])
                else:
                    msg_mode = message.get("mode", "QA")
                    
                    if msg_mode == "MCQ":
                        parsed_questions = parse_mcqs(message["content"])
                        if parsed_questions:
                            for idx, item in enumerate(parsed_questions):
                                st.markdown(f"**Q: {item['question']}**")
                                options_list = [f"{k}: {v}" for k, v in item["options"].items()]
                                user_choice = st.radio("Select your answer:", options_list, key=f"chat_radio_{idx}_{hash(item['question'])}")
                                
                                if st.button(f"Submit Answer Choice {idx+1}", key=f"chat_btn_{idx}_{hash(item['question'])}"):
                                    if user_choice[0] == item["correct"]:
                                        st.success(f"🎯 Correct! Option {item['correct']} is right.")
                                    else:
                                        st.error(f"❌ Incorrect. The correct option was {item['correct']}.")
                                    st.info(f"**Explanation:** {item['explanation']}")
                                st.write("---")
                        else:
                            st.markdown(message["content"])
                            
                    elif msg_mode == "FLASHCARD":
                        parsed_cards = parse_flashcards(message["content"])
                        if parsed_cards:
                            cols = st.columns(2)
                            for i, card in enumerate(parsed_cards):
                                with cols[i % 2]:
                                    st.markdown(f'<div style="background:#1e293b; padding:12px; border-radius:8px; border:1px solid #334155; margin-bottom:10px;"><strong>Concept {i+1}:</strong><br>{card["front"]}</div>', unsafe_allow_html=True)
                                    with st.expander("🔄 Flip Card"):
                                        st.write(card['back'])
                        else:
                            st.markdown(message["content"])
                            
                    elif msg_mode == "SUMMARIZE":
                        summary_data = parse_summary_blocks(message["content"])
                        st.markdown("### 📝 Core Thesis Executive Overview")
                        st.info(summary_data["thesis"])
                        st.markdown("### 📌 Vital Takeaway Milestones")
                        for takeaway in summary_data["takeaways"]:
                            st.markdown(f"⚙️ {takeaway}")
                    else:
                        st.markdown(message["content"])

    # 5. Text-to-Speech Playback Tool
    if read:
        if st.session_state.last_answer:
            with st.spinner("Synthesizing audio presentation..."):
                speak_text(st.session_state.last_answer)
        else:
            st.info("No active text found to read aloud.")

    # 6. Raw Content Document Drawer View
    if st.session_state.processed_file_identifier:
        raw_text = load_document()
        if raw_text:
            st.write("")
            with st.expander(f"📄 View Active Knowledge Base Source Content ({st.session_state.processed_file_identifier})"):
                st.text_area("Extracted Characters (First 4000)", raw_text[:4000], height=250, disabled=True)