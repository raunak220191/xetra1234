# Bring in deps
from langchain.llms import LlamaCpp
from langchain.embeddings import LlamaCppEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
import pandas as pd
import re

# function for writing input text to a file
def write_text_file(content, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Error occurred while writing the file: {e}")
        return False

  # set prompt template
prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
{context}
Question: {question}
Answer:"""
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# initialize the LLM & Embeddings
llm = LlamaCpp(model_path="/Users/raunakpandey/Downloads/DD23/pinaka/app1/llama-7b/llama-7b.ggmlv3.q4_K_S.bin")
embeddings = LlamaCppEmbeddings(model_path="/Users/raunakpandey/Downloads/DD23/pinaka/app1/llama-7b/llama-7b.ggmlv3.q4_K_S.bin")
llm_chain = LLMChain(llm=llm, prompt=prompt)

# Read input text from the user (In this case, we will use a sample Parquet file)
file_path = "/Users/raunakpandey/Downloads/DD23/pinaka/app1/utils/vault_d1/part.0.parquet"
data = pd.read_parquet(file_path)

# Function for pre-processing the content column
def preprocess_text(text):
    # Remove non-ASCII characters using regex
    processed_text = re.sub(r'[^\x00-\x7F]+', '', text)
    return processed_text
data = data[data["content"].str.len()> 100]
len(data)
data['content'] = data['content'].apply(lambda x: preprocess_text(x))

# Document class to hold content and filename
class Document:
    def __init__(self, content, filename,metadata=None):
        self.page_content = content
        self.filename = filename
        self.metadata = metadata
documents = [Document(content, filename, metadata={"filename": filename}) for content, filename in zip(data["content"].tolist(), data["filename"].tolist())]

# Split the input text into chunks of 1024 characters
text_splitter = CharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

texts = [doc.page_content for doc in texts]

# Split the text into chunks of 1024 tokens
def split_text_into_chunks(text, chunk_size=1024):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    return chunks

# Embed each chunk using LlamaCppEmbeddings
def embed_text_chunks(chunks, embeddings):
    return [embeddings.embed_documents(chunk) for chunk in chunks]

# Combine the embeddings of all chunks into a single list
def flatten_embedded_chunks(embedded_chunks):
    return [val for sublist in embedded_chunks for val in sublist]

# Create ChromaDB and link it to the filename column
def create_chroma_db(texts, embeddings):
    chunked_texts = [split_text_into_chunks(text) for text in texts]
    embedded_chunks = [embed_text_chunks(chunks, embeddings) for chunks in chunked_texts]
    flattened_embeddings = [flatten_embedded_chunks(chunks) for chunks in embedded_chunks]
    metadatas = [{"filename": filename} for filename in filenames]
    db = Chroma.from_documents(flattened_embeddings, metadatas=metadatas)
    return db

# Call the function to create ChromaDB
db = create_chroma_db(texts, embeddings)
