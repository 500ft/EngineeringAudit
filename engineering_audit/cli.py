"""Command-line entry point for engineering-audit.

Two subcommands:

- ``engineering-audit audit <case_file> [-o OUT]`` — audit a benchmark case file and
  write a Markdown report (the original behavior).
- ``engineering-audit eval <dir> [...] [--report OUT]`` — audit every benchmark case
  under one or more directories and print a pass/fail summary. A case passes
  when the *computed* detected failure modes equal the case's expected modes
  (so a no-failure control that triggers any check is a false positive and
  fails). Exits nonzero on any failure — this is the CI regression gate.

For backward compatibility, if the first argument is not a known subcommand the
invocation is treated as ``audit`` (so ``engineering-audit path/to/case.md`` still works).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .case_loader import CaseLoadError, load_case_file
from .pressure_vessel import audit_case
from .report_writer import write_markdown_report


SUBCOMMANDS = {"audit", "eval"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="engineering-audit",
        description="Audit retained engineering calculation cases and reproduce benchmark results.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser(
        "audit",
        help="Audit a benchmark case file and write a markdown report.",
    )
    audit.add_argument(
        "case_file",
        type=Path,
        help="Path to a benchmark case markdown file (with a fenced JSON metadata block).",
    )
    audit.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Path to write the markdown report to. Defaults to reports/<case_id>.md.",
    )

    eval_cmd = subparsers.add_parser(
        "eval",
        help=(
            "Audit every benchmark case under the given directories and print a "
            "pass/fail summary. Exits nonzero on any failed case (CI gate)."
        ),
    )
    eval_cmd.add_argument(
        "directories",
        type=Path,
        nargs="+",
        help="Directories to scan recursively for case markdown files.",
    )
    eval_cmd.add_argument(
        "--report",
        type=Path,
        default=None,
        help="Optional path to write a markdown summary report to.",
    )

    return parser


def run(case_file: Path, output: Path | None) -> Path:
    case = load_case_file(case_file)
    result = audit_case(case)

    if output is None:
        output_dir = Path("reports")
        return write_markdown_report(result, output_dir)

    report_path = write_markdown_report(result, output.parent)
    default_path = output.parent / f"{result.case_id}.md"
    if default_path != output:
        default_path.replace(output)
        return output
    return report_path


def _run_audit(args: argparse.Namespace) -> int:
    try:
        report_path = run(args.case_file, args.output)
    except CaseLoadError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote report to {report_path}")
    return 0


_NON_CASE_NAMES = {"readme.md", "template.md"}


def _run_eval(args: argparse.Namespace) -> int:
    case_files: list[Path] = []
    for directory in args.directories:
        if not directory.is_dir():
            print(f"error: not a directory: {directory}", file=sys.stderr)
            return 2
        case_files.extend(
            p for p in sorted(directory.rglob("*.md"))
            if p.name.lower() not in _NON_CASE_NAMES
        )
    if not case_files:
        print("error: no case files found", file=sys.stderr)
        return 2

    rows: list[tuple[str, str, str]] = []      # (case_id, verdict, detail)
    n_pass = n_fail = n_skip = 0
    for path in case_files:
        try:
            case = load_case_file(path)
        except CaseLoadError as exc:
            rows.append((path.name, "ERROR", str(exc)))
            n_fail += 1
            continue
        result = audit_case(case)
        if result.skipped:
            n_skip += 1
            rows.append((result.case_id, "SKIP", result.skip_reason or ""))
        elif result.passed:
            n_pass += 1
            rows.append((result.case_id, "PASS",
                         f"detected == expected: {result.detected_failure_modes or '[]'}"))
        else:
            n_fail += 1
            rows.append((result.case_id, "FAIL",
                         f"expected {sorted(set(result.expected_failure_modes))}, "
                         f"detected {result.detected_failure_modes}"))

    width = max(len(r[0]) for r in rows)
    lines = [f"{'case':<{width}}  verdict  detail",
             f"{'-' * width}  -------  ------"]
    lines += [f"{cid:<{width}}  {verdict:<7}  {detail}" for cid, verdict, detail in rows]
    summary = (f"{n_pass} passed, {n_fail} failed, {n_skip} skipped "
               f"(pass = computed detected modes equal expected modes)")
    lines.append(summary)
    print("\n".join(lines))

    if args.report is not None:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        md = ["# engineering-audit benchmark eval", "",
              "| case | verdict | detail |", "| --- | --- | --- |"]
        md += [f"| `{cid}` | {verdict} | {detail} |" for cid, verdict, detail in rows]
        md += ["", summary, ""]
        args.report.write_text("\n".join(md), encoding="utf-8")
        print(f"Wrote report to {args.report}")

    return 1 if n_fail else 0


def main(argv: list[str] | None = None) -> int:
    raw_args = list(sys.argv[1:] if argv is None else argv)
    # Backward compatibility: bare `engineering-audit <case_file>` still means audit.
    if raw_args and raw_args[0] not in SUBCOMMANDS and not raw_args[0].startswith("-"):
        raw_args = ["audit", *raw_args]

    parser = build_parser()
    args = parser.parse_args(raw_args)

    if args.command == "eval":
        return _run_eval(args)
    return _run_audit(args)


if __name__ == "__main__":
    sys.exit(main())
