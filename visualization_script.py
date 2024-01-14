import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

DATABASE_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'database': 'stat_project',
}


def fetch_data(query):
    with mysql.connector.connect(**DATABASE_CONFIG) as connection:
        result = pd.read_sql_query(query, connection)
    return result


query_monthly = 'SELECT month, AVG(average_temperature) AS average_temperature FROM summary_monthly WHERE city_id = 1 GROUP BY month'
query_yearly = 'SELECT month, AVG(average_temperature) AS average_temperature, MAX(max_temperature) AS max_temperature, MIN(min_temperature) AS min_temperature FROM summary_yearly WHERE city_id = 1 GROUP BY month'

data_monthly = fetch_data(query_monthly)
data_yearly = fetch_data(query_yearly)

plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(data_monthly['month'], data_monthly['average_temperature'], marker='o')
plt.title('Średnie temperatury miesięczne')
plt.xlabel('Miesiąc')
plt.ylabel('Średnia temperatura (°C)')

plt.subplot(2, 1, 2)
plt.plot(data_yearly['month'], data_yearly['average_temperature'], marker='o', label='Średnia temperatura')
plt.plot(data_yearly['month'], data_yearly['max_temperature'], marker='o', label='Maksymalna temperatura')
plt.plot(data_yearly['month'], data_yearly['min_temperature'], marker='o', label='Minimalna temperatura')
plt.title('Średnie temperatury roczne')
plt.xlabel('Miesiąc')
plt.ylabel('Temperatura (°C)')
plt.legend()

plt.tight_layout()
plt.show()
