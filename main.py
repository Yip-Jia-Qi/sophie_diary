import os

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

from utils import *

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
load_resources()

st.set_page_config(
    page_title="Template Chatbot", page_icon="💬", layout="wide", initial_sidebar_state="expanded"
)
st.markdown(get_custom_css_modifier(), unsafe_allow_html=True)

st.markdown("<h5 style='text-align: left;'>💬 Template Chatbot</h5>", unsafe_allow_html=True)
st.title("Sophie's Diary")


# Display starting prompts only once before the chat starts
# if not st.session_state["starting_prompts_shown"]:
#     st.session_state["starting_prompts_shown"] = True
#     st.markdown(
#         "<div class='suggested-prompts'><h4>Suggested Prompts</h4></div>", unsafe_allow_html=True
#     )
#     for prompt in st.session_state["starting_prompts"].split("\n"):
#         if prompt.strip():
#             st.write(f"- {prompt}")


# Create a free text box. Let the user key in
# Allow the user to submit
# Once submit, allow user to dive deeper
# Then load up chatbox interface
with st.form(key='new_entry_form', clear_on_submit=False):
    new_entry_text = st.text_area(
        "What's on your mind?",
        "",
        key='new_entry_text'
    )

    new_entry_submit = st.form_submit_button(label='Submit')

if new_entry_submit and len(new_entry_text.strip()) == 0:
    st.error('Please key a new entry', icon="⚠️")
elif new_entry_submit:
    st.button(
        'Explore further',
        key='explore_further',
        on_click=enable_explore_further
    )

if st.session_state['explore_further_enabled']:

    chat_history_box = st.container()
    
    with chat_history_box:
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

    prompt = st.chat_input()
    if prompt:
        st.chat_message("user").write(prompt)

        response = chat_with_user(
            prompt,
            st.session_state['chat_model']
        )

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response})

        st.chat_message("assistant").write(response)
        st.rerun()
