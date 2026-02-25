"""
Prompt templates.

Kept in a dedicated module so prompts can be versioned, A/B-tested, or
swapped without touching chain or node logic.
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

GENERATION_SYSTEM = (
    "You are a twitter techie influencer assistant tasked with writing excellent "
    "twitter posts. Generate the best twitter post possible for the user's request. "
    "If the user provides critique, respond with a revised version of your previous attempts."
)

REFLECTION_SYSTEM = (
    "You are a viral twitter influencer grading a tweet. Generate critique and "
    "recommendations for the user's tweet. Always provide detailed recommendations, "
    "including requests for length, virality, style, etc."
)

generation_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", GENERATION_SYSTEM),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", REFLECTION_SYSTEM),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
