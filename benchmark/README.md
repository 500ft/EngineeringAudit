# Retained calculation-verifier cases

This collection reproduces the historical calculation-verifier report and
retains useful formula, provenance and false-positive regressions. The active
evidence-sufficiency work follows [ROADMAP.md](../ROADMAP.md) and its separate
[development example](../studies/evidence_sufficiency/README.md). The old
wild-capture campaign is retired; unfilled slots are retained skip fixtures.

## Folders

- `real_world/`: challenge-protocol model outputs, reviewer-synthesis controls
  and unfilled slots, distinguished by their metadata. This is not wild-use evidence.
- `synthetic/`: clearly labeled artificial cases for targeted coverage. This
  includes both single-mode failure cases (`syn-fm*`, `syn-arith-*`) and
  analytically/FEA-grade-validated **ground-truth controls** (`syn-kt-hole-*`,
  `syn-cantilever-*`) whose correct answer is computed independently in-repo by
  `engineering_audit.stress_concentration` and asserted in
  `tests/test_ground_truth_references.py`. The ground-truth controls are
  no-failure positives (`failure_modes: []`), `provenance_tier: synthetic`; they
  are not model runs and must never be described as wild captures.

Historical unfilled capture slots remain in `real_world/` with `status:
pending_capture`, but they must not be described as completed real LLM failures
until the raw model output is present. Anonymize coursework, names, dates, or
project details when needed, but do not fabricate provenance.

Current pressure-vessel real-run status:

- Complete no-failure controls: `rw-pressure-vessel-gemini-0001`,
  `rw-pressure-vessel-claude-0001`, and `rw-pressure-vessel-claude-0002`.
- Pending captures: `rw-pressure-vessel-gpt-0001` and
  `rw-pressure-vessel-gpt-0002`.

The completed controls are populated from reviewer-provided capture synthesis
because the raw transcripts are not present in the repository. Their metadata
must keep that limitation explicit.

## Case Format

Each benchmark case is a Markdown file with a fenced `json` metadata block near
the top. The JSON block follows `docs/schema_contract.md`; the surrounding
Markdown explains the case for human reviewers.

## Case Requirements

Each benchmark case should include:

- Original engineering problem.
- LLM prompt.
- LLM response.
- Correct solution or trusted expected result.
- Classified failure mode labels from `docs/failure_taxonomy.md`.
- Expected future verifier behavior.
- Notes on assumptions, units, and limitations.
- Tolerance policy reference.

## Naming

Use stable lowercase identifiers:

- `rw-pressure-vessel-gpt-0001.md`
- `syn-fm01-0001.md`
- `syn-fm07-0001.md`

## Minimum Review Checklist

- The source is clearly labeled as real-world, synthetic, or reference-correct.
- Units are explicit for all numerical values.
- The expected result is traceable to a trusted calculation.
- The failure mode is documented in the taxonomy.
- The expected verifier behavior is stated in plain language.
- Correct real captures with `failure_modes: []` remain useful: they protect
  against false positives such as treating accepted radius conventions as
  arithmetic errors.
