# Branch Protection Rules for Main Branch

This document describes the branch protection rules configured for the `main` branch.

## Required Settings

### Branch Protection Rules
The following settings must be configured for the `main` branch:

1. **Require pull request reviews before merging**
   - Required approving reviews: **1**
   - Dismiss stale pull request approvals when new commits are pushed: Optional
   - Require review from Code Owners: Optional

2. **Require pull request approval before merging**
   - At least 1 approval from users with write access is required
   - In most cases, repository administrators are the ones with write access
   - For stricter control, consider using CODEOWNERS to specify required reviewers

3. **Do not allow bypassing the above settings**
   - Enforce all configured restrictions for administrators: **Enabled**
   - This ensures that even administrators must follow the pull request review process

4. **Additional recommended settings**:
   - Require status checks to pass before merging (if CI/CD is configured)
   - Require branches to be up to date before merging
   - Require conversation resolution before merging
   - Do not allow force pushes
   - Do not allow deletions

## How to Apply These Settings

### Option 1: Manual Configuration (GitHub UI)
1. Go to your repository on GitHub
2. Click on **Settings** → **Branches**
3. Under "Branch protection rules", click **Add rule**
4. Enter `main` as the branch name pattern
5. Enable the following:
   - ✅ Require a pull request before merging
   - ✅ Require approvals (set to 1)
   - ✅ Restrict who can dismiss pull request reviews (optional)
   - ✅ Require review from Code Owners (optional, if you have a CODEOWNERS file)
6. Click **Create** or **Save changes**

### Option 2: Using the GitHub API (Automated)
Use the provided script in `tools/setup-branch-protection.sh` to automatically apply these rules.

**Prerequisites:**
- GitHub Personal Access Token with `repo` scope
- `curl` installed

**Usage:**
```bash
cd tools
export GITHUB_TOKEN="your_personal_access_token"
./setup-branch-protection.sh
```

## Verifying the Configuration

Once configured, you can verify by:
1. Trying to push directly to `main` (should be blocked)
2. Creating a pull request and trying to merge without approval (should be blocked)
3. Having an admin approve the PR and then merge (should succeed)

## Notes

- These settings ensure that all changes to the `main` branch go through a pull request review process
- At least one user with write access must approve changes before they can be merged
- This helps maintain code quality and prevents accidental direct pushes to the main branch
- For stricter control where only specific users can approve, create a `.github/CODEOWNERS` file and enable "Require review from Code Owners" in the branch protection settings
