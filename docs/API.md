# API & Integrations

All integration credentials are configured through environment variables. **Never put real API keys in source code or commit them to GitHub.**

## Integration groups

| Integration | Variables | Purpose |
|---|---|---|
| CPA network | `CPAGRIP_API_KEY`, `CPAGRIP_API_URL` | Authorized offer/report integration |
| Postiz | `POSTIZ_API_KEY`, `POSTIZ_API_URL` | Self-hosted publishing/scheduling |
| Bluesky | `BLUESKY_HANDLE`, `BLUESKY_APP_PASSWORD` | Authorized social publishing |
| Mastodon | `MASTODON_ACCESS_TOKEN`, `MASTODON_BASE_URL` | Authorized social publishing |
| Ollama | `OLLAMA_URL`, `OLLAMA_MODEL` | Local AI inference |

## Security

- Secrets are loaded from environment variables.
- Real credentials must stay outside Git.
- Only authorized accounts may publish.
- Rate limits and platform rules must be respected.
- Publishing stays disabled until explicitly configured.
- Integration failures should fail closed rather than trigger uncontrolled retries.

## Adding an integration

1. Add environment-variable names to `.env.example`.
2. Add configuration to `app/api_registry.py`.
3. Implement a dedicated adapter.
4. Add tests with mocks/fixtures.
5. Add rate limiting and error handling.
