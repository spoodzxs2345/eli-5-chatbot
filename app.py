import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets['API_KEY'])

st.set_page_config(page_title='Eli-5 Chatbot', page_icon='🤖')

st.title('Eli-5 Chatbot 🧒🤖')

with st.sidebar:
    st.info('Disclaimer\n\nEli-5 is made for educational and entertainment purposes only. Information generated by Eli-5 may not be up-to-date, and should not be taken as an advice.', icon='ℹ️')

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]

system_instruction = "Ignore previous instructions. Explain Like I'm Five the user prompt. Give me a playful and informative answer using emojis for emphasis! Skip the introduction and get straight to the point. Write the whole response in markdown format. The response should be divided into 3 paragraphs. Do not include headers"

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            'role': 'assistant',
            'content': 'Hi! I am Eli-5 Chatbot. 👋 I can help you understand complex topics in a simple way. 📖 Ask me anything! 🧒🤖'
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

examples = ['Explain how neural networks work.', 'What is AI?', 'Why do I get hiccups?']
example_buttons = [st.button(example) for example in examples]

query = st.chat_input('What are black holes?')
for example, example_button in zip(examples, example_buttons):
    if example_button:
        query = example

def chatbot_function(query):
    response = model.generate_content(query)

    with st.chat_message('assistant'):
        st.markdown(response.text)
    
    
    st.session_state.messages.append(
        {
            'role': 'user',
            'content': query
        }
    )

    st.session_state.messages.append(
        {
            'role': 'assistant',
            'content': response.text
        }
    )

if query:
    response = model.generate_content(query)

    with st.chat_message('user'):
        st.markdown(query)
            
    with st.spinner('Thinking...'):
        chatbot_function(query)
