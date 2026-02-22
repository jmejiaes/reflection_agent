from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# Se definen los prompts que se van a usar para los nodos de llms
reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a viral twitter influencer grading a tweet. Generate critique and recommendations for the user's tweet."
            "Always provide detailed recommendations, including requests for length, virality, style, etc.",
        ),
        MessagesPlaceholder(
            variable_name="messages"
        ),  # Se pone este placeholder para que se inserten los mensajes que se quiere que se tengan en cuenta en el historial
    ]
)

generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a twitter techie influencer assistant tasked with writing excellent twitter posts."
            " Generate the best twitter post possible for the user's request."
            " If the user provides critique, respond with a revised version of your previous attempts.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

llm = ChatOpenAI(model='gpt-3.5-turbo')

# Se definen los chains que facilitaran la invocacion de los llms para tareas especificas de ciertos nodos.
generate_chain = generation_prompt | llm
reflect_chain = reflection_prompt | llm
