# Website Control Center

The website is the single control plane for Money-Agentic. API credentials stay server-side and are never exposed to browser code.

## Control areas

- Dashboard: revenue, conversions, EPC, CTR, active experiments
- Offers: CPA offers, payout, CR, EPC, status
- Campaigns: create, pause, approve, schedule
- Content: generated variants and approval
- Publishers: connected authorized accounts
- Research: knowledge sources and findings
- Experiments: A/B tests and outcomes
- Learning: strategy versions, evidence and rollback
- API Hub: connection status and configuration
- Logs: audit trail and integration errors
- Settings: limits, policy and model configuration

## Request flow

Browser -> Website API -> Auth/Permission Gateway -> Agent services -> Integration adapters

The browser never receives raw API secrets. The Website API stores encrypted secrets server-side and exposes only masked connection status.

## API Hub

Each integration has:
- provider name
- enabled/disabled state
- connection test
- masked credential status
- rate-limit status
- last successful request
- last error
- allowed capabilities

## Safety

Publishing actions require the configured permission policy. The website must not provide controls for fake traffic, fake leads, account farming, spam, or rate-limit bypassing.
