from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langgraph.prebuilt import create_react_agent
from db import retriever
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

llm = ChatGroq(
    model='llama-3.3-70b-versatile',
    
    temperature=0.2
)

search_tool = DuckDuckGoSearchRun()

@tool
def search_content(query: str) -> str:
    """Searches the web for the query and returns a concise answer"""
    return search_tool.run(query)


parser = StrOutputParser()

prompt = PromptTemplate(
    template="""
    You are a helpful UPSC preparation assistant.
    Answer ONLY from the provided UPSC PDF context.
    If the context is insufficient, say: "I don't know, sorry."
    Add a relevant emoji at the end.

    Context: {context}
    Question: {question}
    """,
    input_variables=['context', 'question']
)

def format_docs(docs):
    return '\n\n'.join(doc.page_content for doc in docs)

chain = (
    RunnableParallel({
        'context': retriever | format_docs,
        'question': RunnablePassthrough()
    })
    | prompt
    | llm
    | parser
)

# NEW: Convert RAG into a tool
@tool
def upsc_rag_tool(query: str) -> str:
    """Answer UPSC-related questions from local PDF knowledge base"""
    return chain.invoke(query)

@tool
def current_time() -> str:
    """Returns the current date and time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# CHANGED: Added RAG tool inside agent
agent = create_react_agent(
    llm,
    tools=[search_content, upsc_rag_tool, current_time]
)


response = agent.invoke({
    "messages": [
        ("user", "Explain fundamental rights in India and who is their author?")
    ]
})

# CHANGED: Proper output extraction
print(response["messages"][-1].content)

# NEW: Clean interface for reuse
def ask_question(query: str):
    result = agent.invoke({
        "messages": [("user", query)]
    })
    return result["messages"][-1].content