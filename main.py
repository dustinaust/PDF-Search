from utils import load_documents
from utils import converter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
import sys


# Set up API
OPEN_API_KEY = " "
os.environ["OPENAI_API_KEY"] = OPEN_API_KEY

# Catch user query
query_text = " ".join(sys.argv[1:])


path_to_md = "Markdowns/"
path_to_pdf = "DatasetPDF/"

# If the md directory has been created set this to false
create_data = False

if create_data == True:
    converter(path_to_pdf = path_to_pdf, path_to_md = path_to_md)

documents = load_documents(path_to_md)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=500,
    length_function=len,
    add_start_index=True
)

# Split text into chunks and save in chromadb
chunks = text_splitter.split_documents(documents)

path_to_chroma = "Chroma/"
db = Chroma.from_documents(
    chunks, OpenAIEmbeddings(openai_api_key=OPEN_API_KEY), persist_directory=path_to_chroma)

embedding_function = OpenAIEmbeddings()
db = Chroma(persist_directory=path_to_chroma, embedding_function=embedding_function)

# Search for chunks matching users query
results = db.similarity_search_with_relevance_scores(query_text, k=40)

PROMPT_TEMPLATE = """
Beantworte die Frage nur anhand des folgenden Kontextes: {context}

---

Beantworte die Frage ausschließlich anhand des oberen Kontextes: {question}
"""

context_text = "n\n---\n\n".join([doc.page_content for doc, _score in results])
prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
prompt = prompt_template.format(context=context_text, question=query_text)

model = ChatOpenAI()

response_text = model.invoke(prompt)

print(response_text)
