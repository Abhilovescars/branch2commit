Branch2Commit

Branch2Commit is a lightweight, local-first Git workflow tool that generates structured, convention-compliant commit messages by deriving context from branch naming semantics and staged changes.

It is designed for teams that value predictable workflows, clear commit history, and zero reliance on AI or external services.

Why Branch2Commit?

Most commit message generators attempt to infer intent from code changes using AI.
Branch2Commit takes a deterministic approach instead:

Derives commit type and context from the current Git branch name

Extracts ticket IDs directly from branch semantics

Summarizes staged changes using Git diffs

Enforces a consistent commit message structure

This avoids hallucination, improves consistency, and keeps everything fully local.

Installation
> Note: Branch2Commit has no runtime dependencies beyond Python and Git.

Clone the repository and install locally:

pip install -e .


This makes the branch2commit command available in your environment.

Expected Branch Naming Convention

Branch2Commit assumes branches follow a simple convention:

<type>/<TICKET-ID>-short-description

Examples
feat/JIRA-101-add-risk-metrics
fix/BUG-42-null-check
chore/update-readme


Where:

type → feat, fix, chore, etc.

TICKET-ID → optional but recommended

description → short, hyphen-separated context

Step-by-Step Usage
1. Create or switch to a semantic branch
git checkout -b feat/JIRA-101-branch2commit-test

2. Make code changes

Edit or add files as usual.

3. Stage your changes
git add .


Branch2Commit only analyzes staged changes.

4. Generate a commit message preview
branch2commit --dry-run


This prints the suggested commit message without copying or committing anything.

5. Generate and copy the commit message
branch2commit


The generated message is automatically copied to your clipboard.

6. (Optional) Auto-commit
branch2commit --commit


This generates the message and creates the Git commit automatically.

Example Output
feat(JIRA-101): branch2commit test

Affected files:
- cli.py (+42 / -10)
- sometrandomfile.txt (+1 / -0)

Supported Flags
Flag	Description
--dry-run	Preview commit message only
--commit	Automatically create the Git commit
Design Principles

Deterministic — no AI, no guessing

Local-first — no external APIs or services

Workflow-aware — built around real Git usage

Minimal — solves one problem well

When to Use (and Not Use)
Good fit if you:

use ticket-based branch naming

care about consistent commit history

want predictable, explainable tooling

Not intended to:

replace AI commit generators

infer intent from complex diffs

manage Git workflows automatically

License

MIT