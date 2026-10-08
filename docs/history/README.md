# Preserved research and engineering history

The active question and plan are in [ROADMAP.md](../../ROADMAP.md).
These assets are retained for reproduction and reuse, not treated as results
of the new evidence-sufficiency study.

| Asset | Location and status |
| --- | --- |
| Removed research schedules | [v1 plan](https://github.com/500ft/engineering-audit/blob/6e1df808d2f928a2ed15e1e4ffe7533b324bf662/docs/v1_plan.md) and [previous roadmap](https://github.com/500ft/engineering-audit/blob/6e1df808d2f928a2ed15e1e4ffe7533b324bf662/docs/history/roadmap-before-v2-2026-10-06.md) at the pre-cleanup commit; superseded, not completed |
| Previous FEA narrative | [Preserved text](fea-before-correction-2026-10-06.md); contains overclaims corrected in the current FEA README |
| Original FEA records and figures | [runs](../../cadloop/fea/runs), retained byte-for-byte at stable paths; interpretation lives in [derived JSON](../../reports/fea-interpretation.json) |
| CAD calibration, re-drive and host evidence | [Evidence index](../../cadloop/evidence/README.md), [scaffold](../../cadloop/scaffold/README.md); useful machinery retained |
| Earlier calculation benchmark | [Cases](../../benchmark/README.md), [result](../../reports/benchmark-results.md), [captures](../../captures); original data and code retained |
| Prior repository narrative | [README at the pre-pivot main commit](https://github.com/500ft/engineering-audit/blob/6e55653/README.md) |

Historical assets stay at their original paths where moving them would break
provenance, scripts or links. This index is the history area for those assets.
Original record fields such as `status: ok` are interpreted in the correction;
they have not been rewritten into stronger evidence.

## Cleanup boundary

The pre-cleanup tree is [this commit](https://github.com/500ft/engineering-audit/tree/6e1df808d2f928a2ed15e1e4ffe7533b324bf662).
Obsolete schedules and the capture command are removed from the working tree;
Git history retains their source. The old prompt-hardening proposal and run
instructions on unfilled capture slots are removed. No directory-wide archival
move was made.

Consumer tracing covered imports, CLI dispatch, tests, CI workflows and local
documentation references. No workflow or test calls the retired capture CLI;
the evaluator, audit command and backward-compatible bare-file invocation remain.
The stale schedule files had documentation consumers only; those links now point
here. No current figure required deletion: the active plot is computed from the
retained matrix and historical FEA images are primary result views.

Specific retentions:

- `engineering_audit.capture` retains the offline record-writing source and
  verifier used by provenance/tampering tests and committed-capture checks.
  Removing the module would break evidence verification; replacing its writer
  with fabricated test records would weaken that regression coverage. The
  library has no model/network launcher. Its generated README no longer directs
  users to the removed command.
- `prompts/pressure_vessel_prompt_v1.md` retains the original prompt text because
  existing benchmark metadata references that path. Only campaign instructions
  were removed. Unfilled GPT slots retain their original JSON so evaluator skip
  behavior and the historical report still reproduce; they are not active tasks.
- The legacy audit/eval implementation, schemas, formula checks and full test
  suite reproduce retained benchmark results. Their CI gate remains enabled.
- CAD/FEA scripts, scaffold helpers, host guidance, calibration, primary records,
  contours and the corrected convergence interpreter remain useful reproducible
  assets. The CAD briefing documents use by other 500ft projects; no shared
  tooling, host interface or dependency was removed.
- Capture runs, registered prompt bytes, model metadata, dated session reports,
  source/license records and executed numeric results remain intact. The former
  FEA narrative remains explicitly labeled correction history.
