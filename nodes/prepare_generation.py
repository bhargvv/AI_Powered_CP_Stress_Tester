import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from utils.parser import extract_tag

from memory.chroma_memory import (
    build_memory_context
)

load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)


async def prepare_generation(state):

    memory_context = build_memory_context(
        state["problem_statement"]
    )

    prompt = f"""
    Problem Statement:
    {state['problem_statement']}

    Previous learnings:
    {memory_context}

    Requirements:

    1. Generate deterministic brute force Python solution.
    2. Use simplest possible logic.
    3. Avoid recursion.
    4. Avoid huge generators.
    5. Keep constraints VERY SMALL.
    6. Avoid infinite loops.
    7. Output raw Python code only.
    8. No markdown.
    9. No explanations.
    10. No comments in the brute force solution and similarily for generator.
    11. Prioritize correctness over speed.

    Generator Requirements:

    - Prefer n <= 25
    - Prefer tiny random values
    - Always terminate

    Format EXACTLY:

    <brute_force>
    code
    </brute_force>

    <generator>
    code
    </generator>
    """

    response = str(llm.invoke([
        HumanMessage(content=prompt)
    ]).content)

    brute_force_code = extract_tag(
        response,
        "brute_force"
    )

    generator_code = extract_tag(
        response,
        "generator"
    )

    return {
        "brute_force_code": brute_force_code,
        "generator_code": generator_code,
        "generation_attempts":
            state["generation_attempts"] + 1
    }