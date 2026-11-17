# Repository setup (maintainers)

The issue forms, pull request template and checks are in `.github/`. GitHub settings can't be stored in files, so these are set once by the repository owner.

## 1. Protect the `main` branch

*Settings → Branches → Add branch ruleset* (or *Add classic branch protection rule*) for `main`:

- **Require a pull request before merging**, with at least 1 approval.
- **Require status checks to pass**: `check-issue-link` and `validate` (they appear in the list after the first pull request has run them).
- **Block force pushes** and **Restrict deletions**.
- Optionally **Do not allow bypassing the above settings**, so the owner follows the same process.

With the GitHub CLI, run from the repository folder after the first push (replace `OWNER/REPO`):

```bash
gh api -X PUT repos/OWNER/REPO/branches/main/protection --input - <<'EOF'
{
  "required_status_checks": { "strict": true, "contexts": ["check-issue-link", "validate"] },
  "enforce_admins": false,
  "required_pull_request_reviews": { "required_approving_review_count": 1 },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
```

## 2. Labels

The issue forms use `bug`, `enhancement` and `triage` (the first two exist by default). Create the others:

```bash
gh label create triage   --color FBCA04 --description "Waiting for a maintainer"
gh label create accepted --color 0E8A16 --description "Approved – a pull request can be opened"
```

## 3. General settings

*Settings → General*:

- **Features**: keep *Issues* on; turn *Wiki* off if not needed.
- **Pull Requests**: enable *Allow squash merging*, *Always suggest updating pull request branches* and *Automatically delete head branches*.
