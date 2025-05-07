import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('urls.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a table to store the URLs
cursor.execute('''
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL
)
''')

# Insert data into the table (you can loop through your URLs from the file)
with open('urls.txt', 'r', encoding='utf-8') as f:
    urls = f.read()
    urls = urls.split('\n')  # Split the file content into lines
    for url in urls:
        cursor.execute('''
        INSERT INTO urls (url) VALUES (?)
        ''', (url.strip(),))  # Strip removes any extra spaces/newlines from the URL

# Commit the changes to the database
conn.commit()

# Query the database to check if the data was inserted correctly
cursor.execute('SELECT * FROM urls')
rows = cursor.fetchall()

# Print out all the URLs stored in the database
for row in rows:
    print(row)

# Close the connection
conn.close()
