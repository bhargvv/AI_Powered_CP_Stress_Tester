from fastapi import FastAPI
from pydantic import BaseModel

from graph import app_graph

app = FastAPI()


class StressRequest(BaseModel):

    problem_statement: str

    og_code: str

    language: str

    filename: str

    max_tests: int

@app.post("/stress")

async def stress_test(data: StressRequest):

    initial_state = {

        "problem_statement":
            data.problem_statement,

        "og_code":
            data.og_code,

        "language":
            data.language,

        "filename":
            data.filename,

        "max_tests":
            data.max_tests,

        "current_test":
            0,

        "generation_attempts":
            0,

        "verdict":
            None,

        "brute_force_code":
            None,

        "generator_code":
            None,

        "failing_input":
            None,

        "og_output":
            None,

        "bf_output":
            None,

        "verification_error":
            None
    }

    final_response = {

        "status": "AC",

        "message": (
            f"Passed "
            f"{data.max_tests} "
            f"randomized test cases."
        ),

        "failing_input": None,

        "og_output": None,

        "bf_output": None,

        "current_test": 0,

        "error_log": None,

        "verification_error": None
    }


    async for output in app_graph.astream(
        initial_state
    ):

        for key, value in output.items():

            if key == "prepare_generation":

                if value.get("verdict") == "CE":

                    final_response["status"] = "CE"

                    final_response["message"] = (
                        "Compilation Error"
                    )

                    final_response["error_log"] = (
                        value.get(
                            "og_output",
                            "Compilation failed."
                        )
                    )

                    return final_response


            if key == "verify_generation":

                if value.get("verdict") == "REGENERATE":

                    final_response["status"] = (
                        "REGENERATE"
                    )

                    final_response["message"] = (
                        "Generation verification failed"
                    )

                    final_response[
                        "verification_error"
                    ] = value.get(
                        "verification_error"
                    )


            if key == "stress_test":

                final_response[
                    "current_test"
                ] = value.get(
                    "current_test",
                    0
                )

                verdict = value.get(
                    "verdict"
                )

                if verdict in [

                    "WA",
                    "RE",
                    "TLE"

                ]:

                    final_response[
                        "status"
                    ] = verdict

                    final_response[
                        "message"
                    ] = (
                        f"Failed with {verdict}"
                    )

                    final_response[
                        "failing_input"
                    ] = value.get(
                        "failing_input"
                    )

                    final_response[
                        "og_output"
                    ] = value.get(
                        "og_output"
                    )

                    final_response[
                        "bf_output"
                    ] = value.get(
                        "bf_output"
                    )

                    final_response[
                        "error_log"
                    ] = value.get(
                        "og_output"
                    )

                    return final_response

                if verdict == "REGENERATE":

                    final_response[
                        "status"
                    ] = "REGENERATE"

                    final_response[
                        "message"
                    ] = (
                        "Regenerating "
                        "BF and generator"
                    )


                if verdict == "TESTING":

                    final_response[
                        "message"
                    ] = (
                        f"Running test "
                        f"{value.get('current_test', 0)} "
                        f"/ "
                        f"{data.max_tests}"
                    )

    return final_response