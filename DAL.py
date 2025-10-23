"""
Data Access Layer (DAL)
- Ensures the projects database exists with the required schema
- Provides helpers to interact with the projects table
"""

# A. Import the sqlite library
import sqlite3

DB_NAME = "projects.db"

def ensure_db():
    """Create the database and projects table if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                ImageFileName TEXT
            )
            """
        )
        conn.commit()
    finally:
        conn.close()

# 1. ADD Projects TO DB

def saveProjectDB(Title, Description, ImageFileName):
    #A. Make a connection to the database
    conn = None
    conn = sqlite3.connect(DB_NAME)

    #B. Write a SQL statement to insert a specific row (based on Title name)
    # SQLite is case-insensitive for identifiers; we standardize on lowercase column names
    sql='INSERT INTO projects (title, description, ImageFileName) values (?,?,?)'

    # B. Create a workspace (aka Cursor)
    cur = conn.cursor()

    # C. Run the SQL statement from above and pass it 1 parameter for each ?
    cur.execute(sql, (Title,Description,ImageFileName, ))

    # D. Save the changes
    conn.commit()
    if conn:
        conn.close()


def getAllProjects():
    try:
        conn = sqlite3.connect(DB_NAME)

        cursorObj = conn.cursor()

        cursorObj.execute('SELECT id, title, description, ImageFileName FROM projects;')

        allRows = cursorObj.fetchall()

        projectListOfDictionaries = []

        for individualRow in allRows:
            m = {"id" : individualRow[0], "Title" : individualRow[1], "Description": individualRow[2], "ImageFileName":individualRow[3] }
            projectListOfDictionaries.append(m)

        if conn:
            conn.close()

        return projectListOfDictionaries
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
        return [{"Title" : "Error", "Description": 0000, "ImageFileName": "error.png" }]


def addProject(title, description, imageFileName):
    try:
        conn = sqlite3.connect("projects.db")

        sql = 'INSERT INTO projects (title, description, ImageFileName) VALUES (?,?,?)'

        cur = conn.cursor()

        cur.execute(sql, (title, description, imageFileName))

        conn.commit()
        
        if conn:
            conn.close()
        
        return True
    except Exception as e:
        print(f"An error occurred while adding project: {e}")
        return False

def deleteProject(project_id):
    try:
        conn = sqlite3.connect("projects.db")

        sql = 'DELETE FROM projects WHERE id = ?'

        cur = conn.cursor()

        cur.execute(sql, (project_id,))

        conn.commit()
        
        if conn:
            conn.close()
        
        return True
    except Exception as e:
        print(f"An error occurred while deleting project: {e}")
        return False
