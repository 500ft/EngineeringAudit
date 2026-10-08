# Contributing

Follow [ROADMAP.md](ROADMAP.md), the only active plan. Current research concerns
claim-specific evidence sufficiency. The calculation verifier and capture library
remain for reproducing and checking retained evidence.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
```

## Checks

```bash
pytest
engineering-audit eval benchmark/
```

Both commands must pass. The batch evaluator is also a false-positive gate for
reference cases whose expected failure-mode set is empty.

## Evidence-sufficiency work

Use the claim, independent-reference and exposure prerequisites in the roadmap.
The public development example lives in `studies/evidence_sufficiency/`; its
full-tuple schema is not yet a claim-specific benchmark schema. Freeze reserved
families before reviewer or policy tuning. Keep historical results reproducible.

## Maintaining legacy calculation cases

1. Start from the appropriate template under `benchmark/`.
2. Use a stable lowercase case identifier.
3. Include explicit units, assumptions, expected values, and tolerances.
4. Record expected failure modes using `docs/failure_taxonomy.md`.
5. Add or update tests before changing verifier logic.
6. Keep synthetic, reviewer-authored, and captured model outputs in their
   respective provenance tiers.

Do not describe a pending slot as a completed capture, and do not create a raw
model transcript from a summary.

## Captured outputs

The capture CLI and wild-capture campaign are retired. Keep raw artifacts,
source records and registered prompts unchanged. `engineering_audit.capture`
remains the offline source for their record format and verification tests; it
does not call models. A new collection campaign requires its own authorization
and protocol. See [the capture index](captures/README.md).

## CAD loop

`cadloop/` needs a Windows host with SOLIDWORKS licensed, so only its oracle
tests run in CI. When changing it:

1. State which stage of [`docs/cad_fea_loop.md`](docs/cad_fea_loop.md) the change
   affects.
2. Keep the acceptance gate honest. A build is accepted only when measured mass
   properties match a declared oracle; a job without an oracle reports
   `"accepted": null`, never a pass.
3. Do not commit host configuration. Credentials live outside the repository;
   `cadloop/config.example.json` documents the shape with placeholders.
4. Do not commit retrieved run artifacts except as deliberate evidence. STEP
   files, previews, and per-job directories under `cadloop/runs/` are ignored.
5. Record newly observed host API behaviour in
   [`docs/solidworks_api_findings.md`](docs/solidworks_api_findings.md) rather
   than only working around it in code.

## Pull requests

List the cases added or changed, the failure modes affected, and the output of
both the test suite and `engineering-audit eval benchmark/`.
