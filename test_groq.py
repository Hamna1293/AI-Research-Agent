from app.rag.llm import LLM

llm = LLM()

response = llm.generate(
    "Explain attention mechanism in one paragraph."
)

print(response)