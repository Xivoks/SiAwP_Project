import warnings

import scipy.stats as stats

from fetch_data import fetch_data_from_database
from load_data import initialize_and_load_data
from statistical_tests import test_normality, test_variance_equality, paired_t_test, independent_t_test, one_way_anova


def main():
    warnings.filterwarnings("ignore", category=stats.DegenerateDataWarning)
    initialize_and_load_data()

    data = fetch_data_from_database()
    if data is not None:
        print("Test normalności:", test_normality(data['mean_temperature']))
        print("Test równości wariancji:", test_variance_equality(data[['max_temperature', 'min_temperature']]))
        data1 = data['mean_temperature'].iloc[:5]
        data2 = data['median_temperature'].iloc[:5]
        print("Test t-Studenta dla zmiennych zależnych:", paired_t_test(data1, data2))
        data1 = data['mean_temperature'].iloc[:5]
        data2 = data['std_deviation'].iloc[:5]
        print("Test t-Studenta dla zmiennych niezależnych:", independent_t_test(data1, data2))

        print("Dostępne kolumny w danych:", data.columns)

        # kolumny do testu ANOVA
        group_column = 'city'
        value_column = 'mean_temperature'

        data_anova = data[[group_column, value_column]]

        try:
            with warnings.catch_warnings():
                result = one_way_anova(data_anova, group_column, value_column)
                print("Test ANOVA:", result)
        except stats.ConstantInputWarning:
            print("Błąd podczas przeprowadzania testu ANOVA: Dane są stałe.")

    else:
        print("Błąd podczas pobierania danych z bazy.")


if __name__ == "__main__":
    main()
