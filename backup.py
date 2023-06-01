from time import sleep
from os import system
from datetime import datetime

while True:
    system("cp ./db.sqlite3 ../db.sqlite3.bak")
    system("git pull")
    print("Backed up database and synced repo at", datetime.now())
    sleep(3600)
