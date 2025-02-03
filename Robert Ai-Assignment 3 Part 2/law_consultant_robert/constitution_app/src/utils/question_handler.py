from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.load import dumps, loads
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Multi-Query Prompt
multi_query_template = """You are an AI assistant. Generate five different versions of the user's question to improve document retrieval.
User question: {question}"""

prompt_perspectives = ChatPromptTemplate.from_template(multi_query_template)

def get_multi_queries(question):
    """Generate multiple reformulations of the query."""
    generate_queries = (
        prompt_perspectives
        | ChatOpenAI(temperature=0)
        | StrOutputParser()
        | (lambda x: x.split("\n"))
    )
    return generate_queries.invoke({"question": question})

# Reciprocal Rank Fusion (RRF)
def reciprocal_rank_fusion(results: list[list], k=60):
    """RRF for merging multi-query search results."""
    fused_scores = {}
    for docs in results:
        for rank, doc in enumerate(docs):
            doc_str = dumps(doc)
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0
            fused_scores[doc_str] += 1 / (rank + k)
    return [loads(doc) for doc, _ in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)]

def handle_question(query, retriever):
    """Enhanced retrieval using Multi-Query and RRF."""
    queries = get_multi_queries(query)
    retrieved_docs = [retriever.get_relevant_documents(q) for q in queries]
    reranked_docs = reciprocal_rank_fusion(retrieved_docs)
    return reranked_docs[:5]  # Return top 5 results

# Initialize Vectorstore
vectorstore = Chroma(embedding_function=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

def query_pipeline(query):
    """Query pipeline to retrieve and display responses."""
    return handle_question(query, retriever)
