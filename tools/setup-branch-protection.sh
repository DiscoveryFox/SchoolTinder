#!/bin/bash

# Script to set up branch protection rules for the main branch
# This script uses the GitHub API to configure branch protection
# 
# Prerequisites:
#   - GitHub Personal Access Token with 'repo' scope
#   - Set the GITHUB_TOKEN environment variable
#   - curl installed
#
# Usage:
#   export GITHUB_TOKEN="your_token_here"
#   ./setup-branch-protection.sh

set -e

# Configuration
REPO_OWNER="DiscoveryFox"
REPO_NAME="SchoolTinder"
BRANCH="main"
API_URL="https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/branches/${BRANCH}/protection"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if GITHUB_TOKEN is set
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}Error: GITHUB_TOKEN environment variable is not set${NC}"
    echo "Please set it with: export GITHUB_TOKEN=\"your_token_here\""
    exit 1
fi

echo -e "${YELLOW}Setting up branch protection for ${BRANCH} branch...${NC}"

# Branch protection configuration
PROTECTION_CONFIG='{
  "required_status_checks": null,
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "dismissal_restrictions": {},
    "dismiss_stale_reviews": false,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 1,
    "require_last_push_approval": false,
    "bypass_pull_request_allowances": {}
  },
  "restrictions": null,
  "required_linear_history": false,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "block_creations": false,
  "required_conversation_resolution": false,
  "lock_branch": false,
  "allow_fork_syncing": false
}'

# Apply branch protection
echo "Applying branch protection rules..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  "${API_URL}" \
  -d "${PROTECTION_CONFIG}")

# Extract HTTP status code (last line)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 201 ]; then
    echo -e "${GREEN}✓ Branch protection rules successfully applied to ${BRANCH} branch!${NC}"
    echo ""
    echo "The following rules are now active:"
    echo "  • Pull requests are required before merging"
    echo "  • At least 1 approval is required"
    echo "  • Force pushes are not allowed"
    echo "  • Branch deletions are not allowed"
    echo ""
    echo -e "${GREEN}Setup complete!${NC}"
else
    echo -e "${RED}✗ Failed to apply branch protection rules${NC}"
    echo "HTTP Status Code: ${HTTP_CODE}"
    echo "Response:"
    echo "$BODY" | head -20
    exit 1
fi
