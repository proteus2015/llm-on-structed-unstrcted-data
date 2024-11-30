# llm-on-structed-unstrcted-data
Provide a context-aware Large Language Model (LLM) end-to-end solution with Retrieval Augmented Generation (RAG) on data health and analysis for unstructured data and structured data. The solution

          - understands and analyses text data as well as numeric data
          - only answers enterprise specified data related questions
          - replies “No” if it doesn’t know from the specified data
          - structured data is any data Pandas Dataframe can handle (csv, excel, JSON, table, etc.)
          - unstructured data includes pdf, email, text, word and other non-tabular format data. In our test case we test on pdf file.
          - for unstructured data, Vectorizing with FAISS (Facebook Similarity Soluntion) is used to improve accuracy
          - Analysis results depend on internal enterprise data only (NO “general” results)
          - Results are updated when new data files are uploaded




