# SchoolTinder

A Flask-based matching application for schools.

## Git Tutorial for Beginners

This project uses Git for version control and follows a **feature branch workflow**. This means we create separate branches for each new feature or fix, then merge them back to the main branch when complete.

### First Time Setup

#### 1. Clone the Repository
```bash
# Clone the repository to your computer
git clone https://github.com/DiscoveryFox/SchoolTinder.git

# Navigate into the project folder
cd SchoolTinder
```

#### 2. Configure Git (First Time Only)
```bash
# Set your name (this will appear in commits)
git config --global user.name "Your Name"

# Set your email
git config --global user.email "your.email@example.com"
```

### Working with Feature Branches

#### Step 1: Start Working on a New Feature

Before you start coding, always create a new branch for your feature:

```bash
# Make sure you're on the main branch and it's up to date
git checkout main
git pull origin main

# Create and switch to a new branch for your feature
# Use a descriptive name like: feature/add-login or fix/profile-bug
git checkout -b feature/your-feature-name
```

#### Step 2: Make Your Changes

Now you can edit files and make your changes. As you work:

```bash
# Check which files you've modified
git status

# See the specific changes you made
git diff
```

#### Step 3: Save Your Changes (Commit)

When you've made progress, save your work with commits:

```bash
# Add specific files to staging
git add filename.py

# Or add all changed files
git add .

# Commit with a clear message describing what you did
git commit -m "Add user login functionality"
```

**Tip**: Make small, frequent commits with clear messages. This makes it easier to track changes and fix issues later.

#### Step 4: Push Your Branch to GitHub

```bash
# Push your branch to GitHub (first time)
git push -u origin feature/your-feature-name

# For subsequent pushes to the same branch
git push
```

#### Step 5: Create a Pull Request

1. Go to the GitHub repository in your web browser
2. You'll see a prompt to create a Pull Request for your branch
3. Click "Compare & pull request"
4. Write a description of your changes
5. Click "Create pull request"
6. Wait for code review and approval
7. Once approved, your changes will be merged into main!

### Common Commands Cheat Sheet

```bash
# Check current status
git status

# See commit history
git log

# Switch to an existing branch
git checkout branch-name

# See all branches
git branch -a

# Pull latest changes from main
git pull origin main

# Discard changes to a specific file
git checkout -- filename

# Update your branch with latest changes from main
git checkout feature/your-feature-name
git merge main
```

### Best Practices

1. **Always create a new branch** for each feature or bug fix
2. **Pull before you push** to get the latest changes
3. **Write clear commit messages** that explain what and why
4. **Commit often** - small commits are better than large ones
5. **Don't work directly on main** - always use feature branches
6. **Keep your branch up to date** by regularly merging main into your branch

### Troubleshooting

#### "I made changes to the wrong branch!"
```bash
# Save your changes temporarily
git stash

# Switch to the correct branch
git checkout correct-branch-name

# Apply your saved changes
git stash pop
```

#### "I have merge conflicts!"
1. Open the files with conflicts (Git will mark them)
2. Look for sections marked with `<<<<<<<`, `=======`, and `>>>>>>>`
3. Edit the file to keep the correct version
4. Remove the conflict markers
5. Add and commit the resolved files:
```bash
git add resolved-file.py
git commit -m "Resolve merge conflict"
```

#### "I want to undo my last commit"
```bash
# Undo commit but keep changes
git reset --soft HEAD~1

# Undo commit and discard changes (careful!)
git reset --hard HEAD~1
```

### Need Help?

- Ask your team members
- Check [GitHub's Git Guide](https://docs.github.com/en/get-started/using-git)
- Use `git --help` or `git command --help` for command documentation

---

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will be available at `http://localhost:5000`
