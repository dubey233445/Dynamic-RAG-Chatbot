from src.ingest import get_vectorstore
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
# We'll use a dummy LLM or a simple logic if no key is provided.
# For a real demo, we'd need an LLM. 
# I'll use a FakeLLM for demonstration purposes so it runs without keys, 
# but structurally it's ready for OpenAI/Gemini.
from langchain_community.llms import FakeListLLM

class Chatbot:
    def __init__(self):
        self.vectorstore = get_vectorstore()
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        
        # Setup a fake LLM that just echoes or gives a standard answer for this demo
        # In production, replace with: from langchain_openai import ChatOpenAI
        self.llm = FakeListLLM(responses=["Expected Response: Based on the knowledge base, I found relevant info."])
        
        template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
        self.prompt = PromptTemplate.from_template(template)
        
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(self, query: str):
        # For the demo, let's also print the retrieved docs so we can PROVE it found the new info
        docs = self.retriever.invoke(query)
        if docs:
            print(f"\n[Debug] Found {len(docs)} relevant documents:")
            for d in docs:
                print(f" - {d.page_content[:100]}...")
        else:
            print("\n[Debug] No relevant documents found.")
            
        # Run the chain (even if mock)
        return self.chain.invoke(query)
