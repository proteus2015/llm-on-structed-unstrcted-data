# llm-on-structed-unstrcted-data
Provide a context-aware Large Language Model (LLM) end-to-end solution with Retrieval Augmented Generation (RAG) on data health and analysis for unstructured data and structured data. The solution (implemented in Python with Langchain, Streamlit, and other tools you need (I will cover in mext project)

          - understands and analyses text data as well as numeric data
          - only answers enterprise specified data related questions
          - replies “No” if it doesn’t know from the specified data
          - structured data is any data Pandas Dataframe can handle (csv, excel, JSON, table, etc.)
          - unstructured data includes pdf, email, text, word and other non-tabular format data. In our test case we test on pdf file.
          - for unstructured data, Vectorizing with FAISS (Facebook Similarity Soluntion) is used to improve accuracy
          - Analysis results depend on internal enterprise data only (NO “general” results)
          - Results are updated when new data files are uploaded
          - I use https://platform.openai.com/ for OpenAI support, but can change to other OpenAI supporter (AWS Bedrock, Databricks dataiku, etc.)

Architecture:

![image](https://github.com/user-attachments/assets/b4d20b98-12ca-4225-b1bf-b33cba572a5f)

Packages and condistions needed:
1. creat an account and an OpenAI api key in (https://platform.openai.com/api-keys) , and save they key in your local environment with name OPENAI_API_KEY. In the code, the key will be retrieved like this:

    import os
   
    my_openai_api_key = os.getenv("OPENAI_API_KEY")

    from langchain_openai import ChatOpenAI
   
    llm = ChatOpenAI(
          temperature=0, model="gpt-3.5-turbo", openai_api_key=my_openai_api_key, streaming=True
   )
   
3. go to Openai your profile/billing, and deposit money there. Each OpenAI call costs ~1 cent in my case (with 10M data maximum), so I only deposited $10 there.
   
4. Install necessary packages

   pip install langchain   
   pip install streamlit   
   pip install pandas
   
5. How to run:
   5.1 For csv and any structured data pandas can process, you only need to run dataset.server under folder vectoring, for example, in pycharm Terminal (community version is good enough):
       cd vectorizing
       streamlit run .\dataset-server.py

   a new URL will pop up. Current codes support upload 1 to 2 csv files; then raise questions on the uploaded files in the same URL. An example is shown below:

     ![image](https://github.com/user-attachments/assets/c495570d-864c-44a1-b342-4385baec0f48)

              

