# Semantic Search Engine For Wikipedia Articles

A high-performance, containerized semantic search engine built to recommend contextually relevant Wikipedia "Level 5 Vital Articles" based on natural language queries.

## Features
- Context-Aware Search: Goes beyond keyword matching by using Sentence Transformers (all−MiniLM−L6−v2) to understand the intent and context of the user query.
- Fast Retrieval: Leverages FAISS (Facebook AI Similarity Search) to build an efficient vector index, enabling lightning-fast k−nearest neighbor lookups for millions of potential articles.
- Production Ready: Packaged as a lightweight Docker container and served by a high-performance FastAPI web API.
- Data Source: Indexed content is sourced from the HuggingFace datasets library, specifically targeting a curated list of vital Wikipedia articles.
- Persistence: The FAISS index and metadata are saved to disk, allowing for rapid application restarts without re-indexing.

## Setup
1. Clone the repository 
```bash
git clone https://github.com/00AR/semantic_search_engine.git
```
2. Spin the docker container
```bash
cd semantic_search_engine/
docker compose up --build
```
3. On the browser go to `http://0.0.0.0:7860/` to search for articles
**NOTE**: The above command will also build the embeddigs for 50000+ articles(can take hours if GPU is not available), so it is better for you to use the deployed application, if you just want to test.

## How It Works
1. Indexing: The SemanticIndex class loads text from the Wikipedia dataset, converts the title and initial text into a dense vector embedding using the all−MiniLM−L6−v2 model, and adds these vectors to a FAISS IndexFlatL2. The index is then persisted to disk.
2. Querying: A user query is received by the FastAPI endpoint.
3. Vector Search: The query text is encoded into a vector embedding, which is then passed to the FAISS index to find the top k nearest item vectors.
4. Results: The system returns the title, URL, and a calculated similarity score for the most relevant articles

# Tech Stack Used
|Component|	Technology|	Role|
|--|--|--|
|Search/Indexing|	FAISS	|Efficient vector similarity search|
|Embeddings	|Sentence Transformers (all−MiniLM−L6−v2)	|Semantic understanding and vector creation|
|Web Framework	| FastAPI	|Serving the search API and Jinja2 templates|
|Containerization|	Docker	|Packaging and deployment|
|Data Source	|HuggingFace datasets	|Loading and processing Wikipedia data|