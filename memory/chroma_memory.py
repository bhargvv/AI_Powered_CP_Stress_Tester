import os
import uuid
import chromadb

from chromadb.utils.embedding_functions import (
    DefaultEmbeddingFunction,
)



CHROMA_DIR = "memory/chroma_db"

os.makedirs(CHROMA_DIR, exist_ok=True)


embedding_function = (
    DefaultEmbeddingFunction()
)

client = chromadb.PersistentClient(
    path=CHROMA_DIR
)


collection = client.get_or_create_collection(
    name="stress_testing_memory",
    embedding_function=embedding_function
)


def classify_problem(statement: str):

    s = statement.lower()

    if "graph" in s:
        return "graph"

    if "tree" in s:
        return "tree"

    if "array" in s:
        return "array"

    if "string" in s:
        return "string"

    if "dynamic programming" in s:
        return "dp"

    if "dp" in s:
        return "dp"

    if "math" in s:
        return "math"

    return "general"


def save_failure_memory(
    problem_statement,
    brute_force_code,
    generator_code,
    failure_reason,
    suggested_fix,
    metadata=None
):

    if metadata is None:
        metadata = {}

    memory_text = f"""
    Problem:
    {problem_statement}

    Brute_Force:
    {brute_force_code}

    Generator:
    {generator_code}

    Failure:
    {failure_reason}

    Suggested Fix:
    {suggested_fix}
    """

    metadata.update({
        "type": "failure",
        "problem_type": classify_problem(
            problem_statement
        )
    })

    collection.add(
        ids=[str(uuid.uuid4())],
        documents=[memory_text],
        metadatas=[metadata]
    )


def save_success_memory(
    problem_statement,
    brute_force_code,
    generator_code,
    successful_strategy,
    metadata=None
):

    if metadata is None:
        metadata = {}

    memory_text = f"""
    Problem:
    {problem_statement}

    Brute_Force:
    {brute_force_code}

    Generator:
    {generator_code}

    Successful Strategy:
    {successful_strategy}
    """

    metadata.update({
        "type": "success",
        "problem_type": classify_problem(
            problem_statement
        )
    })

    collection.add(
        ids=[str(uuid.uuid4())],
        documents=[memory_text],
        metadatas=[metadata]
    )


def retrieve_memories(
    query,
    n_results=5,
    memory_type=None
):

    where_filter = None

    if memory_type:

        where_filter = {
            "type": memory_type
        }

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where_filter
    )

    formatted_memories = []

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    for doc, meta, dist in zip(
        documents,
        metadatas,
        distances
    ):

        formatted_memories.append({
            "memory": doc,
            "metadata": meta,
            "distance": dist
        })

    return formatted_memories


def build_memory_context(problem_statement):

    memories = retrieve_memories(
        query=problem_statement,
        n_results=5
    )

    if not memories:
        return ""

    context = "\n\n===== PREVIOUS LEARNINGS =====\n"

    for idx, mem in enumerate(memories, start=1):

        context += f"""
Memory {idx}:

{mem['memory']}

--------------------------------
"""

    return context


def clear_memory():

    global collection

    client.delete_collection(
        "stress_testing_memory"
    )

    collection = client.get_or_create_collection(
        name="stress_testing_memory",
        embedding_function=embedding_function
    )

def print_all_memories():

    results = collection.get()

    docs = results.get("documents", [])

    metas = results.get("metadatas", [])

    for idx, (doc, meta) in enumerate(
        zip(docs, metas),
        start=1
    ):

        print("\n======================")
        print(f"MEMORY {idx}")
        print("======================")

        print(doc)

        print("\nMetadata:")
        print(meta)