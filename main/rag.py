import re


KB_PATH = "knowledge_base/devforge.md"


def load_documents():
    """
    Load the DEVFORGE knowledge base and split it
    into sections based on Markdown headings.
    """

    with open(KB_PATH, "r", encoding="utf-8") as file:
        text = file.read()

    sections = re.split(r"\n(?=## )", text)

    documents = []

    for section in sections:
        section = section.strip()

        if section:
            documents.append(section)

    return documents


documents = load_documents()


def retrieve_context(question, k=3):
    """
    Lightweight retrieval method suitable for Vercel.

    Scores knowledge-base sections based on how many
    question words appear in each section.
    """

    question_words = set(
        re.findall(r"\b[a-zA-Z0-9]+\b", question.lower())
    )

    scored_documents = []

    for document in documents:

        document_words = set(
            re.findall(
                r"\b[a-zA-Z0-9]+\b",
                document.lower()
            )
        )

        score = len(
            question_words.intersection(document_words)
        )

        scored_documents.append(
            (score, document)
        )

    scored_documents.sort(
        key=lambda item: item[0],
        reverse=True
    )

    selected = [
        document
        for score, document in scored_documents[:k]
        if score > 0
    ]

    if not selected:
        selected = documents[:k]

    return "\n\n".join(selected)
