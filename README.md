# CP Multi-Language Sandbox Tester

A competitive programming stress-testing prototype built with Streamlit, FastAPI, LangGraph, and Google Gemini-style generation. It generates brute-force Python reference code and randomized test inputs, then runs user solutions in a sandboxed execution flow.

## What it does

- Accepts a problem statement, user solution, and target language from the UI
- Generates a brute-force Python reference implementation and a randomized test-case generator
- Verifies generator and brute-force validity before stress testing
- Runs the user's code in a sandboxed MCP tool environment
- Detects and reports:
  - `AC` (all tests passed)
  - `WA` (wrong answer)
  - `RE` (runtime error)
  - `TLE` (timeout)
  - `CE` (compilation error)

## Key files

- `app.py` — Streamlit frontend for entering problem statements, code, and running tests
- `server.py` — FastAPI backend exposing `/stress` and orchestrating the workflow
- `graph.py` — LangGraph workflow definition for generation, verification, and stress testing
- `nodes/prepare_generation.py` — LLM prompt and brute-force/generator generation step
- `nodes/verify_generation.py` — Syntax and execution validation of generated code
- `nodes/stress_test.py` — Executes generated code and user code through the MCP tool
- `nodes/router.py` — Workflow routing logic for retrying or continuing
- `memory/chroma_memory.py` — Persistent Chroma memory store for previous failures/successes
- `docker/Dockerfile` — Base sandbox image with Python, C/C++, and Java toolchains
- `requirements.txt` — Core Python dependencies

## Architecture

1. User enters a problem statement, code, language, and test count in Streamlit (`app.py`).
2. The frontend sends the request to FastAPI (`server.py`).
3. `graph.py` runs a LangGraph workflow with three main stages:
   - `prepare_generation`
   - `verify_generation`
   - `stress_test`
4. Generated brute-force and test-case code are verified before stress testing.
5. The MCP-backed sandbox environment compiles/runs code and returns results.
6. Memory data is saved to `memory/chroma_db` for future similarity-based context.

## Requirements

- Python 3.11+ (project uses Python 3.12 in the virtual environment)
- Docker Engine (for sandbox execution if you use Docker tooling)
- `GEMINI_API_KEY` set in the environment or `.env`
- Required Python packages including:
  - `streamlit`
  - `requests`
  - `mcp`
  - `fastapi`
  - `uvicorn`
  - `python-dotenv`
  - `pydantic`
  - `langgraph`
  - `langchain_google_genai`
  - `chromadb`

## Setup

1. Activate your virtual environment:

```bash
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
pip install fastapi uvicorn python-dotenv pydantic langgraph langchain_google_genai chromadb
```

3. Configure your Gemini API key in `.env` or environment variables:

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

4. Start the backend server:

```bash
uvicorn server:app --reload --port 8000
```

5. Start the frontend UI:

```bash
streamlit run app.py
```

## Running with Docker

The repository includes a Dockerfile at `docker/Dockerfile` for a sandbox base image.

Build it with:

```bash
docker build -t ai-agent-runner -f docker/Dockerfile .
```

Use the image as a reference environment for language runtimes and compilation.

## Usage

- Open the Streamlit app in your browser
- Enter a problem statement and paste your code
- Select the target language (`cpp`, `python`, or `java`)
- Choose the number of randomized test cases
- Click **Start Stress Test**

The app will display one of the following outcomes:

- `Accepted` if the solution passes all tests
- `Wrong Answer` with failing input and expected output
- `Runtime Error` with error logs
- `Time Limit Exceeded` with failing input
- `Generation verification failed` if the generated helper code needs regeneration

## Notes

- Generated brute-force and generator code are validated before stress testing.
- Failure and success cases are stored in Chroma memory for later context.
- The backend uses MCP tooling to isolate code compilation and execution.
- If the frontend cannot connect, ensure `uvicorn server:app --reload --port 8000` is running.
