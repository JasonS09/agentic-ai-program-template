# FAQ

## Why a separate `src/` directory?
Encourages reusable, tested utilities vs copying logic into each week.

## Do I need all provider API keys?
No. Start with one (e.g., OpenAI). Add others when exploring model behaviors.

## Should I commit evaluation outputs?
Small JSONL summaries: yes. Large raw logs: usually no (or compress / ignore).

## How do I reduce token costs?
- Trim unnecessary system prompt prose
- Use shorter model where fidelity not critical
- Cache repeated intermediate outputs

## What if a model hallucinates tools or functions?
Add explicit negative instruction: "Only use the listed tools" and validate JSON schema.

## When do I add tests?
As soon as you add reusable parsing, scoring, or template logic. Prompt text itself isn't tested, but functions around it can be.

## How to handle rate limits?
Implement exponential backoff + jitter. Queue batch evaluations rather than firing in parallel.

## Can I use local models?
Yes—consider small instruct models for iteration; document any differences vs cloud providers.

## How to log sensitive data safely?
Mask or hash PII fields before logging; implement a redaction helper.

## How will my work be evaluated?
See `PROGRAM_OVERVIEW.md` rubric dimensions and weekly `rubric.md` files once added.
