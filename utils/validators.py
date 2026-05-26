import ast

def validate_python_syntax(code):

    try:

        ast.parse(code)

        return True, None

    except Exception as e:

        return False, str(e)


