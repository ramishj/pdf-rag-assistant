# 🚀 Git Commands Guide

## **📋 Common Git Operations**

### **🔄 Daily Workflow**

```bash
# Check status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Your commit message here"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main
```

### **🌿 Branch Management**

```bash
# Create new branch
git checkout -b feature-name

# Switch to existing branch
git checkout branch-name

# List all branches
git branch -a

# Delete local branch
git branch -d branch-name
```

### **📁 Repository Setup**

```bash
# Add remote origin
git remote add origin https://github.com/username/repo-name.git

# Check remote configuration
git remote -v

# Change remote URL
git remote set-url origin https://github.com/username/new-repo-name.git
```

### **🔧 Troubleshooting**

```bash
# Reset to last commit (discard changes)
git reset --hard HEAD

# Abort rebase
git rebase --abort

# Clean untracked files
git clean -fd

# View commit history
git log --oneline
```

### **📤 Pushing to GitHub**

```bash
# First time setup
git remote add origin https://github.com/username/repo-name.git
git branch -M main
git push -u origin main

# Regular pushes
git push origin main
```

### **⚠️ Security Notes**

- **Never commit `.env` files** containing API keys
- **Use `.gitignore`** to exclude sensitive files
- **Check `git status`** before committing
- **Use descriptive commit messages**

---

**Remember**: Always check `git status` before committing to see what files will be included! 🎯

