# Git Workflow & Branching Strategy

## 🌿 Branch Strategy for Team

### **Main Branch**
- `master` - The main branch (stable, working code only)

### **Feature Branches (Each Person Creates Their Own)**

| Team Member | Branch Name | Purpose |
|------------|-------------|---------|
| **Mitali** | `feature/mitali-erd-prediction` | ERD Diagram + Prediction Script |
| **Raissa** | `feature/raissa-mysql-population` | MySQL Database Population |
| **Alliance** | `feature/alliance-crud-api` | FastAPI CRUD Endpoints |
| **Innocente** | `feature/innocente-mongodb` | MongoDB Implementation |

---

## 📋 Git Workflow - Step by Step

### **Step 1: Create Your Branch**

```bash
# First, make sure you're on master and have latest changes
git checkout master
git pull origin master

# Create and switch to your feature branch
# MITALI:
git checkout -b feature/mitali-erd-prediction

# RAISSA:
git checkout -b feature/raissa-mysql-population

# ALLIANCE:
git checkout -b feature/alliance-crud-api

# INNOCENTE:
git checkout -b feature/innocente-mongodb
```

---

### **Step 2: Work on Your Tasks**

```bash
# Make changes to your files...
# Create new files...
# Test your code...

# Check what files you changed
git status

# Add your files
git add your_files.py

# Commit with clear message (remember: you need 4+ commits!)
git commit -m "[Component] Description of what you did"
```

---

### **Step 3: Push Your Branch to GitHub**

```bash
# Push your feature branch
# MITALI:
git push origin feature/mitali-erd-prediction

# RAISSA:
git push origin feature/raissa-mysql-population

# ALLIANCE:
git push origin feature/alliance-crud-api

# INNOCENTE:
git push origin feature/innocente-mongodb
```

---

### **Step 4: Keep Your Branch Updated**

```bash
# Regularly pull changes from master to avoid conflicts
git checkout master
git pull origin master

# Switch back to your branch
git checkout feature/your-branch-name

# Merge master into your branch
git merge master

# If there are conflicts, resolve them and commit
git add .
git commit -m "[Merge] Merged latest changes from master"
```

---

### **Step 5: Create Pull Request (Optional but Recommended)**

1. Go to GitHub: https://github.com/IrutingaboRaissa/Formative1_Database_predictionPipeline_group10
2. Click "Pull requests" → "New pull request"
3. Select your branch
4. Add description of what you did
5. Request review from team members
6. After approval, merge to master

**OR** merge directly:

```bash
# When your feature is complete and tested
git checkout master
git pull origin master
git merge feature/your-branch-name
git push origin master
```

---

## 🎯 Example Workflow for Mitali

```bash
# 1. Create your branch
git checkout -b feature/mitali-erd-prediction

# 2. Create ERD diagram
# - Design ERD using dbdiagram.io
# - Export to docs/ERD.png

git add docs/ERD.png
git commit -m "[ERD] Add database ERD diagram with all tables and relationships"
git push origin feature/mitali-erd-prediction

# 3. Start prediction script
mkdir -p prediction
# Create prediction/fetch_and_predict.py

git add prediction/fetch_and_predict.py
git commit -m "[Prediction] Add script to fetch latest data from API"
git push origin feature/mitali-erd-prediction

# 4. Add model loading functionality
# Edit prediction/model_loader.py

git add prediction/model_loader.py
git commit -m "[Prediction] Implement ML model loading and preprocessing"
git push origin feature/mitali-erd-prediction

# 5. Complete prediction logging
# Update prediction/fetch_and_predict.py

git add prediction/fetch_and_predict.py
git commit -m "[Prediction] Add prediction logging to database via API"
git push origin feature/mitali-erd-prediction

# 6. Merge to master when complete
git checkout master
git pull origin master
git merge feature/mitali-erd-prediction
git push origin master
```

---

## ✅ Commit Best Practices

### **Good Commits (Clear, Specific)**
✅ `[ERD] Create database ERD diagram with 5 tables`  
✅ `[Prediction] Add data fetching from API endpoint`  
✅ `[Prediction] Implement model preprocessing pipeline`  
✅ `[Prediction] Add error handling for missing data`  
✅ `[MongoDB] Create MongoDB connection and setup script`  
✅ `[MongoDB] Add data population script with validation`  
✅ `[API] Implement POST endpoint for student creation`  
✅ `[API] Add GET endpoints for fetching students`  
✅ `[Database] Create MySQL population script`  

### **Bad Commits (Avoid These)**
❌ `Update`  
❌ `Fixed stuff`  
❌ `Changes`  
❌ `Work in progress`  
❌ `asdf`  

---

## 🔄 Handling Conflicts

If you get a merge conflict:

```bash
# 1. Git will show conflict markers in files:
<<<<<<< HEAD
Your changes
=======
Someone else's changes
>>>>>>> master

# 2. Edit the file to keep what you need

# 3. Remove the conflict markers

# 4. Add and commit
git add conflicted_file.py
git commit -m "[Fix] Resolve merge conflict in filename"
```

---

## 📊 Checking Your Commits

```bash
# See your commit history
git log --oneline

# See commits on your branch only
git log master..feature/your-branch-name --oneline

# Count your commits
git log master..feature/your-branch-name --oneline | wc -l
```

---

## ⚠️ Important Rules

1. **NEVER commit directly to master** (until your feature is complete)
2. **Always pull before pushing** to avoid conflicts
3. **Commit often** (you need 4+ meaningful commits!)
4. **Use clear commit messages** with [Component] prefix
5. **Test your code** before pushing
6. **Don't commit .env files** (use .env.example instead)
7. **Don't commit large files** (like datasets, unless necessary)

---

## 🆘 Emergency Commands

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes (careful!)
git reset --hard HEAD

# See what branch you're on
git branch

# Switch branches
git checkout branch-name

# Delete a branch (after merged)
git branch -d feature/your-branch-name

# Force push (use carefully!)
git push origin your-branch --force
```

---

## 📝 Summary for Each Team Member

### **Mitali:**
```bash
git checkout -b feature/mitali-erd-prediction
# Work on ERD + Prediction
git push origin feature/mitali-erd-prediction
# Merge to master when done
```

### **Raissa:**
```bash
git checkout -b feature/raissa-mysql-population
# Work on MySQL population
git push origin feature/raissa-mysql-population
# Merge to master when done
```

### **Alliance:**
```bash
git checkout -b feature/alliance-crud-api
# Work on FastAPI CRUD
git push origin feature/alliance-crud-api
# Merge to master when done
```

### **Innocente:**
```bash
git checkout -b feature/innocente-mongodb
# Work on MongoDB
git push origin feature/innocente-mongodb
# Merge to master when done
```

---

## 🎓 Why Use Branches?

✅ **Prevents conflicts** - Everyone works independently  
✅ **Easy to review** - Can see exactly what each person did  
✅ **Safe to experiment** - Won't break main code  
✅ **Professional workflow** - Industry standard practice  
✅ **Clear history** - Easy to track who did what  

---

**Questions? Check with the team or ask in the group chat!**
