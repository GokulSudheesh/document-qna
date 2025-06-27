from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.prompts import PromptTemplate


def get_chat_prompt_template() -> ChatPromptTemplate:
    system_template = """ 
    - You are an assistant for question-answering tasks.
    - Use the following pieces of retrieved context and user information to answer the question. Please do not make up answers or answer out of context.
    - If the context is not sufficient to answer the question, then say "I don't have that information at hand. Please provide more details or check your sources.", this is very important.
    - If you don't find the answer of the query,then just say I don't have that information at hand. Please provide more details or check your sources.
    
    {context}
    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", system_template),
            MessagesPlaceholder(variable_name="messages"),
            ("human", "{user_input}")
        ])


session_name_prompt_template = PromptTemplate.from_template(
    """Generate a session name based on the following context: {context}. 
    The session name should be concise and relevant to the content of the context.
    Please keep the session name short, ideally no more than 5 words.""")
