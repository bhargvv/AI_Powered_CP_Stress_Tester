import json

from mcp import (
    ClientSession,
    StdioServerParameters
)

from mcp.client.stdio import (
    stdio_client
)

from memory.chroma_memory import (
    save_failure_memory,
    save_success_memory
)


server_params = StdioServerParameters(
    command="python",
    args=["-m", "mcp_tools.mcp_server"]
)


async def run_stress_test(state):

    async with stdio_client(
        server_params
    ) as (read, write):

        async with ClientSession(
            read,
            write
        ) as session:

            await session.initialize()

            await session.call_tool(
                "write_code_file_tool",
                {
                    "filename": "bf.py",
                    "code": state[
                        "brute_force_code"
                    ]
                }
            )

            await session.call_tool(
                "write_code_file_tool",
                {
                    "filename": "gen.py",
                    "code": state[
                        "generator_code"
                    ]
                }
            )

            await session.call_tool(
                "write_code_file_tool",
                {
                    "filename": state[
                        "filename"
                    ],
                    "code": state[
                        "og_code"
                    ]
                }
            )


            if state["language"] != "python":

                compile_result = await session.call_tool(
                    "compile_code_tool",
                    {
                        "filename": state[
                            "filename"
                        ],
                        "language": state[
                            "language"
                        ]
                    }
                )

                compile_result = json.loads(
                    compile_result.content[0].text
                )

                if (
                    compile_result["status"]
                    !=
                    "OK"
                ):

                    return {

                        "verdict": "CE",

                        "og_output":
                            compile_result.get(
                                "output",
                                ""
                            )
                    }


            gen_result = await session.call_tool(
                "run_code_tool",
                {
                    "filename": "gen.py",
                    "language": "python",
                    "input_data": ""
                }
            )


            gen_result = json.loads(
                gen_result.content[0].text
            )

            if gen_result["status"] != "OK":

                return {

                    "verdict": "RE",

                    "og_output":
                        gen_result.get(
                            "output",
                            ""
                        )
                }

            test_input = gen_result[
                "output"
            ]

            bf_result = await session.call_tool(
                "run_code_tool",
                {
                    "filename": "bf.py",
                    "language": "python",
                    "input_data": test_input
                }
            )

            bf_result = json.loads(
                bf_result.content[0].text
            )

            og_result = await session.call_tool(
                "run_code_tool",
                {
                    "filename": state[
                        "filename"
                    ],
                    "language": state[
                        "language"
                    ],
                    "input_data": test_input
                }
            )

            og_result = json.loads(
                og_result.content[0].text
            )

            if bf_result["status"] != "OK":

                save_failure_memory(

                    problem_statement=state[
                        "problem_statement"
                    ],

                    brute_force_code=state["brute_force_code"],

                    generator_code=state["generator_code"],

                    failure_reason=(
                        "Brute Force execution failed"
                    ),

                    suggested_fix=(
                        "Generate stable Brute Force solution and check for correctness of Brute Force solution implementation"
                    )
                )

                return {
                    "verdict": "REGENERATE"
                }

            if og_result["status"] in [
                "TLE",
                "RE"
            ]:

                save_success_memory(

                    problem_statement=state[
                        "problem_statement"
                    ],

                    brute_force_code=state["brute_force_code"],

                    generator_code=state["generator_code"],

                    successful_strategy=("User's solution failing on testcases indicates that the testcases are effective in figuring out tle and re issues in the user's code. This is a good sign for the stress testing process and indicates that generators like this are quite helpful.")

                )

                return {

                    "verdict":
                        og_result["status"],

                    "failing_input":
                        test_input,

                    "og_output":
                        og_result.get(
                            "output",
                            ""
                        ),

                    "current_test":
                        state["current_test"] + 1
                }

            if (
                og_result["output"]
                !=
                bf_result["output"]
            ):

                save_success_memory(

                    problem_statement=state[
                        "problem_statement"
                    ],

                    brute_force_code=state["brute_force_code"],
                    generator_code=state["generator_code"],

                    successful_strategy=("Small deterministic generators worked, as they were able to find a failing test case where the user's code output did not match the brute force output. This indicates that the stress testing process is effective in identifying correctness issues in the user's code.")
                )

                return {

                    "verdict": "WA",

                    "failing_input":
                        test_input,

                    "og_output":
                        og_result["output"],

                    "bf_output":
                        bf_result["output"],

                    "current_test":
                        state["current_test"] + 1
                }

    if (
        state["current_test"] + 1
        >=
        state["max_tests"]
    ):

        save_success_memory(

            problem_statement=state[
                "problem_statement"
            ],

            brute_force_code=state["brute_force_code"],
            generator_code=state["generator_code"],

            successful_strategy=("Stress testing process successfully ran for the maximum number of tests without finding any issues in the user's code. This indicates that the user's code is likely correct and efficient, and that the stress testing process is effective in validating the user's code against a variety of test cases. Hence the generators used in this process are quite helpful in ensuring the robustness of the user's code.")
        )

    return {

        "current_test":
            state["current_test"] + 1,

        "verdict": "TESTING"
    }