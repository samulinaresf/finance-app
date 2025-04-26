import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(BASE_DIR, 'database.db')
upload_date = 20250416
file_name = "archivo.csv"

class File():
    def __init__(self,uploadDate,fileName):
        self.uploadDate = uploadDate
        self.fileName = fileName
    def __str__(self):
        return f"Archivo guardado. Fecha:{self.uploadDate}, Nombre:{self.fileName}.csv"

new_file = File(upload_date,file_name)

def create_file(file_obj):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO files (uploadDate, fileName) VALUES (?,?)",(file_obj.uploadDate, file_obj.fileName))  
    conn.commit() 
    conn.close()
    
#create_file(new_file)
    
def read_file():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM files")
    rows = cursor.fetchall()
    for row in rows:
        print(row) 
    conn.close()

#read_file()
    
def update_file(new_filename,file_id):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("UPDATE files SET fileName = ? WHERE fileId = ?", (new_filename, file_id))
    conn.commit()
    conn.close()    

def delete_file(file_name):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM files WHERE fileName = ?", (file_name,))
    conn.commit()
    conn.close()

