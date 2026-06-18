#!/usr/bin/env python3
"""
File GitHub issues for notebooks that failed execution.

For each failing notebook:
  - Check whether an open issue with the same title already exists.
  - If not, create a new issue tagged with 'bug' and 'notebook-failure'.
  - If yes, skip to avoid duplicate noise.

Requires: gh CLI authenticated via GH_TOKEN environment variable.
"""

import argparse
import json
import os
import subprocess
import sys


LABEL_BUG = "bug"
LABEL_NOTEBOOK = "notebook-failure"


def gh(*args):
    """Run a gh CLI command and return stdout as a string."""
    result = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def ensure_label(repo, name, color, description):
    """Create the label if it doesn't already exist."""
    rc, _, _ = gh("label", "view", name, "--repo", repo)
    if rc != 0:
        gh(
            "label", "create", name,
            "--repo", repo,
            "--color", color,
            "--description", description,
        )


def open_issue_exists(repo, title):
    """Return True if an open issue with this exact title already exists."""
    rc, out, _ = gh(
        "issue", "list",
        "--repo", repo,
        "--state", "open",
        "--label", LABEL_NOTEBOOK,
        "--json", "title",
        "--limit", "200",
    )
    if rc != 0:
        return False
    try:
        issues = json.loads(out)
        return any(i["title"] == title for i in issues)
    except (json.JSONDecodeError, KeyError):
        return False


def read_error(error_dir, notebook_name):
    """Read the captured stderr for a notebook (last ~4000 chars)."""
    stem = notebook_name.replace(".ipynb", "")
    err_file = os.path.join(error_dir, f"{stem}.json.err")
    if os.path.exists(err_file):
        with open(err_file) as f:
            content = f.read()
        if len(content) > 4000:
            content = "...(truncated)...\n" + content[-4000:]
        return content.strip()
    return "(no error output captured)"


def main():
    parser = argparse.ArgumentParser(description="File GitHub issues for failing notebooks.")
    parser.add_argument("--failed-list", required=True, help="File with one failing notebook name per line.")
    parser.add_argument("--error-dir", required=True, help="Directory containing captured stderr files.")
    parser.add_argument("--repo", required=True, help="GitHub repo in owner/name format.")
    args = parser.parse_args()

    if not os.environ.get("GH_TOKEN"):
        print("ERROR: GH_TOKEN environment variable not set.", file=sys.stderr)
        sys.exit(1)

    # Ensure required labels exist
    ensure_label(args.repo, LABEL_BUG, "d73a4a", "Something isn't working")
    ensure_label(args.repo, LABEL_NOTEBOOK, "0075ca", "Jupyter notebook execution failure")

    with open(args.failed_list) as f:
        failing = [line.strip() for line in f if line.strip()]

    if not failing:
        print("No failing notebooks listed.")
        return

    filed = 0
    skipped = 0
    for notebook in failing:
        title = f"Notebook failure: {notebook}"
        if open_issue_exists(args.repo, title):
            print(f"SKIP (duplicate): {title}")
            skipped += 1
            continue

        error_output = read_error(args.error_dir, notebook)
        body = (
            f"## Notebook execution failed\n\n"
            f"**Notebook:** `{notebook}`\n\n"
            f"This issue was automatically filed by the [Test Notebooks workflow]"
            f"(../../actions/workflows/test-notebooks.yml) "
            f"after the notebook failed to execute against the current environment "
            f"(QuTiP ≥ 5, Python ≥ 3.11).\n\n"
            f"### Error output\n\n"
            f"```\n{error_output}\n```\n\n"
            f"### Next steps\n"
            f"- Review the error above and update the notebook to be compatible with the current QuTiP version.\n"
            f"- Close this issue once the notebook executes cleanly.\n"
        )

        rc, out, err = gh(
            "issue", "create",
            "--repo", args.repo,
            "--title", title,
            "--body", body,
            "--label", f"{LABEL_BUG},{LABEL_NOTEBOOK}",
        )
        if rc == 0:
            print(f"FILED: {title} -> {out}")
            filed += 1
        else:
            print(f"ERROR filing issue for {notebook}: {err}", file=sys.stderr)

    print(f"\nDone. Filed: {filed}, Skipped (duplicate): {skipped}")


if __name__ == "__main__":
    main()
