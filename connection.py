import mysql.connector
from sqlalchemy import create_engine, types
import passkeys as pk

def create_database_Alchemy(db_name,df):
    try:
        url = f"mysql+mysqlconnector://{pk.user}:{pk.password}@{pk.host}/{db_name}"
        engine = create_engine(url)

        df.to_sql(
            name='messages',
            con=engine,
            if_exists='replace',
            index=False,
            dtype={
                'account_id': types.Integer(),
                'full_date': types.DATETIME(),
                'msgs_count': types.Integer(),
                'im_state': types.VARCHAR(20)
            }
        )
        print(f"- Data successfully inserted into {db_name}.")
    except Exception as e:
        print(f">> Error creating database: {e}")

def create_database_Connector(db_name,df):
    try:
        conn = mysql.connector.connect(
            host = pk.host,
            user = pk.user,
            password = pk.password
        )
        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"-- Database '{db_name} created successfully.")
        cursor.execute(f"USE {db_name}")

        create_table_query = """ 
        CREATE TABLE IF NOT EXISTS messages(
            id INT AUTO_INCREMENT PRIMARY KEY,
            account_id INT,
            full_date DATE,
            msgs_count INT,
            im_state VARCHAR(20)
        );
        """
        cursor.execute(create_table_query)
        print(f"> Table 'messages' created in {db_name}.")

        for index, row in df.iterrows():
            insert_query = """ 
            INSERT INTO messages(account_id, full_date, msgs_count, im_state)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query,tuple(row))
        
        conn.commit()
        print(f"> Data inserted successfully into {db_name}.")
    except (mysql.connector.Error,IOError) as e:
        print(f">> Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print(f"> Connection to {db_name} closed.")
