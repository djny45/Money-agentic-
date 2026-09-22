# Money-Agentic Web

The landing page is the control center for the Money-Agentic backend.

## API architecture

The browser should never receive CPA/social API secrets. Configure secrets on the server and expose only authenticated, minimal API endpoints to this frontend.

Planned backend routes:
- GET /api/status
- GET /api/integrations
- POST /api/integrations/{provider}/test
- GET /api/offers
- GET /api/campaigns
- GET /api/analytics
- POST /api/experiments
- POST /api/publish/queue
- POST /api/strategies/rollback

The frontend is currently a UI foundation; provider adapters remain server-side.
