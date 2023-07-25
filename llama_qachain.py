from langchain.document_loaders import DataFrameLoader
import pandas as pd
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# initialize the LLM & Embeddings
from langchain.llms import LlamaCpp
from langchain.embeddings import LlamaCppEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
llm = LlamaCpp(model_path="/Users/raunakpandey/Downloads/DD23/pinaka/app1/llama-7b/llama-7b.ggmlv3.q4_K_S.bin",n_batch=512,
    n_ctx=2048,
    f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
    callback_manager=callback_manager,
    verbose=True,
    temperature=0.0)
embeddings = LlamaCppEmbeddings(model_path="/Users/raunakpandey/Downloads/DD23/pinaka/app1/llama-7b/llama-7b.ggmlv3.q4_K_S.bin")

file_path = "/Users/raunakpandey/Downloads/DD23/pinaka/app1/utils/vault_d1/part.0.parquet"
df = pd.read_parquet(file_path)
# Function for pre-processing the content column
def preprocess_text(text):
    # Remove non-ASCII characters using regex
    processed_text = re.sub(r'[^\x00-\x7F]+', '', text)
    return processed_text
df['content'] = df['content'].apply(lambda x: preprocess_text(x))
loader = DataFrameLoader(df, page_content_column="content")
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 0)
all_splits = text_splitter.split_documents(df)
vectorstore = Chroma.from_documents(documents=all_splits,embedding=embeddings,persist_directory='/Users/raunakpandey/Downloads/DD23/pinaka/app1/working_folder/vstore')
qa_chain = RetrievalQA.from_chain_type(llm,retriever=vectorstore.as_retriever(),
                                       return_source_documents=True)

