import os


class Config:
    DEBUG = True

    # Project path, get the folder name of the current file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # sqlite data location
    SQLITE_DIR = os.path.join(BASE_DIR, r'src\sqlite3.db')

