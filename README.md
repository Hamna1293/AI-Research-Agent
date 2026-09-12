# AI Research Agent

A retrieval-augmented chatbot that lets you upload any research paper and ask questions about it in natural language — with answers grounded in the paper's actual content, plus quick short-form Q&A extraction for fast insight retrieval.

## How it works
- Ingests an uploaded PDF/research paper and splits it into chunks
- Embeds chunks into a **ChromaDB** vector store
- Retrieves the most relevant chunks for a given question
- Uses the **OpenAI API** to generate an answer grounded in retrieved context

## Tech Stack
- Python
- OpenAI API
- ChromaDB (vector database)

## Example
> **Q:** What dataset did this paper use for evaluation?
> **A:** [ output here]

## Status
Actively used as a portfolio/demo project. 
