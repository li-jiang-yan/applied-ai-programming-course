import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages([
    ("system", "Explain the topic in exactly three short bullet points for {audience}."),
    ("human", "{topic}"),
])
model = ChatOpenAI(model=os.environ["OPENAI_MODEL"], timeout=45, max_retries=2)
chain = prompt | model | StrOutputParser()

if __name__ == "__main__":
    print(chain.invoke({"audience": "new Python programmers", "topic": "dictionaries"}))
