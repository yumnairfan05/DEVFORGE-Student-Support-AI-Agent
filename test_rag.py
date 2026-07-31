from rag import retrieve_context


question = "How can I deploy my FastAPI project?"


context = retrieve_context(question)


print("Retrieved Context:")
print("------------------")
print(context)