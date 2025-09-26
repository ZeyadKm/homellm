# Air Pollution Literature Agent

This agent collects very recent scholarly publications about air pollution and automatically compiles a weekly-style literature review. It draws from PubMed and Crossref-indexed journals, deduplicates overlapping records, generates a structured narrative, and can email the finished review to you.

## Prerequisites

- Python 3.9+ with `pip`
- `requests` dependency (install via the steps below)

Optionally, configure SMTP credentials that can send mail on your behalf (e.g. a dedicated app password or service account).

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Alternatively, install the requirements into your preferred environment.

## Usage

Run the agent from the repository root:

```bash
PYTHONPATH=src python3 -m air_pollution_agent.cli --skip-email
```

Key options:

- `--days` *(default 7)*: how many days back to look when querying sources.
- `--max-pubmed` *(default 8)*: maximum PubMed records to include.
- `--max-crossref` *(default 8)*: maximum records from Crossref.
- `--output PATH`: save the generated review to a file.
- `--skip-email`: disable email delivery (useful while testing).

The command prints the literature review to STDOUT. The same text can be saved with `--output` or delivered by email when SMTP settings are provided.

### Email delivery

Set these environment variables before running the command if you want the agent to send the review automatically:

- `AIR_AGENT_SMTP_HOST` *(required)*
- `AIR_AGENT_SMTP_PORT` *(default `587`)*
- `AIR_AGENT_SMTP_USER` *(optional but required if authentication is needed)*
- `AIR_AGENT_SMTP_PASSWORD` *(optional)*
- `AIR_AGENT_EMAIL_FROM` *(defaults to `AIR_AGENT_SMTP_USER` if omitted)*
- `AIR_AGENT_EMAIL_TO` *(comma-separated list of recipients, required when host is set)*
- `AIR_AGENT_SMTP_USE_TLS` *(set to `false` to disable STARTTLS, defaults to true)*
- `AIR_AGENT_CONTACT_EMAIL` *(optional, passed to PubMed/Crossref for polite API usage)*

Example:

```bash
export AIR_AGENT_SMTP_HOST=smtp.gmail.com
export AIR_AGENT_SMTP_PORT=587
export AIR_AGENT_SMTP_USER=example@gmail.com
export AIR_AGENT_SMTP_PASSWORD='app-specific-password'
export AIR_AGENT_EMAIL_FROM=example@gmail.com
export AIR_AGENT_EMAIL_TO=recipient@example.com

PYTHONPATH=src python3 -m air_pollution_agent.cli
```

If email variables are not set, the agent completes normally and reports that delivery was skipped.

## How it works

1. Queries PubMed (via E-utilities) and Crossref for air pollution publications added within the chosen window.
2. Cleans the metadata, removes duplicates using DOI/title heuristics, and filters out off-topic Crossref results.
3. Builds a themed literature review with inline references and a reference list.
4. Emails the compiled review when SMTP credentials are available.

## Troubleshooting

- **Empty results**: occasionally no qualifying studies are added within a week. Try increasing `--days`.
- **SSL warning**: macOS may bundle LibreSSL with the system Python, which triggers a urllib3 warning. Using a virtual environment with an up-to-date Python build resolves it.
- **Email failures**: ensure your SMTP provider allows third-party access and that TLS/App Password requirements are satisfied.

## Next steps

- Extend `RELEVANCE_KEYWORDS` in `src/air_pollution_agent/data_sources.py` to broaden or narrow topical filtering.
- Adjust `THEME_KEYWORDS` in `src/air_pollution_agent/review_builder.py` to tailor review sections to your interests.
