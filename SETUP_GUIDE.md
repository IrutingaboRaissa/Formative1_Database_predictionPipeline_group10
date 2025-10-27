# Quick Setup Guide

## For Team Members: Mitali, Raissa, Alliance, Innocente

### Step 1: Clone the Repository (If Not Done)

```bash
git clone https://github.com/IrutingaboRaissa/Formative1_Database_predictionPipeline_group10.git
cd Formative1_Database_predictionPipeline_group10
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your database credentials
nano .env  # or use any text editor
```

**Important:** Update these in `.env`:
```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_actual_password
MYSQL_DATABASE=student_performance_db

MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=student_performance_nosql
```

### Step 4: Set Up MySQL Database

```bash
# Login to MySQL
mysql -u root -p

# Once logged in, execute the schema
source student_performance_db_schema.sql

# Or from command line:
mysql -u root -p < student_performance_db_schema.sql
```

### Step 5: Install MongoDB (If Not Installed)

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

**Windows/Mac:**
- Download from: https://www.mongodb.com/try/download/community
- Install and start MongoDB service

### Step 6: Verify Setup

```bash
# Test MySQL connection
mysql -u root -p -e "SHOW DATABASES;"

# Test MongoDB connection
mongosh
# or
mongo
```

### Step 7: Start Working on Your Task

Check `TASK_BREAKDOWN.md` to see:
- What tasks need to be completed
- Who is assigned to what
- How to make meaningful commits

### Git Workflow for Team

```bash
# Always pull latest changes before starting work
git pull origin master

# Create a branch for your feature (optional but recommended)
git checkout -b feature/your-name-task-name

# Make your changes...

# Check what files changed
git status

# Add your files
git add your_files.py

# Commit with meaningful message
git commit -m "[Component] Description of what you did"

# Push your changes
git push origin master
# or if you created a branch:
git push origin feature/your-name-task-name
```

### Example Good Commits:

```bash
git commit -m "[MongoDB] Create MongoDB setup and population script"
git commit -m "[API] Implement POST endpoint for creating students"
git commit -m "[Prediction] Add model loading and preprocessing functions"
git commit -m "[Database] Add MySQL data population script"
```

### Testing Your Work

```bash
# Run FastAPI server (once endpoints are created)
uvicorn app.main:app --reload

# Access API docs at:
# http://localhost:8000/docs

# Run Jupyter notebook
jupyter notebook Untitled8.ipynb

# Run prediction script (once created)
python prediction/fetch_and_predict.py
```

### Common Issues & Solutions

**Issue:** MySQL connection error
**Solution:** Check if MySQL service is running, verify credentials in `.env`

**Issue:** MongoDB connection error
**Solution:** Start MongoDB service: `sudo systemctl start mongodb`

**Issue:** Import errors in Python
**Solution:** Make sure virtual environment is activated and dependencies installed

**Issue:** Permission denied on git push
**Solution:** Make sure you have access to the repository, contact Raissa if needed

### Need Help?

- Check the main `README.md` for project overview
- Check `TASK_BREAKDOWN.md` for detailed tasks
- Ask in the group chat
- Review existing code in `app/models/` and `app/database/`

### Remember:

✅ Each person needs **4+ meaningful commits** (not README changes)  
✅ Use clear commit messages with [Component] prefix  
✅ Test your code before committing  
✅ Pull latest changes before starting work  
✅ Ask for help if stuck!  

Good luck! 🚀
