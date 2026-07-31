from agent import agent

result = agent.invoke({
    "question": "How do I deploy a FastAPI project on Render?",
    "category": "",
    "answer": ""
})

print(result["answer"])
