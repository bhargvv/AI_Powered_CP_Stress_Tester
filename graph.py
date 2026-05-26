from typing import TypedDict
from typing import Optional

from langgraph.graph import (
    StateGraph,
    END
)

from nodes.prepare_generation import (
    prepare_generation
)

from nodes.verify_generation import (
    verify_generation
)

from nodes.stress_test import (
    run_stress_test
)

from nodes.router import (
    verification_router,
    stress_router
)


class StressTestState(TypedDict):


    problem_statement: str

    og_code: str

    language: str

    filename: str

    max_tests: int

    current_test: int

    generation_attempts: int

    brute_force_code: Optional[str]

    generator_code: Optional[str]

    verdict: Optional[str]

    failing_input: Optional[str]

    og_output: Optional[str]

    bf_output: Optional[str]

    verification_error: Optional[str]


workflow = StateGraph(
    StressTestState
)

workflow.add_node(
    "prepare_generation",
    prepare_generation
)

workflow.add_node(
    "verify_generation",
    verify_generation
)

workflow.add_node(
    "stress_test",
    run_stress_test
)

workflow.set_entry_point(
    "prepare_generation"
)

workflow.add_edge(
    "prepare_generation",
    "verify_generation"
)

workflow.add_conditional_edges(

    "verify_generation",

    verification_router,

    {

        "retry":
            "prepare_generation",

        "continue":
            "stress_test",

        "failed":
            END
    }
)


workflow.add_conditional_edges(

    "stress_test",

    stress_router,

    {

        "continue":
            "stress_test",

        "failed":
            END,

        "passed":
            END
    }
)


app_graph = workflow.compile()