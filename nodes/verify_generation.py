import os
import tempfile
import subprocess

from utils.validators import (
    validate_python_syntax
)

from memory.chroma_memory import (
    save_failure_memory
)

async def verify_generation(state):

    brute_force = state[
        "brute_force_code"
    ]

    generator = state[
        "generator_code"
    ]


    if not brute_force.strip():

        save_failure_memory(
            problem_statement=state[
                "problem_statement"
            ],
            brute_force_code=brute_force,
            generator_code=generator,
            failure_reason="Empty brute force",
            suggested_fix=(
                "Always generate valid Brute Force Solution"
            )
        )

        return {
            "verdict": "REGENERATE",
            "verification_error":
                "Empty Brute Force Solution..."
        }

    if not generator.strip():

        save_failure_memory(
            problem_statement=state[
                "problem_statement"
            ],
            brute_force_code=brute_force,
            generator_code=generator,
            failure_reason="Empty generator",
            suggested_fix=(
                "Always generate valid generator"
            )
        )

        return {
            "verdict": "REGENERATE",
            "verification_error":
                "Empty generator"
        }


    valid, error = validate_python_syntax(
        brute_force
    )

    if not valid:

        save_failure_memory(
            problem_statement=state[
                "problem_statement"
            ],
            brute_force_code=brute_force,
            generator_code=generator,
            failure_reason=f"""
            Brute Force syntax error:
            {error}
            """,
            suggested_fix=(
                "Generate syntactically"
                "valid Brute Force Solution in Python"
            )
        )

        return {
            "verdict": "REGENERATE",
            "verification_error": error
        }

    valid, error = validate_python_syntax(
        generator
    )

    if not valid:

        save_failure_memory(
            problem_statement=state[
                "problem_statement"
            ],
            brute_force_code=brute_force,
            generator_code=generator,
            failure_reason=f"""
            Generator syntax error:
            {error}
            """,
            suggested_fix=(
                "Generate syntactically"
                "valid generator code"
            )
        )

        return {
            "verdict": "REGENERATE",
            "verification_error": error
        }


    with tempfile.TemporaryDirectory() as temp_dir:

        bf_path = os.path.join(
            temp_dir,
            "bf.py"
        )

        gen_path = os.path.join(
            temp_dir,
            "gen.py"
        )

        with open(bf_path, "w") as f:
            f.write(brute_force)

        with open(gen_path, "w") as f:
            f.write(generator)

        try:

            gen_result = subprocess.run(
                ["python", gen_path],
                capture_output=True,
                text=True,
                timeout=2
            )

        except subprocess.TimeoutExpired:

            save_failure_memory(
                problem_statement=state[
                    "problem_statement"
                ],
                brute_force_code=brute_force,
                generator_code=generator,
                failure_reason=(
                    "Generator timeout"
                ),
                suggested_fix=(
                    "Reduce testcase size"
                )
            )

            return {
                "verdict": "REGENERATE",
                "verification_error":
                    "Generator timeout"
            }

        generated_input = gen_result.stdout

        if len(generated_input) > 10000:

            save_failure_memory(
                problem_statement=state[
                    "problem_statement"
                ],
                brute_force_code=brute_force,
                generator_code=generator,
                failure_reason=(
                    "Huge testcase generation"
                ),
                suggested_fix=(
                    "Keep constraints <= 25 and generate smaller testcases"
                )
            )

            return {
                "verdict": "REGENERATE",
                "verification_error":
                    "Huge testcase"
            }

        try:

            bf_result = subprocess.run(
                ["python", bf_path],
                input=generated_input,
                capture_output=True,
                text=True,
                timeout=3
            )

        except subprocess.TimeoutExpired:

            save_failure_memory(
                problem_statement=state[
                    "problem_statement"
                ],
                brute_force_code=brute_force,
                generator_code=generator,
                failure_reason=(
                    "Brute force timeout"
                ),
                suggested_fix=(
                    "Use simpler Brute Force approach that is valid for sure but not too much time taking"
                )
            )

            return {
                "verdict": "REGENERATE",
                "verification_error":
                    "BF timeout"
            }

        if bf_result.returncode != 0:

            save_failure_memory(
                problem_statement=state[
                    "problem_statement"
                ],
                brute_force_code=brute_force,
                generator_code=generator,
                failure_reason=(
                    bf_result.stderr
                ),
                suggested_fix=(
                    "Avoid runtime crashes for brute force code. Always generate valid code that doesn't crash on generated testcases"
                )
            )

            return {
                "verdict": "REGENERATE",
                "verification_error":
                    bf_result.stderr
            }

    return {
        "verdict": "VERIFIED"
    }