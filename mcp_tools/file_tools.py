import os
import json



WORKSPACE = "sandbox/workspace"

os.makedirs(
    WORKSPACE,
    exist_ok=True
)


def write_code_file(
    filename,
    code
):

    path = os.path.join(
        WORKSPACE,
        filename
    )

    with open(path, "w") as f:
        f.write(code)

    return json.dumps({
        "status": "OK"
    })



def read_code_file(filename):

    path = os.path.join(
        WORKSPACE,
        filename
    )

    if not os.path.exists(path):

        return json.dumps({
            "status": "ERROR",
            "output": "File not found"
        })

    with open(path, "r") as f:

        content = f.read()

    return json.dumps({
        "status": "OK",
        "output": content
    })