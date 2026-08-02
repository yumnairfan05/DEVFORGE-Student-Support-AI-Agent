import os
import requests
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate

from main.rag import retrieve_context

# ---------------------------------
# Load Environment Variables
# ---------------------------------
load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMAAPIKEY")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gpt-oss:20b")

OLLAMA_URL = "https://ollama.com/api/chat"


print("=" * 50)
print("API KEY LOADED:", OLLAMA_API_KEY is not None)
print("MODEL LOADED:", OLLAMA_MODEL)
print("=" * 50)


# ---------------------------------
# LangGraph State
# ---------------------------------
class AgentState(TypedDict):
    question: str
    category: str
    answer: str


# ---------------------------------
# Node 1 - Question Classification
# ---------------------------------
def classify_question(state: AgentState):

    question = state["question"].lower()

    keywords = [
        "python",
        "fastapi",
        "langchain",
        "langgraph",
        "github",
        "render",
        "deployment",
        "deploy",
        "ai",
        "agent",
        "devforge",
        "assignment",
        "project",
        "internship",
        "ollama",
        "api",
        "machine learning",
        "rag",
        "chatbot",
        "web development",
        "technical",
        "programming",
    ]

    if any(keyword in question for keyword in keywords):
        state["category"] = "related"
    else:
        state["category"] = "unrelated"

    return state


# ---------------------------------
# Node 2 - AI Support + RAG
# ---------------------------------
def ai_support(state: AgentState):

    try:

        # Check API key
        if not OLLAMA_API_KEY:
            state["answer"] = (
                "Error: Ollama Cloud API key is not configured."
            )
            return state

        # Retrieve relevant knowledge
        context = retrieve_context(
            state["question"]
        )

        # Build LangChain prompt
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are the DEVFORGE Student Support AI Agent.

You help DEVFORGE internship students with:
- AI Engineering
- Web Development
- Python
- FastAPI
- LangChain
- LangGraph
- GitHub
- Render deployment
- Student assignments
- Project guidance
- DEVFORGE internship learning support

Rules:
1. Use ONLY the provided knowledge base.
2. Do not invent information.
3. Give clear and helpful answers.
4. If the answer is not in the knowledge base, say:

"I couldn't find that information in the DEVFORGE knowledge base."

5. Do not answer unrelated questions.
"""
                ),
                (
                    "human",
                    """
Knowledge Base:

{context}

----------------------------------------

Student Question:

{question}

----------------------------------------

Answer ONLY using the knowledge base above.
"""
                ),
            ]
        )

        # Create LangChain messages
        messages = prompt_template.format_messages(
            context=context,
            question=state["question"]
        )

        # Convert LangChain message roles to Ollama roles
        ollama_messages = []

        for message in messages:

            if message.type == "system":
                role = "system"
            elif message.type == "human":
                role = "user"
            elif message.type == "ai":
                role = "assistant"
            else:
                role = "user"

            ollama_messages.append(
                {
                    "role": role,
                    "content": str(message.content)
                }
            )

        # Request to Ollama Cloud
        headers = {
            "Authorization": f"Bearer {OLLAMA_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": OLLAMA_MODEL,
            "messages": ollama_messages,
            "stream": False
        }

        response = requests.post(
            OLLAMA_URL,
            headers=headers,
            json=data,
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        answer = result.get(
            "message",
            {}
        ).get(
            "content",
            ""
        )

        if answer:
            state["answer"] = answer
        else:
            state["answer"] = (
                "The Ollama Cloud model returned an empty response."
            )

    except requests.exceptions.Timeout:

        state["answer"] = (
            "The Ollama Cloud request timed out. Please try again."
        )

    except requests.exceptions.HTTPError as e:

        state["answer"] = (
            f"Ollama Cloud API error: {str(e)}"
        )

    except requests.exceptions.RequestException as e:

        state["answer"] = (
            f"Network error while connecting to Ollama Cloud: {str(e)}"
        )

    except Exception as e:

        state["answer"] = (
            f"Error processing your request: {str(e)}"
        )

    return state


# ---------------------------------
# Node 3 - Safe Response
# ---------------------------------
def safe_response(state: AgentState):

    state["answer"] = (
        "I'm sorry, but I can only answer questions related to "
        "DEVFORGE learning, AI Engineering, Web Development, "
        "Python, FastAPI, LangChain, LangGraph, GitHub, "
        "RAG systems, deployment, assignments, projects, "
        "and internship guidance."
    )

    return state


# ---------------------------------
# Router
# ---------------------------------
def route_question(state: AgentState):

    if state["category"] == "related":
        return "ai_support"

    return "safe_response"


# ---------------------------------
# Build LangGraph Workflow
# ---------------------------------
graph = StateGraph(AgentState)

graph.add_node(
    "classify_question",
    classify_question
)

graph.add_node(
    "ai_support",
    ai_support
)

graph.add_node(
    "safe_response",
    safe_response
)

graph.set_entry_point(
    "classify_question"
)

graph.add_conditional_edges(
    "classify_question",
    route_question,
    {
        "ai_support": "ai_support",
        "safe_response": "safe_response",
    }
)

graph.add_edge(
    "ai_support",
    END
)

graph.add_edge(
    "safe_response",
    END
)


# ---------------------------------
# Compile Agent
# ---------------------------------
agent = graph.compile()