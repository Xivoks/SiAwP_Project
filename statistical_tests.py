import scipy.stats as stats


def test_normality(data):
    _, p_value = stats.shapiro(data)
    if p_value < 0.05:
        return "Rozkład jest nie normalny (p < 0.05)"
    else:
        return "Rozkład jest normalny (p >= 0.05)"


def test_variance_equality(data):
    _, p_value = stats.levene(*data.values.T)
    if p_value < 0.05:
        return "Równość wariancji nie jest spełniona (p < 0.05)"
    else:
        return "Równość wariancji jest spełniona (p >= 0.05)"


def paired_t_test(data1, data2):
    _, p_value = stats.ttest_rel(data1, data2)
    if p_value < 0.05:
        return "Istnieje istotna różnica między grupami (p < 0.05)"
    else:
        return "Brak istotnej różnicy między grupami (p >= 0.05)"


def independent_t_test(data1, data2):
    _, p_value = stats.ttest_ind(data1, data2)
    if p_value < 0.05:
        return "Istnieje istotna różnica między grupami (p < 0.05)"
    else:
        return "Brak istotnej różnicy między grupami (p >= 0.05)"


def one_way_anova(data, group_column, value_column):
    groups = data[group_column].unique()
    group_data = [data[data[group_column] == group][value_column] for group in groups]
    _, p_value = stats.f_oneway(*group_data)
    if p_value < 0.05:
        return "Istnieje istotna różnica między grupami (p < 0.05)"
    else:
        return "Brak istotnej różnicy między grupami (p >= 0.05)"
