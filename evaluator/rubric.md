# Rubric

## Strong

- Parses trace records without crashing on missing optional span fields.
- Scores final answer quality, tool path correctness, evidence grounding, loop behavior, escalation judgment, latency, and cost.
- Penalizes traces where the final answer is plausible but the tool path is unsafe.
- Requires citations to map to observed evidence when evidence is required.
- Detects repeated failed tool loops without penalizing useful bounded retries.
- Produces stable, machine-readable reports.

## Partial

- Scores final answer and some tool behavior but misses evidence or escalation.
- Detects loops only in simple public fixtures.
- Produces reports that are readable but not stable enough for grading.

## Weak

- Scores only final answer text.
- Hardcodes public trace IDs.
- Crashes on missing fields.
- Ignores tool failures, loops, evidence, escalation, cost, or latency.

