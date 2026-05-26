import os
import subprocess
import json


WORKSPACE = os.path.abspath(
    "sandbox/workspace"
)

IMAGE_NAME = "ai-agent-runner"


def compile_code(
    filename,
    language
):

    try:

        if language == "cpp":

            compile_cmd = [

                "docker",
                "run",
                "--rm",

                "-v",
                f"{WORKSPACE}:/workspace",

                IMAGE_NAME,

                "g++",
                f"/workspace/{filename}",
                "-o",
                "/workspace/a.out"
            ]

            result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:

                return json.dumps({
                    "status": "CE",
                    "output": result.stderr
                })

            return json.dumps({
                "status": "OK",
                "output": ""
            })

        if language == "java":

            compile_cmd = [

                "docker",
                "run",
                "--rm",

                "-v",
                f"{WORKSPACE}:/workspace",

                IMAGE_NAME,

                "javac",
                f"/workspace/{filename}"
            ]

            result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:

                return json.dumps({
                    "status": "CE",
                    "output": result.stderr
                })

            return json.dumps({
                "status": "OK",
                "output": ""
            })


        return json.dumps({
            "status": "OK",
            "output": ""
        })

    except subprocess.TimeoutExpired:

        return json.dumps({
            "status": "CE",
            "output": "Compilation timeout"
        })

    except Exception as e:

        return json.dumps({
            "status": "CE",
            "output": str(e)
        })
    


def run_code(
    filename,
    language,
    input_data=""
):

    try:


        if language == "python":

            run_cmd = [

                "docker",
                "run",
                "--rm",

                "-i",

                "-v",
                f"{WORKSPACE}:/workspace",

                IMAGE_NAME,

                "python",
                f"/workspace/{filename}"
            ]

    

        elif language == "cpp":

            run_cmd = [

                "docker",
                "run",
                "--rm",

                "-i",

                "-v",
                f"{WORKSPACE}:/workspace",

                IMAGE_NAME,

                "/workspace/a.out"
            ]

    

        elif language == "java":

            class_name = (
                filename
                .replace(".java", "")
            )

            run_cmd = [

                "docker",
                "run",
                "--rm",

                "-i",

                "-v",
                f"{WORKSPACE}:/workspace",

                IMAGE_NAME,

                "java",
                "-cp",
                "/workspace",

                class_name
            ]

        else:

            return json.dumps({
                "status": "RE",
                "output": (
                    "Unsupported language"
                )
            })

    

        result = subprocess.run(

            run_cmd,

            input=input_data,

            capture_output=True,

            text=True,

            timeout=5
        )

        if result.returncode != 0:

            return json.dumps({
                "status": "RE",
                "output": result.stderr
            })

        return json.dumps({
            "status": "OK",
            "output": result.stdout
        })

    except subprocess.TimeoutExpired:

        return json.dumps({
            "status": "TLE",
            "output": "Execution timeout"
        })

    except Exception as e:

        return json.dumps({
            "status": "RE",
            "output": str(e)
        })