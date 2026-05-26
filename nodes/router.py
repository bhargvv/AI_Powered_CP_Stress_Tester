def verification_router(state):

    if (
        state["generation_attempts"]
        >= 3
    ):
        return "failed"

    if state["verdict"] == "REGENERATE":
        return "retry"

    return "continue"

def stress_router(state):

    if state["verdict"] in [

        "WA",
        "RE",
        "TLE",
        "CE"

    ]:
        return "failed"

    if (
        state["current_test"]
        >=
        state["max_tests"]
    ):
        return "passed"

    return "continue"