# SchoolTinder

A Flask-based matching application.

## Branch Protection

The `main` branch is protected and requires administrator approval before merging. All changes must go through pull requests.

For detailed information about branch protection rules and how to configure them, see [.github/BRANCH_PROTECTION.md](.github/BRANCH_PROTECTION.md).

### Quick Setup

To apply branch protection rules automatically:

```bash
cd tools
export GITHUB_TOKEN="your_personal_access_token"
./setup-branch-protection.sh
```

## Development

This project uses Flask for the backend.

### Installation

```bash
pip install -e .
```

### Running the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`.
