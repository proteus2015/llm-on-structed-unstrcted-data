from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI

import os
import openai
import uuid

import pandas as pd
import streamlit as sl

## Text Splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

## Pdf Loader
from langchain_community.document_loaders import PyPDFLoader

## import FAISS
from langchain_community.vectorstores import FAISS

from langchain_openai import OpenAIEmbeddings

def get_unique_id():
    return str(uuid.uuid4())


## Split the pages / text into chunks
def split_text(filePageDict, chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    rtnSplittedDict ={}
    for fileName in filePageDict.keys():
        docs = text_splitter.split_documents(filePageDict.get(fileName))
        rtnSplittedDict[fileName]=docs
    return rtnSplittedDict


## create vector store, or add documents in existing vector store
    #    docDict: Dictionary {"uploadedFile name", [splitted documents list]}
    #    return: True or False

def create_or_add_vector_store(request_id, docDict):


    embeddings = OpenAIEmbeddings()  # embeddings object creation
    # Load the vector store
    try:
        vector_store = FAISS.load_local(folder_path="./vectorstore",embeddings=embeddings, index_name = "pdfIndex", allow_dangerous_deserialization=True)
        sl.write('============Start adding documents to an existing FAISS vector store============')
        '''If there has been existing FAISS vector store, we add split documents into it. 
        Each slit document while have (fileName+ split index of the document) as id for future update/delete '''
        for key in docDict:
             docs = docDict[key]
             rtn_ids= vector_store.add_documents(documents=docs, ids=[key+str(docs.index(x)) for x in docs])
             #sl.write(f"ids stored to vector: {rtn_ids}")
             vector_store.save_local(folder_path="./vectorstore",index_name = "pdfIndex")
        sl.write('============End adding documents to an existing FAISS vector store============')

    except RuntimeError:
            sl.write('============Start creating a new FAISS vector store ============')

            for key in docDict:
                docs = docDict[key]
                db = FAISS.from_documents(documents=docs, embedding=embeddings,
                                          ids=[key + str(docs.index(x)) for x in docs])  # data base creation

            '''If there is no vector being created, we create a new FAISS vector store, and
            add split documents into it. Each slit document while have (fileName+ split index of the document) 
            as id for future update/delete'''
            db.save_local(folder_path="./vectorstore", index_name="pdfIndex")
            sl.write('============End creating a new FAISS vector store successfully!============')

    return True


#sl.write("my fist streamlit app")


my_openai_api_key = os.getenv("OPENAI_API_KEY")
print("openAI key is correct")

df_base = pd.read_csv ("./data/tela_history_data.csv")
llm = ChatOpenAI(
temperature=0, model="gpt-3.5-turbo", openai_api_key=my_openai_api_key, streaming=True
)


def main():
    list_df = []
    sl.markdown(":blossom::blossom:**Load pdf files for langchain analysis** -")
    # sl.write("Load pdf files for langchain analysis")
    uploaded_files = sl.file_uploader("Choose pdf file(s)", type=["pdf"], accept_multiple_files=True)
    if len(uploaded_files)>0:
        sl.write("you have uploaded pdf files - ")
        fileDict={}
        request_id = get_unique_id()
        sl.write(f"Request Id: {request_id}")
        total_pages = []
        total_page_number =0
        for single_file in uploaded_files:
            sl.write(f"File name: {single_file.name}")
            saved_file_name = f"{request_id}{single_file.name}"
            with open(saved_file_name, mode="wb") as w:
                w.write(single_file.getvalue())

            loader = PyPDFLoader(saved_file_name)
            pages = loader.load_and_split()
            total_pages.extend(pages)
            total_page_number=total_page_number+len(total_pages)
            sl.write(f"total page numbers so far is: {total_page_number}")
            fileDict[single_file.name]=total_pages

        if len(fileDict) > 0:
            ## Split Text
            splitted_docDict = split_text(fileDict, 1000, 200)
            sl.write(f"Splitted Doc length: {total_page_number}")
            sl.write("=====================Splitted page 0 as an example:====================")
            for key in splitted_docDict.keys():
                 sl.write(splitted_docDict[key][0])

            #create vector store, or add documents in existing vector store
            result = create_or_add_vector_store(request_id, splitted_docDict)

            if result:
                sl.write("Succeed on PDF vectorizing - PDF processed successfully")
            else:
                sl.write("Error on PDF vectorizing - please check errors in log.")


    sl.markdown(":sunflower::sunflower:**Load csv files for langchain analysis** -")
    # sl.write("Load pdf files for langchain analysis")
    uploaded_files_2 = sl.file_uploader("Choose 1 or 2 csv file(s)", type=["csv"], accept_multiple_files=True)
    if len(uploaded_files_2) ==1:
        sl.write("you have uploaded 1 csv file - ")
        sl.write(f"single_file: {uploaded_files_2[0].name}")
        df1 = pd.read_csv(uploaded_files_2[0])
        sl.write(df1.head(5))
        sl.write(f"dataframe size: {len(df1)}")

        custom_prompt = """
          Use pandas DataFrame methods to answer the user's question. If necessary, convert text column to numeric column. If you don't know the answer, just say that you don't know, don't try to make up an answer
          """

        pandas_df_agent = create_pandas_dataframe_agent(
                llm,
                df1,
                verbose=True,
                agent_type=AgentType.OPENAI_FUNCTIONS,
               # handle_parsing_errors=True,
                prefix=custom_prompt,
                allow_dangerous_code=True
        )

    if len(uploaded_files_2) == 2:
        sl.write("you have uploaded 2 csv files - ")
        sl.write(f"file 1: {uploaded_files_2[0].name}")
        df1 = pd.read_csv(uploaded_files_2[0])
        df2 = pd.read_csv(uploaded_files_2[1])
        sl.write(df1.head(5))
        sl.write(f"dataframe df1 size: {len(df1)}")
        sl.write(df2.head(5))
        sl.write(f"dataframe df2 size: {len(df2)}")

            #     list_df.append(df)
            #     sl.write(df.head(5))
            #     sl.write(f"dataframe size in list: {len(list_df[0])}")
            #     sl.write(f"dataframe size: {len(df)}")

            # for single_file in uploaded_files_2:
            #     sl.write(f"single_file: {single_file.name}")
            #     df = pd.read_csv(single_file)
            #     list_df.append(df)
            #     sl.write(df.head(5))
            #     sl.write(f"dataframe size in list: {len(list_df[0])}")
            #     sl.write(f"dataframe size: {len(df)}")
            # Create your custom prompt
        custom_prompt = """
             Strategy: Use pandas DataFrame methods to answer the user's question. If necessary, convert text column to numeric column. If you don't know the answer, just say that you don't know, don't try to make up an answer
         """

        pandas_df_agent = create_pandas_dataframe_agent(
                llm,
                [df1,df2],
                verbose=True,
                agent_type=AgentType.OPENAI_FUNCTIONS,
                # handle_parsing_errors=True,
                prefix=custom_prompt,
                allow_dangerous_code=True
        )

    question = sl.text_input("Input your question")
    if sl.button("Submit"):
       with sl.spinner("Querying..."):
            result_on_csv = pandas_df_agent.invoke(question)
            sl.write(result_on_csv)
            sl.success("Complete")

if __name__ == "__main__":
    main()
