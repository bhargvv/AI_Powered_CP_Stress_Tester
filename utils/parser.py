import re


def extract_tag(
    text: str,
    tag: str
):

    match = re.search(
        f"<{tag}>(.*?)</{tag}>",
        text,
        re.DOTALL
    )

    if not match:
        return ""

    content = (
        match
        .group(1)
        .strip()
    )

    content = re.sub(
        r"^```[a-zA-Z]*",
        "",
        content
    )

    content = re.sub(
        r"```$",
        "",
        content
    )

    return content.strip()