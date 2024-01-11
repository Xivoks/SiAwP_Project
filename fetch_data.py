import mysql.connector
import pandas as pd

def fetch_data_from_database():
    try:
        with open('pass.txt', 'r') as file:
            lines = file.readlines()
            db_username = lines[0].strip()
            # db_password = lines[1].strip()

        db_host = '127.0.0.1'
        db_name = 'stat_project'

        connection = mysql.connector.connect(
            host=db_host,
            user=db_username,
            # password=db_password,
            database=db_name,
            auth_plugin='mysql_native_password'
        )

        cursor = connection.cursor()

        query = "SELECT * FROM weather_statistics;"  # Zapytanie SQL do pobrania wszystkich danych
        cursor.execute(query)
        data = cursor.fetchall()

        # Przekształć wyniki zapytania do DataFrame
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=columns)

        cursor.close()
        connection.close()

        return df

    except Exception as e:
        print(f"Błąd podczas pobierania danych z bazy: {e}")
        return None
