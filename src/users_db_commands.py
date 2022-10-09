class UsersDBCommands:
    CREATE_USERS_TABLE_COMMAND = """
    CREATE TABLE IF NOT EXISTS users (
        user_id UUID PRIMARY KEY,
        user_name VARCHAR(255) NOT NULL,
        user_surname VARCHAR(255) NOT NULL,
        user_age INTEGER NOT NULL
    );
    """
    INSERT_USER_COMMAND = """
    INSERT INTO users (user_id, user_name, user_surname, user_age)
    VALUES (%s, %s, %s, %s);
    """
    GET_USER_COMMAND = """
    SELECT * FROM users WHERE user_id = %s;
    """
    UPDATE_USER_COMMAND = """
    UPDATE users SET user_name = %s, user_surname = %s, user_age = %s
    WHERE user_id = %s;
    """
    DELETE_USER_COMMAND = """
    DELETE FROM users WHERE user_id = %s;
    """

    CREATE_SESSIONS_HISTORY_TABLE_COMMAND = """
    CREATE TABLE IF NOT EXISTS sessions_history (
        session_id SERIAL PRIMARY KEY,
        session_key UUID NOT NULL,
        session_data CHAR(32) NOT NULL
    );
    """
    INSERT_SESSION_COMMAND = """"""
