# Contributing Guidelines

These guidelines help participants keep a consistent, high-quality repository throughout the 12-Week Agentic AI Program.

## Branching Strategy

For most participants a single `develop` (or `main`) branch is acceptable. If you want isolation for experiments:
- `feat/weekX-*` for new weekly work
- `exp/*` for ephemeral experiments (may be squashed later)
- `refactor/*` for structural changes

## Commit Messages (Conventional Commits)
Use a clear prefix:
- `feat:` new functionality (week solution, tool, agent component)
- `chore:` maintenance / formatting / dependency updates
- `docs:` documentation only
- `refactor:` internal restructuring without changing behavior
- `fix:` bug fix
- `test:` add/update tests
- `exp:` experimental spike (optional)

Examples:
```
feat: add evaluation script for week3 tool outputs
refactor: extract prompt templating helper
```

## Pull Requests (Optional for Solo Repos)
If you fork this into a team environment:
- Keep PRs focused, < 400 LOC diff when possible
- Include: summary, screenshots (if UX), test plan
- Use draft status until ready

## Code Style
- Prefer Python 3.11+
- Ruff formatter (or Black) to enforce formatting
- Type hints for reusable `src/` code; solutions can be lighter early
- Avoid global state; pass config explicitly

## Prompts & Artifacts
- Keep iterative prompt variants in a `prompts/` subfolder or `PROMPT_PLAYBOOK.md`
- For major changes, note reasoning in `reflections.md`

## Tests
- Minimal but meaningful: cover core utilities, evaluation scoring, parsing
- Fast ( < 5s ). Defer slow integration tests.

## Evaluation Data
- Store golden testcases in JSON/CSV under `eval/fixtures/`
- Name schema keys clearly: `input`, `expected`, `metadata`

## Security & Safety
- Never commit real API keys (use `.env.example`)
- Redact PII in logs

## Performance & Cost Awareness
- Cache expensive calls if re-running evaluation loops
- Prefer smaller local models for iteration when possible

## Documentation Conventions
- Link cross-files using relative paths
- Use tables for comparative results

## Closing
Consistency > perfection. If unsure, lean toward clarity, short functions, and explicit naming. Enjoy building! 🚀
