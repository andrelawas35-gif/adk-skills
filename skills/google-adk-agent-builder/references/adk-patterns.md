# Google ADK Patterns

## Official docs to refresh first

Use official Google ADK sources before relying on memory for SDK details:

- Docs home: `https://google.github.io/adk-docs/`
- Quickstart: `https://google.github.io/adk-docs/get-started/quickstart/`
- Models: `https://google.github.io/adk-docs/agents/models`
- Tools: `https://google.github.io/adk-docs/tools/`
- Sessions: `https://google.github.io/adk-docs/sessions/`
- Multi-agent systems: `https://google.github.io/adk-docs/agents/multi-agents/`
- Memory: `https://google.github.io/adk-docs/memory/`
- Evaluation: `https://google.github.io/adk-docs/evaluate/`

Refresh any page that matches the feature being implemented. ADK evolves quickly.

## Current local CLI shape

These commands are present in the installed `google-adk 2.3.0` CLI:

- `adk create`
- `adk run`
- `adk web`
- `adk api_server`
- `adk eval`
- `adk test`
- `adk deploy`
- `adk optimize`

Useful local commands:

```powershell
adk create my_agent_app
adk run path\to\my_agent
adk run path\to\my_agent "teach me the main idea"
adk web path\to\agents_dir
adk api_server path\to\agents_dir
```

If `adk` is not on `PATH`, invoke the installed executable directly from the user Scripts directory.

## Current scaffold shape

Running `adk create` produces a minimal scaffold centered on:

- `.env`
- `.gitignore`
- `agent.py`
- `__init__.py`

The generated `agent.py` currently looks like this:

```python
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model="<FILL_IN_MODEL>",
    name="root_agent",
    description="A helpful assistant for user questions.",
    instruction="Answer user questions to the best of your knowledge",
)
```

Treat this as a seed, not a final architecture.

## Build sequence

1. Create the app with `adk create` if no project exists.
2. Fill in the model and any required API or environment settings.
3. Replace the default instruction with a narrow job description.
4. Add tools for deterministic operations before adding more prompt complexity.
5. Run with `adk run` for the fastest feedback loop.
6. Switch to `adk web` only after the basic chat loop works.

## Agent patterns

### Single-agent assistant

Use for:

- one chat workflow
- one tool chain
- local experiments
- first versions of tutors or note assistants

Prefer this first.

### Tool-using tutor

Use one root agent plus Python tools when the system must:

- read notes or PDFs
- fetch glossary entries
- generate quizzes
- store or retrieve review data

Keep the root agent focused on teaching behavior. Push file parsing and storage into tools.

### Multi-agent learning system

Split into separate agents only when roles are meaningfully different:

- `reader_agent`: extracts concepts, claims, methods, and vocabulary from sources
- `tutor_agent`: explains and adapts to learner level
- `examiner_agent`: asks questions and grades or critiques responses
- `planner_agent`: decides what to learn next

If one agent can do the job cleanly, keep one agent.

## Learning-system pattern

For a "read papers and teach me" workflow, structure the system as:

1. Source ingestion
2. Concept extraction
3. Dependency mapping
4. Lesson generation
5. Recall quiz
6. Review scheduling

Keep these data objects outside the prompt when continuity matters:

- source metadata
- concept cards
- glossary entries
- misconceptions
- quiz history
- review schedule

## Grounding rules

For research and learning agents:

- cite the source used for each important claim
- distinguish direct extraction from model inference
- store summaries as artifacts, not just chat output
- prefer short explanations followed by questions that force recall

## Local development notes

- Use local runs first. Hosted deployment is a later concern.
- Prefer explicit environment configuration in `.env`.
- Keep one reproducible test prompt for each major capability.
- If `adk create` becomes interactive, pass explicit flags where possible and inspect the generated files before retrying.
