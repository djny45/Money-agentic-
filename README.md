# Money-Agentic

Autonomous CPA promotion and optimization agent focused on legitimate, measurable affiliate traffic.

## Core principles
- Optimize for real conversions and revenue, not artificial clicks.
- Use official APIs and authorized accounts.
- Respect platform terms, CPA network rules, rate limits, and disclosure requirements.
- Research, experiment, measure, learn, version, and roll back.
- Never automate fake leads, fake accounts, click fraud, spam, or tracking bypasses.

## Architecture

```
Research -> Offer Intelligence -> Strategy -> Content -> Distribution
                                      ^             |
                                      |             v
                               Learning <--- Analytics
                                      |
                               Strategy Versions
```

## Components
- Swarm orchestrator
- Offer intelligence
- Research/knowledge ingestion
- Content experimentation
- Publisher adapters
- Attribution and analytics
- Strategy memory
- Experiment manager
- Safety/compliance gateway
- Versioned strategy and rollback
- SQLite persistence
- Optional Ollama local LLM

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app
```

The default mode is **DRY_RUN**. Publishing requires explicit configuration of authorized platform adapters.

## License
MIT
