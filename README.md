# Full Gitflow Simulation

A hands-on project that walks through the complete Gitflow lifecycle:
**feature branch → PR → merge → release → hotfix**, plus a **pre-commit hook**
and **GitHub Actions CI**.

The app is a tiny Python calculator, so the focus stays on the Git workflow.

## Branch model

| Branch | Purpose |
| --- | --- |
| `main` | Production code. Every commit here is a release or hotfix, tagged `vX.Y.Z`. |
| `develop` | Integration branch. Features merge here first. |
| `feature/*` | One branch per feature, created from `develop`. |
| `release/*` | Release stabilisation, created from `develop`, merged to `main` and `develop`. |
| `hotfix/*` | Urgent production fix, created from `main`, merged to `main` and `develop`. |

## Setup

```bash
pip install -r requirements-dev.txt
bash scripts/install-hooks.sh     # installs the pre-commit hook
pytest -q
```

## Step-by-step walkthrough

### 1. Initialise the repo and create `develop`
```bash
git init -b main
git add -A && git commit -m "chore: initial project skeleton"
git branch develop
```

### 2. Add the pre-commit hook and CI
- `scripts/pre-commit` blocks direct commits to `main`, then runs flake8 and pytest.
- `.github/workflows/ci.yml` runs lint and tests on every push and pull request.

Because `.git/hooks` is not versioned, `scripts/install-hooks.sh` copies the hook in.

### 3. Feature branch and pull request
```bash
git checkout develop
git checkout -b feature/multiply
# ...edit code and tests...
git add -A && git commit -m "feat: add multiply function with test"
git push -u origin feature/multiply   # then open a PR into develop on GitHub
```
Locally the PR is simulated with a no-fast-forward merge so the merge commit stays visible:
```bash
git checkout develop
git merge --no-ff feature/multiply -m "Merge pull request #1 from feature/multiply"
git branch -d feature/multiply
```

### 4. Release
```bash
git checkout -b release/0.2.0 develop
echo "0.2.0" > VERSION && git commit -am "chore: bump version to 0.2.0"
git checkout main    && git merge --no-ff release/0.2.0
git tag -a v0.2.0 -m "v0.2.0"
git checkout develop && git merge --no-ff release/0.2.0
git branch -d release/0.2.0
```

### 5. Hotfix
`divide` crashes on division by zero in production, so fix it straight from `main`:
```bash
git checkout -b hotfix/0.2.1 main
# ...fix + test + bump VERSION to 0.2.1...
git checkout main    && git merge --no-ff hotfix/0.2.1
git tag -a v0.2.1 -m "v0.2.1"
git checkout develop && git merge --no-ff hotfix/0.2.1   # don't lose the fix
git branch -d hotfix/0.2.1
```

### 6. Inspect the history
```bash
git log --oneline --graph --all --decorate
git tag
```

## Pre-commit hook behaviour

```text
$ git commit -m "oops"        # while on main
pre-commit: direct commits to 'main' are not allowed.
```

On any other branch it runs `flake8` and `pytest`, and the commit is rejected if either fails.

## Pushing to GitHub

```bash
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main develop
git push origin --tags
```
