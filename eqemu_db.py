import mariadb
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_ADDRESS = os.getenv('DB_ADDRESS')
DB_NAME = os.getenv('DB_NAME')

class eqemu_db:
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = mariadb.connect(
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_ADDRESS,
                database=DB_NAME
            )
        except mariadb.Error as e:
            print(f"Error connecting to EQEMU: {e}")

    def get_valid(self, account_name, character_name):
        try:
            cursor = self.conn.cursor()
            query = "SELECT account.id, character_data.name FROM account, character_data WHERE LOWER(account.name) = LOWER(%s) AND LOWER(character_data.name) = LOWER(%s) AND character_data.account_id = account.id"
            cursor.execute(query, (account_name, character_name))
            result = cursor.fetchone()
            return result is not None  # Returns True if the pair is valid, False otherwise
        except mariadb.Error as e:
            print(f"Database error in get_valid: {e}")
            return None

    def get_nick_string(self, discord_id):
        try:
            cursor = self.conn.cursor()
            query = """
                        SELECT character_data.name 
                        FROM discord_ls_accounts
                        JOIN character_data ON discord_ls_accounts.character_id = character_data.id
                        WHERE discord_ls_accounts.discord_id = %s
                    """
            cursor.execute(query, (discord_id,))
            characters = cursor.fetchall()
            character_names = [char[0] for char in characters]  # Extract character names from the query results
            return " \ ".join(character_names)  # Join the names with ' \ ' as separator
        except mariadb.Error as e:
            print(f"Database error in get_nick_string: {e}")
            return None


    # ... Other database methods ...

    def close(self):
        if self.conn:
            self.conn.close()
