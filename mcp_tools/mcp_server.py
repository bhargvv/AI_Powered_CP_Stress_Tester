import json
from mcp.server.fastmcp import FastMCP

from mcp_tools.file_tools import (

    write_code_file,
    read_code_file

)

from mcp_tools.docker_tools import (

    compile_code,
    run_code

)


mcp = FastMCP(
    "stress-testing-server"
)



@mcp.tool()
def write_code_file_tool(

    filename: str,
    code: str

):

    return write_code_file(
        filename,
        code
    )


@mcp.tool()
def read_code_file_tool(

    filename: str

):

    return read_code_file(
        filename
    )


@mcp.tool()
def compile_code_tool(

    filename: str,
    language: str

):

    return compile_code(
        filename,
        language
    )


@mcp.tool()
def run_code_tool(

    filename: str,
    language: str,
    input_data: str = ""

):

    return run_code(
        filename,
        language,
        input_data
    )


if __name__ == "__main__":

    mcp.run()