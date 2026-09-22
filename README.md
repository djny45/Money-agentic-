# Money-Agentic

<p align="center"><img src="assets/money-agentic-logo.svg" alt="Money-Agentic logo" width="720"></p>


Autonomous CPA promotion and optimization agent focused on legitimate, measurable affiliate traffic.

## Mission

Turn measured campaign data into better promotional strategies through a controlled research → experiment → measurement → learning loop.

**The system targets genuine conversions and revenue. It does not generate fake clicks/leads, create fake accounts, spam communities, bypass rate limits, or manipulate affiliate tracking.**

## Architecture

```
Research -> Offer Intelligence -> Strategy -> Content -> Compliance
                                      |               |
                                      v               v
                                  Experiments <--- Publisher Queue
                                      |
                                      v
                                  Analytics
                                      |
                                      v
                              Learning + Memory
                                      |
                                      v
                             Versioned Strategy
```

## Implemented

- Swarm coordinator
- Offer scoring from supplied/observed metrics
- Content variant generation
- Compliance gate
- Dry-run publisher queue
- Experiment primitives
- CTR / CR / EPC / profit analytics
- UTM attribution helper
- SQLite persistence
- Strategy memory
- Ollama client
- Docker support
- Automated tests + GitHub Actions
- Policy configuration

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app init
python -m app plan "Your CPA offer" --channel social
pytest -q
```

Default behavior is **DRY_RUN** and publishing requires an explicitly authorized integration.

## Self-improvement model

The agent is designed to improve **strategies**, not blindly rewrite executable source code:

1. Collect real campaign observations.
2. Form a measurable hypothesis.
3. Run a controlled experiment.
4. Measure clicks, conversions, revenue and EPC.
5. Compare against a sufficient sample.
6. Retain, pause or revise the strategy.
7. Version the strategy.
8. Roll back when regression is detected.

## Next implementation phases

See [docs/ROADMAP.md](docs/ROADMAP.md) for CPA reporting, official social APIs, research ingestion, controlled optimization, monitoring and production deployment.

## License

MIT
