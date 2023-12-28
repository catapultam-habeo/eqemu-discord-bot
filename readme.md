Database Schema additions

table: discord_users
    discord_id INT (PRIMARY, AUTO_INC)
    subscriber_tier TINYINT (0)

table: discord_ls_accounts
    account_id INT (PRIMARY, UNIQUE)
    character_id INT (UNIQUE)
    discord_id INT


```sql
-- Drop existing tables if they exist
DROP TABLE IF EXISTS discord_ls_accounts;
DROP TABLE IF EXISTS discord_users;

-- Create table 'discord_users'
CREATE TABLE discord_users (
    discord_id INT AUTO_INCREMENT PRIMARY KEY,
    subscriber_tier TINYINT DEFAULT 0
);

-- Create table 'discord_ls_accounts'
CREATE TABLE discord_ls_accounts (
    account_id INT PRIMARY KEY,
    character_id INT UNIQUE,
    discord_id INT,
    FOREIGN KEY (discord_id) REFERENCES discord_users(discord_id)
);
```

Usage:
    /register <account_name> <character_name>
        - Register your loginserver account ownership. Provided character name will be added to your Discord nickname. Character\Account pair must be valid. If this account is already registered, the new character name will overwrite your previous one.

    /unregister <account_name>
        - Removes your loginserver account registration.

    /accounts
        - List your registered loginserver accounts