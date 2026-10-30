#!/usr/bin/env python3
"""Verify the supplied file manifests and reproduce the three small exact checks.

Uses Python 3.8+ and the standard library. This does not verify the full paper.
"""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = ("SHA256SUMS.txt", "REPOSITORY_SHA256SUMS.txt")
CHECKS = (
    ("p2_complete", "p2_completion_checks", 20, "all_passed"),
    ("p2_local", "p2_exact_checks", 41, "all_checks_passed"),
    ("p3_local", "p3_exact_checks", 26, "all_checks_passed"),
)


class VerificationError(Exception):
    pass


def verify_manifest(name):
    seen = set()
    for line_number, line in enumerate((ROOT / name).read_text(encoding="utf-8").splitlines(), 1):
        digest, separator, filename = line.partition("  ")
        if not separator or not re.fullmatch(r"[0-9a-f]{64}", digest) or not filename:
            raise VerificationError("{}:{}: invalid checksum entry".format(name, line_number))
        relative = PurePosixPath(filename)
        if relative.is_absolute() or ".." in relative.parts or filename in seen:
            raise VerificationError("{}:{}: unsafe or duplicate path".format(name, line_number))
        target = (ROOT / relative).resolve()
        try:
            target.relative_to(ROOT)
        except ValueError:
            raise VerificationError("{}: path leaves the repository".format(filename))
        if not target.is_file():
            raise VerificationError("{}: missing file".format(filename))
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != digest:
            raise VerificationError("{}: SHA-256 mismatch".format(filename))
        seen.add(filename)
    if not seen:
        raise VerificationError("{}: empty manifest".format(name))
    print("PASS: {} ({} files)".format(name, len(seen)))


def reproduce_checks():
    results = ROOT / "results"
    results.mkdir(exist_ok=True)
    total = 0
    with tempfile.TemporaryDirectory(prefix="verification-", dir=str(results)) as temporary:
        for folder, name, expected_count, success_field in CHECKS:
            source = ROOT / "local_checks" / folder / (name + ".py")
            output = Path(temporary) / (name + ".json")
            command = [sys.executable, "-I", str(source), "--output", str(output)]
            try:
                completed = subprocess.run(
                    command, cwd=str(ROOT), stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, universal_newlines=True, timeout=60,
                )
            except subprocess.TimeoutExpired:
                raise VerificationError("{}: exceeded 60 seconds".format(name))
            if completed.returncode != 0:
                raise VerificationError("{} failed:\n{}".format(name, completed.stdout))
            report = json.loads(output.read_text(encoding="utf-8"))
            retained = json.loads(source.with_suffix(".json").read_text(encoding="utf-8"))
            checks = report.get("checks") if isinstance(report, dict) else None
            if not isinstance(checks, list) or len(checks) != expected_count:
                raise VerificationError("{}: unexpected check count".format(name))
            if report.get(success_field) is not True or not all(
                isinstance(item, dict) and item.get("passed") is True for item in checks
            ):
                raise VerificationError("{}: a check did not pass".format(name))
            if report != retained:
                raise VerificationError("{}: generated JSON differs from retained report".format(name))
            total += len(checks)
            print("PASS: {} ({} checks; retained JSON matches)".format(name, len(checks)))
    print("PASS: {} exact checks in total".format(total))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--integrity-only", action="store_true",
                        help="verify both manifests without running the algebra scripts")
    args = parser.parse_args()
    try:
        for name in MANIFESTS:
            verify_manifest(name)
        if not args.integrity_only:
            reproduce_checks()
    except (VerificationError, OSError, ValueError) as error:
        print("FAIL: {}".format(error), file=sys.stderr)
        return 1
    print("Scope: file integrity and small exact algebra only; no full proof verification.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
