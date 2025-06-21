from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def get_chat_prompt_template() -> ChatPromptTemplate:
    system_template = """ 
    - You are an assistant for question-answering tasks.
    - Use the following pieces of retrieved context and user information to answer the question. Please do not make up answers or answer out of context.
    - If you don't find the answer of the query,then just say I don't have that information at hand. Please provide more details or check your sources.
    
    {context}
    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", system_template),
            MessagesPlaceholder(variable_name="messages"),
            ("human", "{user_input}")
        ])
