# Preserved model captures

This tree contains the original challenge-protocol evidence for the calculation
verifier. It is historical development evidence, not a reserved evaluation set
for the current [roadmap](../ROADMAP.md). The capture campaign and CLI command
are retired.

- `prompts/`: original registered prompt bytes.
- `models/`: recorded model identifiers and versions.
- `runs/`: verbatim outputs, source records and ancillary artifacts with hashes.
- Dated session reports retain the original collection methods and limitations.

Do not rewrite these records. The offline source in `engineering_audit.capture`
remains available for provenance reproduction and hash verification. To verify
all committed records without calling a model:

```bash
pytest tests/test_committed_captures.py
```

Promoted benchmark cases reference the original artifacts. See
[provenance rules](../docs/capture_provenance.md) and
[the cleanup boundary](../docs/history/README.md#cleanup-boundary).
