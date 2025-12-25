#!/usr/bin/env python
import subprocess
import re
import argparse


def run_git_command(command):
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip()


def get_current_branch():
    return run_git_command(["git", "branch", "--show-current"])


def get_staged_diff():
    return run_git_command(["git", "diff", "--staged"])


def parse_branch(branch):
    parts = branch.split("/")

    commit_type = "chore"
    ticket = None
    description = branch.replace("-", " ")

    if len(parts) > 1:
        commit_type = parts[0]
        rest = parts[1]

        ticket_match = re.search(r"[A-Z]+-\d+", rest)
        if ticket_match:
            ticket = ticket_match.group()

        description = rest.replace(ticket or "", "")
        description = description.replace("-", " ").strip()

    return commit_type, ticket, description


def summarize_diff(diff):
    files = {}

    current_file = None
    added = removed = 0

    for line in diff.splitlines():
        if line.startswith("diff --git"):
            if current_file:
                files[current_file] = (added, removed)

            parts = line.split(" ")
            current_file = parts[-1].replace("b/", "")
            added = removed = 0

        elif line.startswith("+") and not line.startswith("+++"):
            added += 1
        elif line.startswith("-") and not line.startswith("---"):
            removed += 1

    if current_file:
        files[current_file] = (added, removed)

    return files



def generate_commit_message(commit_type, ticket, description, files):
    header = commit_type
    if ticket:
        header += f"({ticket})"
    header += f": {description}"

    body = ""
    if files:
        body += "\n\nAffected files:\n"
        for f, (add, rem) in files.items():
            body += f"- {f} (+{add} / -{rem})\n"

    return header + body


def copy_to_clipboard(text):
    subprocess.run("clip", input=text, text=True)

def parse_args():
    parser = argparse.ArgumentParser(description="Generate structured git commit messages.")
    parser.add_argument("--dry-run", action="store_true", help="Preview commit message only")
    parser.add_argument("--commit", action="store_true", help="Automatically create git commit")
    return parser.parse_args()

def git_commit(message):
    subprocess.run(["git", "commit", "-m", message])


def main():
    args = parse_args()

    branch = get_current_branch()
    diff = get_staged_diff()

    if not diff:
        print("No staged changes found.")
        return

    commit_type, ticket, description = parse_branch(branch)
    files = summarize_diff(diff)

    message = generate_commit_message(
        commit_type,
        ticket,
        description,
        files
    )

    print("\nSuggested Commit Message:\n")
    print(message)

    if args.dry_run:
        print("\nDry run enabled — no commit created.")
        return

    copy_to_clipboard(message)
    print("\nCommit message copied to clipboard.")

    if args.commit:
        git_commit(message)
        print("Commit created.")


if __name__ == "__main__":
    main()
