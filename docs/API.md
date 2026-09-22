# API and integration contract

## Security
Secrets are environment variables only. They are never returned by the website API, stored in SQLite, or written to strategy memory.

## CPAGrip
The adapter treats CPAGrip as an offer-feed integration. CPAGrip documents JSON/XML/CSV offer feeds and postback/analytics tooling. The configured CPAGRIP_API_URL therefore points to the feed/report endpoint supplied by the user's CPAGrip account rather than an assumed undocumented REST route.

The adapter can health-check the configured feed, fetch it, parse JSON/XML/CSV, and normalize common offer fields: id, title, url, payout, country, category.

The agent does not fabricate offer metrics. Conversion rate, EPC, and revenue must come from observed campaign/report data.

## Postiz
The adapter uses the documented public API endpoints GET /public/v1/integrations and POST /public/v1/posts.

Publishing is approval-first. The dashboard should create drafts by default. Scheduling a live post requires an explicitly configured, authorized Postiz integration ID and an explicit approval action.

The agent must not create accounts, evade platform limits, generate fake engagement, or publish spam.

## Environment

CPAGRIP_API_KEY=
CPAGRIP_API_URL=
POSTIZ_API_KEY=
POSTIZ_API_URL=https://api.postiz.com

Use the exact feed/report endpoint and credentials provided by the relevant provider account. Do not copy secrets into Git.

## Campaign intelligence service

The Python service layer now persists offers and experiments, generates UTM tracking URLs from stored offer destinations, aggregates measured metrics, and evaluates experiments through the evidence-based learning engine. Learning actions are `collect_more_data`, `pause_experiment`, or `retain_and_test`; the service does not rewrite executable code.
