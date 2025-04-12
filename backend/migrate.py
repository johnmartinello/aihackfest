import sqlite3

def migrate_database():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("PRAGMA table_info(books)")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        
        if 'genre' not in column_names:
            print("Adding 'genre' column to books table...")
            cursor.execute("ALTER TABLE books ADD COLUMN genre TEXT")
            conn.commit()
            print("Migration completed successfully!")
        else:
            print("The 'genre' column already exists in the books table.")
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()