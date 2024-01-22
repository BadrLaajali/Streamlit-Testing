import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage, #Tell the LLM what our assistant is suppose to be
    HumanMessage, #Message that the user will send to the LLM
    AIMessage #The response from the LLM
)

def init():
    # Load the OpenAI API key from the environment variable
    load_dotenv()

    # test that the API key exists
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    # setup streamlit page
    st.set_page_config(
        page_title="Your own ChatGPT",
        page_icon="🤖",
        layout="wide"
    )

def clear_text():
    #On fait un swap de user_text saisie par l'utilisateur et l'affecte a user_input pour pouvoir clearer
    st.session_state.user_input = st.session_state.user_text
    st.session_state.user_text = ""

def main():
    #Appeler la fonction init
    init()   
    
    #Crée un header pour notre page
    st.header("Your own ChatGPT 🤖")

    #Create chat object 
    chat = ChatOpenAI(temperature=0.5)

    #Check if the variable messages is not initialised inside the current session
    if 'messages' not in st.session_state:
        #Define the message for the session in a list[] starting with systemmessage 
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]

    #First message
    message("Bonjour, je suis votre assistant, merci de me fournir votre prénom pour que je puisse personnalise ma conversation avec vous", is_user=False)

    # sidebar with user input
    with st.sidebar:
        #On crée la zone texte (text_input) ou l'utilisateur saisie son message
        #La key stock l'identifiant du champ texte
        st.text_input("Your message: ", key="user_text", on_change=clear_text)
        #On récupere la valeur stocker dans user_input, si user_input n'existe pas on retourne vide ''
        user_input = st.session_state.get('user_input', '')

    # handle user input
    if user_input:
        #Add in the list messages created above the user message
        st.session_state.messages.append(HumanMessage(content=user_input))
        #Add a spinner before the response send to make it like he is thinking
        with st.spinner("Thinking"):    
            #Send the list messages to openai via chat object and store the result in response variable
            response = chat(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))
    
    
            

    # display message history
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            #Showing the input that user send in FE
            message(msg.content, is_user=True, key=str(i) + '_user')
        else:
            #Show the response received from the LLM in FE
            message(msg.content, is_user=False, key=str(i) + '_ai')



# s'assurer que certaines parties du code ne soient exécutées que lorsqu'un script est lancé directement, et non lorsqu'il est importé en tant que module dans un autre script.
if __name__ == '__main__':
    main()