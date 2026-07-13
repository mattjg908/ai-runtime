# AI Runtime

AI Runtime is a long-term project exploring how to build reliable, observable, and fault-tolerant AI systems.

Rather than focusing on model training or prompt engineering, this repository focuses on the infrastructure required to operate AI systems in production: typed interfaces, evaluation, tool orchestration, durable execution, observability, distributed workflows, and reliability.

## Purpose

I am a senior distributed-systems engineer with experience building reliable, concurrent, and fault-tolerant systems across healthcare, IoT, cloud, and edge environments.

This project documents my transition into AI infrastructure engineering. Instead of starting over as a junior AI engineer, I am building on my existing distributed-systems experience by learning the engineering required to operate production AI systems.

Modern AI applications require much more than model training. They require engineers who can build reliable systems around models: distributed inference, agent infrastructure, workflow orchestration, evaluation frameworks, observability, durable execution, failure recovery, and production reliability.

My background is in distributed systems and fault-tolerant software. This project applies those principles to AI infrastructure rather than to machine learning research.

Every feature in this repository is built with the same engineering principles I have applied throughout my career:

- Reliability
- Correctness
- Observability
- Maintainability
- Testability

The long-term goal is to become a staff-level engineer who understands both modern AI systems and the distributed-systems techniques required to run them reliably in production.

## Project Goals

This repository is being developed incrementally over a structured multi-month plan. The project evolves from a small typed Python gateway into a complete AI runtime capable of:

- Calling multiple model providers through a common interface
- Producing validated structured outputs
- Supporting streaming responses
- Executing tools safely and deterministically
- Evaluating agent behavior across repeatable scenarios
- Recording execution trajectories
- Instrumenting workflows with OpenTelemetry
- Orchestrating long-running workflows using Elixir/OTP
- Recovering safely from failures
- Supporting durable, event-driven execution

## Repository Structure

```
ai-runtime/
├── gateway/      # Python model gateway
├── runtime/      # Elixir/OTP runtime (added incrementally)
├── scenarios/    # Evaluation scenarios
├── docs/         # Notes, architecture decisions, experiments
├── runs/         # Saved execution traces
├── docker-compose.yml
└── README.md
```

## Current Status

The project is currently in its initial foundation phase.

Completed:

- Python project structure
- Type checking with mypy
- Linting with Ruff
- Testing with pytest
- Dependency management using `pyproject.toml`
- Development environment managed with `asdf` and Python virtual environments

Future milestones include typed model providers, structured outputs, evaluation harnesses, AI observability, Elixir workflow orchestration, durable execution, and production deployment.

## Development

### Python

```bash
cd gateway

source .venv/bin/activate

python -m pip install --editable ".[dev]"

pytest
ruff check .
ruff format --check .
mypy src tests
```

## Principles

Some guiding principles for this project:

- Build small, tested vertical slices.
- Prefer explicit interfaces over framework magic.
- Favor typed data structures over unstructured dictionaries.
- Make failures observable.
- Treat reliability as a feature.
- Build infrastructure before abstractions.
- Avoid unnecessary frameworks until the underlying concepts are understood.

## License

This project is currently under active development.
