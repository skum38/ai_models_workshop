#pip install -U langchain langchain-openai
#LangChain split providers into separate packages to reduce bloat.

import os
from langchain_openai import OpenAIEmbeddings
os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"
openaiEmbeddings = OpenAIEmbeddings()
openaitextEmbeddings = openaiEmbeddings.embed_query("Hi")
print(len(openaitextEmbeddings))

#Using huggingface Sentence Transformers instead (local, no API)
from langchain_huggingface import HuggingFaceEmbeddings
huggingFaceEmbeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
textEmbeddings = huggingFaceEmbeddings.embed_query("Hi")
print(len(textEmbeddings))

#Using FAISS vector store to store and query embeddings
from langchain_community.vectorstores import FAISS 

texts=[ "Customer support helps users solve problems",
    "Greetings are used to start conversations"]
huggingFaceEmbeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create a FAISS vector store from the embeddings
vectorStore = FAISS.from_texts(texts, huggingFaceEmbeddings)
vectorStore.save_local("my_vectordb")   

# Query the vector store
query = "Hello"
results = vectorStore.similarity_search(query)
for doc in results:
    print(doc.page_content)


results = vectorStore.similarity_search_with_score(query)

for doc, score in results:
    print(f"Text: {doc.page_content}, Score: {score}")
