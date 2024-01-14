import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
import seaborn as sns
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

connection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    database='stat_project',
)

query = """
SELECT DAY(w_date) as day, AVG(temp_avg) as avg_temp
FROM historical_weather
WHERE MONTH(w_date) = 1 AND city = 1
GROUP BY DAY(w_date);
"""

data = pd.read_sql(query, connection)

data['city'] = 1
X_train = data[['day', 'city']]
y_train = data['avg_temp']

models = {
    'Regresja Ridge': Ridge(),
    'Regresja Lasso': Lasso(),
    'Regresja Las Losowy': RandomForestRegressor()
}

plt.figure(figsize=(16, 16))
for model_name, model in models.items():
    model = make_pipeline(PolynomialFeatures(2), model)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_train)

    sns.lineplot(x=data['day'], y=y_pred, label=f'Prognoza {model_name}', alpha=0.7)

sns.lineplot(x=data['day'], y=y_train, label='Rzeczywiste temperatury', alpha=0.7)

plt.xlabel('Dzień stycznia')
plt.ylabel('Temperatura')
plt.title('Prognozowanie średnich temperatur dla różnych modeli regresji')
plt.legend(loc='lower right')
plt.show()

connection.close()
