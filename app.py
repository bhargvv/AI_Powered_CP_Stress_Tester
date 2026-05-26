import streamlit as st
import requests
import os

from dotenv import load_dotenv

load_dotenv()

st.set_page_config(

    page_title="CP Sandbox Tester",

    layout="wide"
)

st.title(
    "CP Multi-Language Sandbox Tester 🐳"
)


if "stress_running" not in st.session_state:

    st.session_state.stress_running = False


col1, col2 = st.columns(2)

with col1:

    problem_statement = st.text_area(

        "Problem Statement",

        height=350,

        disabled=st.session_state.stress_running
    )

    language = st.selectbox(

        "Target Language",

        [
            "cpp",
            "python",
            "java"
        ],

        disabled=st.session_state.stress_running
    )

with col2:

    og_code = st.text_area(

        "Your Code",

        height=350,

        disabled=st.session_state.stress_running
    )

    max_tests = st.slider(

        "Random Test Cases",

        10,
        1000,
        50,

        disabled=st.session_state.stress_running
    )

ext_map = {

    "cpp": "og.cpp",

    "python": "og.py",

    "java": "Solution.java"
}


start_clicked = st.button(

    "Start Stress Test 🚀",

    disabled=st.session_state.stress_running
)


if start_clicked:

    st.session_state.stress_running = True

    try:

        if not problem_statement.strip():

            st.error(
                "Please provide "
                "the problem statement."
            )

            st.stop()

        if not og_code.strip():

            st.error(
                "Please provide your code."
            )

            st.stop()

        payload = {

            "problem_statement":
                problem_statement,

            "og_code":
                og_code,

            "language":
                language,

            "filename":
                ext_map[language],

            "max_tests":
                max_tests
        }

        progress_bar = st.progress(0)

        status_text = st.empty()

        with st.spinner(

            "Running adaptive "
            "stress testing agent..."
        ):

            response = requests.post(

                "http://localhost:8000/stress",

                json=payload,

                timeout=600
            )

        result = response.json()

        status = result.get(
            "status"
        )

        current_test = result.get(
            "current_test",
            0
        )

        progress = min(
            current_test / max_tests,
            1.0
        )

        progress_bar.progress(progress)

        
        if status == "AC":

            progress_bar.progress(1.0)

            st.success(
                f"✅ Accepted! "
                f"Passed {max_tests} "
                f"randomized test cases."
            )

        # -------------------------------
        # Compilation Error
        # -------------------------------

        elif status == "CE":

            st.error(
                "Compilation Error 🚨"
            )

            st.markdown(
                "## Compiler Output"
            )

            st.code(

                result.get(
                    "error_log",
                    ""
                ),

                language="bash"
            )


        elif status == "REGENERATE":

            retry_count = result.get(
                "retry_count",
                0
            )

            max_retries = 3

            if retry_count < max_retries:

                st.warning(
                    f"Test case generator/brute-force code generation failed. "
                    f"Regenerating... "
                    f"(Attempt {retry_count + 1} of {max_retries}) 🔄"
                )

            else:

                st.error(
                    "Test case generator/brute-force code generation failed after multiple attempts. "
                    "Please check your problem statement for clarity and try again. ❌"
                )

            verification_error = result.get(
                "verification_error"
            )

            if verification_error:

                st.markdown(
                    "## Verification Error"
                )

                st.code(
                    verification_error,
                    language="text"
                )


        elif status == "WA":

            st.error(
                f"Wrong Answer "
                f"on test "
                f"#{current_test} ❌"
            )

            st.markdown(
                "## Failing Test Case"
            )

            st.code(

                result.get(
                    "failing_input",
                    ""
                ),

                language="text"
            )

            col_a, col_b = st.columns(2)

            with col_a:

                st.markdown(
                    "### Your Output"
                )

                st.code(

                    result.get(
                        "og_output",
                        ""
                    ),

                    language="text"
                )

            with col_b:

                st.markdown(
                    "### Expected Output"
                )

                st.code(

                    result.get(
                        "bf_output",
                        ""
                    ),

                    language="text"
                )

        elif status == "RE":

            st.error(
                f"Runtime Error "
                f"on test "
                f"#{current_test} 💥"
            )

            st.markdown(
                "## Failing Test Case"
            )

            st.code(

                result.get(
                    "failing_input",
                    ""
                ),

                language="text"
            )

            st.markdown(
                "## Error Log"
            )

            st.code(

                result.get(
                    "error_log",
                    ""
                ),

                language="bash"
            )


        elif status == "TLE":

            st.error(
                f"Time Limit Exceeded "
                f"on test "
                f"#{current_test} ⏳"
            )

            st.markdown(
                "## Failing Test Case"
            )

            st.code(

                result.get(
                    "failing_input",
                    ""
                ),

                language="text"
            )

            if result.get("og_output"):

                st.markdown(
                    "## Partial Output"
                )

                st.code(

                    result.get(
                        "og_output",
                        ""
                    ),

                    language="text"
                )

        else:

            st.error(
                "Unknown response "
                "from backend."
            )

            st.json(result)

    except requests.exceptions.ConnectionError:

        st.error(

            "Cannot connect to "
            "backend server.\n\n"

            "Make sure FastAPI "
            "server is running."
        )

    except requests.exceptions.Timeout:

        st.error(
            "Request timed out."
        )

    except Exception as e:

        st.error(
            f"Unexpected Error:\n{str(e)}"
        )

    finally:

        st.session_state.stress_running = False