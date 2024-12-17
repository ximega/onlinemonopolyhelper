#!/usr/bin/python

import shutil
import os
import pytz
from datetime import datetime

TZ = pytz.timezone('Asia/Tashkent')

# Paths to your database and backup directory
db_path = 'db.sqlite3'
backup_dir = 'backups'

# Create a timestamped backup file name
timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
backup_file = os.path.join(backup_dir, f"db_backup_{timestamp}.sqlite3")

# Copy the database to the backup location
shutil.copy(db_path, backup_file)

print(f"Backup created: {backup_file}")

filenames = os.listdir(backup_dir)
for filename in filenames:
    then = datetime.strptime(filename.replace("db_backup_", "").replace(".sqlite3", ""), "%Y-%m-%d-%H:%M:%S")
    then = TZ.localize(then)
    now = datetime.now(TZ)
    if (now - then).seconds > 60 * 20:
        os.remove(os.path.join(backup_dir, filename))