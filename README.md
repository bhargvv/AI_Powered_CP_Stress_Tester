# CP Multi-Language Sandbox Tester (AI Powered)

A competitive-programming (CP) stress-testing toolkit that helps you find corner cases by running a trusted reference implementation (brute-force or correct solution) against one or more candidate solutions across many generated test cases. This project includes optional AI-assisted test-generation and a sandboxed execution environment for multi-language support.

Why this exists
- Finding hard-to-reach bugs in CP solutions is time-consuming. This tool automates test-case generation, verification, and differential testing to surface Wrong Answers, Runtime Errors, Timeouts, and other failures.
- AI-assisted generators can explore non-obvious edge cases faster than naive randomized testers.

Key features
- Generate brute-force (reference) solutions and test-case generators (including LLM-assisted generators).
- Verify generated helpers before running stress tests to avoid false positives.
- Sandboxed execution for multiple languages (Python and other runtimes supported in the Docker environment).
- Record and persist failing test cases for later debugging and reuse.
- Streamlit frontend and FastAPI backend for interactive workflows.

Repository layout (important files)
- app.py — Streamlit web UI for entering problem statements, code, and running tests
- server.py — FastAPI backend exposing stress endpoints
- graph.py — LangGraph workflow orchestration for generation, verification, and testing
- nodes/ — Workflow node implementations (prepare_generation, verify_generation, stress_test, router)
- memory/chroma_memory.py — Optional Chroma persistence for known failures/successes
- docker/Dockerfile — Base image for sandboxed execution (includes common toolchains)
- requirements.txt — Python dependencies

Quickstart (local)
1. Clone the repo

   git clone https://github.com/bhargvv/AI_Powered_CP_Stress_Tester.git
   cd AI_Powered_CP_Stress_Tester

2. Create and activate a virtual environment

   python -m venv .venv
   source .venv/bin/activate   # macOS / Linux
   .venv\Scripts\activate    # Windows

3. Install dependencies

   pip install -r requirements.txt

4. Configure environment variables (if using LLM/AI generation)

   - Set GEMINI_API_KEY or other provider keys as required (see code/config for supported providers).
   - Create a `.env` file or export the keys into your shell.

5. Run the backend and frontend

   uvicorn server:app --reload --port 8000
   streamlit run app.py

Usage overview
- From the Streamlit UI, provide:
  - Problem statement/description
  - A reference (brute-force) implementation or choose to auto-generate one
  - One or more candidate solutions to test
  - Target language (e.g., python, cpp, java) and iteration count
- Start the stress test. The backend will:
  1. Generate (or accept) a brute-force reference and a test-case generator
  2. Validate that generated code runs and produces expected output on sanity checks
  3. Run many randomized/AI-generated test cases, comparing outputs and reporting mismatches
- Failures (WA/RE/TLE) are reported with the input that triggered them and any available logs.

Docker (optional)
- Build the sandbox image (used as a reference environment for compilation/execution):

   docker build -t ai-agent-runner -f docker/Dockerfile .

- Run commands inside the container or mount your repo to run tests in an isolated environment.

Configuration & notes
- Timeouts: Configure per-test timeouts to avoid long-running or hung processes.
- Generators: Use the deterministic or LLM-based generator depending on the breadth of coverage desired. LLM generators may require API keys and might incur costs.
- Persisting failures: The project optionally saves failing cases in Chroma memory for later inspection and similarity-based reuse.
- Security: The tool executes untrusted code in a sandboxed environment. Review the Docker sandbox implementation before use in untrusted environments.

Contributing
- Bug reports, feature requests, and pull requests are welcome. Please include tests for new functionality where applicable and keep PRs focused.

License
- Add or update a LICENSE file to declare the project license (e.g., MIT).

Contact
- For questions or issues, please open an issue in the repo.
