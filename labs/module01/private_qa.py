"""Local embeddings, hosted generation. Retrieved text leaves the computer."""
import os
from pathlib import Path
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI

def build_engine():
    Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Settings.llm = OpenAI(model=os.environ["OPENAI_MODEL"], temperature=0)
    documents = SimpleDirectoryReader(str(Path(__file__).resolve().parents[1] / "data")).load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index.as_query_engine(similarity_top_k=2)

def answer(engine, question):
    if not question.strip():
        return "Please enter a question."
    if len(question) > 2000:
        return "Please shorten the question to 2,000 characters."
    response = engine.query("Use only the supplied course policies. Say you do not know if unsupported. " + question)
    sources = sorted({n.node.metadata.get("file_name", "unknown") for n in response.source_nodes})
    return f"{response}\n\nRetrieved files: {', '.join(sources)}"

if __name__ == "__main__":
    print(answer(build_engine(), "When can I request a refund?"))
