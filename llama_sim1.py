# Bring in deps
from langchain.llms import LlamaCpp
from langchain.embeddings import LlamaCppEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

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

# Read input text from the user
content = input("Enter the text: ")

# Write input text to a temporary file
file_path = "file1.txt"
write_text_file(content, file_path)

# Load the text from the file
loader = TextLoader(file_path)
docs = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
texts = text_splitter.split_documents(docs)
db = Chroma.from_documents(texts, embeddings)

# Prompt the user to ask questions
while True:
    question = input("Ask a question (or 'q' to quit): ")
    if question.lower() == 'q':
        break
    
    similar_doc = db.similarity_search(question, k=1)
    context = similar_doc[0].page_content
    query_llm = LLMChain(llm=llm, prompt=prompt)
    response = query_llm.run({"context": context, "question": question})
    print(response)
