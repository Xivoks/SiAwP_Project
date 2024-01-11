import os
import mysql.connector
import pandas as pd


def load_data(csv_path):
    try:
        df = pd.read_csv(csv_path)
        df.dropna(thresh=6, inplace=True)
        return df
    except Exception as e:
        print(f"Błąd podczas wczytywania danych: {e}")
        return None


with open('pass.txt', 'r') as file:
    lines = file.readlines()
    db_username = lines[0].strip()
    db_password = lines[1].strip()

db_host = '127.0.0.1'
db_name = 'stat_project'

connection = mysql.connector.connect(
    host=db_host,
    user=db_username,
    password=db_password,
    database=db_name,
    auth_plugin='mysql_native_password'
)

cursor = connection.cursor()

create_table_query_city = """
CREATE TABLE IF NOT EXISTS city (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(60)
);
"""

cursor.execute(create_table_query_city)

create_table_query_historical_weather = """
CREATE TABLE IF NOT EXISTS historical_weather (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    w_date DATE,
    temp_avg FLOAT,
    temp_min FLOAT,
    temp_max FLOAT,
    wind_dir FLOAT,
    wind_speed FLOAT,
    pressure FLOAT,
    city INT,
    FOREIGN KEY (city) REFERENCES city(ID)
);
"""

cursor.execute(create_table_query_historical_weather)

create_stats_table_query = """
CREATE TABLE IF NOT EXISTS weather_statistics (
    city INT,
    mean_temperature FLOAT,
    median_temperature FLOAT,
    std_deviation FLOAT,
    min_temperature FLOAT,
    max_temperature FLOAT
);
"""

cursor.execute(create_stats_table_query)

csv_path = './data'

for plik in os.listdir(csv_path):
    if plik.endswith(".csv"):
        print("$" * 70)
        print(plik)
        print("$" * 70)
        location_name = plik.split('.')[0]
        insert_query = f"INSERT INTO city (name) " \
                       f"VALUES ('{location_name}');"
        cursor.execute(insert_query)

        connection.commit()

        location_id = cursor.lastrowid

        df = load_data(csv_path + "/" + plik)

        for column in df.columns:
            print(f"Unikalne wartości w kolumnie '{column}':")
            print(len(df[column].unique()))
            print(f"Liczba wartości NaN w kolumnie '{column}':")
            print(df[column].isna().sum().sum())
            print("=" * 40)

        # Usunięcie kolumn tsun i snow, ponieważ tam wszystkie wartości to NaN
        # Usunięcie także kolumn prcp i wpgt, ponieważ ponad połowa rekordów ma wartości NaN
        df.drop(['tsun', 'snow', 'prcp', 'wpgt'], axis=1, inplace=True)

        df = df.fillna(df.mode().iloc[0])

        print(df.shape)

        for _, row in df.iterrows():
            insert_query = f"INSERT INTO historical_weather (w_date, temp_avg, temp_min, temp_max, wind_dir, wind_speed, pressure, city) " \
                           f"VALUES ('{row['date']}', {row['tavg']}, {row['tmin']}, {row['tmax']}, {row['wdir']}, {row['wspd']}, {row['pres']}, {location_id});"
            cursor.execute(insert_query)

        connection.commit()

# Obliczenie i zapisanie statystyk dla każdej lokalizacji
stats_query = """
INSERT INTO weather_statistics (city, mean_temperature, median_temperature, std_deviation, min_temperature, max_temperature)
SELECT city,
       AVG(temp_avg) AS mean_temperature,
       IFNULL(
           (SELECT temp_avg
            FROM (
                SELECT temp_avg, @rownum:=@rownum+1 as rownum
                FROM historical_weather
                WHERE city = historical_weather.city
                ORDER BY temp_avg
            ) as temp_table
            WHERE temp_table.rownum = (
                (SELECT COUNT(*) FROM historical_weather WHERE city = historical_weather.city) + 1) / 2
           ),
           (SELECT AVG(temp_avg) FROM historical_weather WHERE city = historical_weather.city)
       ) AS median_temperature,
       STDDEV(temp_avg) AS std_deviation,
       MIN(temp_avg) AS min_temperature,
       MAX(temp_avg) AS max_temperature
FROM historical_weather
GROUP BY city;
"""

cursor.execute(stats_query)
connection.commit()

select_query = """
SELECT city.name, weather_statistics.mean_temperature, weather_statistics.median_temperature, weather_statistics.std_deviation, 
weather_statistics.min_temperature, weather_statistics.max_temperature
FROM weather_statistics
JOIN city ON weather_statistics.city = city.ID;
"""

cursor.execute(select_query)

print("\nDane statystyczne dla każdej lokalizacji:")
for (name, mean_temp, median_temp, std_dev, min_temp, max_temp) in cursor:
    print(f"Lokalizacja: {name}")
    print(f"Średnia temperatura: {mean_temp}")
    print(f"Mediana temperatury: {median_temp}")
    print(f"Odchylenie standardowe: {std_dev}")
    print(f"Minimalna temperatura: {min_temp}")
    print(f"Maksymalna temperatura: {max_temp}")
    print("=" * 40)

cursor.close()
connection.close()
