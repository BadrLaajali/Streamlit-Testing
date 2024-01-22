from dotenv import load_dotenv
import os
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage, #Tell the LLM what our assistant is suppose to be
    HumanMessage, #Message that the user will send to the LLM
    AIMessage #The response from the LLM
)
from langchain.chains import create_extraction_chain


def init():
    # Load the OpenAI API key from the environment variable
    load_dotenv()

    # test that the API key exists
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")
    
    llm = OpenAI(model_name='text-davinci-003',
             temperature=0,
             max_tokens = 256)

def main():

    init()

    # Schema
    schema = {
        "properties": {
            "nom": {"type": "string"},
            "service": {"type": "integer"},
            "city": {"type": "string"},
            "date_start": {"type": "string"},
            "date_end": {"type": "string"},
            "details": {"type": "string"},
        }
    }

    #Ici on déclara un dictionnaire clé valeur
    conversation_state = {
        "step": "ask_name",
        "name": "",
        "service": "",
        "city": "",
        "date_start": "",
        "date_end": "",
        "details": ""
    }

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    chain = create_extraction_chain(schema, llm)
    messages = []

    if conversation_state["step"] == "ask_name":
        #Ici LLM pour demander le nom du user et ne passer à aucune étape sans le nom
        #Le user pourra poser des questions mais le LLM lui expliquera qu'il ne peux pas demarrer la conversation sans le nom
        messages = [
            SystemMessage(content="""Tu es un assistant virtuel spécialisé dans la réservation d'hôtels. Ton rôle est d'aider les utilisateurs à trouver et réserver l'hôtel idéal pour leurs besoins. Avant de répondre à leurs questions sur les hôtels ou de procéder à une réservation, il est essentiel que tu demandes le nom de l'utilisateur. Cette étape est cruciale pour personnaliser la conversation et offrir une expérience utilisateur optimale. Tu dois rester courtois et professionnel en tout temps, même si les utilisateurs ne fournissent pas immédiatement leur nom. Ton objectif principal est de les guider à travers le processus de réservation tout en veillant à personnaliser l'interaction. Rappelle-toi que tu ne peux pas poursuivre avec des suggestions ou des réservations spécifiques sans connaître le nom de l'utilisateur. Si un utilisateur pose des questions sans fournir son nom, réponds poliment en lui rappelant l'importance de cette information pour personnaliser le service.""")
        ]
        message = input("Bonour je suis votre assistant virtuel, merci de saisir votre nom :")
        usr_msg = HumanMessage(content=message)
        messages.append(usr_msg)
        ai_msg = llm(messages)
        print(chain.run(ai_msg.content))

        user_name = "user name"
        if user_name:
            conversation_state = {
            "step": "ask_service",
            "name": user_name,
            "service": "",
            "city": "",
            "date_start": "",
            "date_end": "",
            "details": ""
            }
    elif conversation_state["step"] == "ask_service":
        '''
        Ici LLM pour demander le choix du service l'utilisateur pourra poser d'autres questions, 
        le LLM va répondre mais toujours lui demander à la fin de la réponse de choisir un service.
        Voici les choix : 
        1. Faire une réservation
        2. Annuler une réservation
        3. Contacter le support
        Si le LLM detecte que le user à donner une ville sur le premier choix ainsi que des dates il doit les save
        '''
        service_choice = "Service Choice"
        city_choice = "City Choice"
        date_start = "Date start"
        date_end = "Date fin"
        
        if service_choice and not city_choice and not date_start and not date_end:
            conversation_state = {
            "step": "ask_city",
            "name": user_name,
            "service": service_choice,
            "city": "",
            "date_start": "",
            "date_end": "",
            "details": ""
            }
        #Ici on vérifie que les deux variables sont rempli
        elif service_choice and city_choice and not date_start and not date_end:
            conversation_state = {
            "step": "ask_date",
            "name": user_name,
            "service": service_choice,
            "city": city_choice,
            "date_start": "",
            "date_end": "",
            "details": ""
            }
        elif service_choice and city_choice and date_start and date_end :
            conversation_state = {
            "step": "ask_details",
            "name": user_name,
            "service": service_choice,
            "city": city_choice,
            "date_start": date_start,
            "date_end": date_end,
            "details": ""
            }

    #for key, value in conversation_state.items():
        #print(f"{key}: {value}")


if __name__ == "__main__":
    main()
