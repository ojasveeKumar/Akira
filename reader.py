import sqlite3
import time
import os
from tabulate import tabulate

DB_FILE = 'Calls.db'
REFRESH_INTERVAL = 3  # Time in seconds between updates

def clear_screen():
    """Clear the terminal screen based on OS."""
    os.system('cls' if os.name == 'nt' else 'clear')

def view_database_continuous():
    print("Starting database monitor... Press Ctrl+C to stop.\n")
    time.sleep(1)

    while True:
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            cursor.execute("SELECT id, name, email, project_type, message, submitted_at FROM calls")
            rows = cursor.fetchall()
            headers = [description[0] for description in cursor.description]

            conn.close()

            clear_screen()
            print("=== Live Database Feed (Press Ctrl+C to exit) ===\n")

            if not rows:
                print("No inquiries found in the database yet.")
            else:
                print(tabulate(rows, headers=headers, tablefmt="grid"))
                print(f"\nTotal submissions: {len(rows)}")

            time.sleep(REFRESH_INTERVAL)

        except sqlite3.OperationalError:
            clear_screen()
            print(f"Waiting for database '{DB_FILE}' to be created...")
            time.sleep(REFRESH_INTERVAL)
        except KeyboardInterrupt:
            print("\nStopped monitoring database.")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            break

if __name__ == '__main__':
    view_database_continuous()