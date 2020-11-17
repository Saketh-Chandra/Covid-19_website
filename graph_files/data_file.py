import pandas as pd
import numpy as np


def data_Confirmed(Country, State=''):
    # -->Confirmed
    dfC = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    dfC = dfC.replace(np.nan, '', regex=True)

    in_C = dfC.loc[(dfC['Country/Region'] == Country) & (dfC['Province/State'] == State)]

    Confirmed = in_C.to_numpy()

    index = dfC.columns[1:].to_numpy()

    # print(list(index[3:]))
    # print(list(Confirmed[0][4:]))
    # a = pd.to_datetime(np.array(list(index[3:])))
    return list(index[3:]), (list(Confirmed[0][4:]))

    # print(inx[4:],b[0][4:],sep='\n')


def data_Recovered(Country, State=''):
    # -->Recovered
    dfR = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    dfR = dfR.replace(np.nan, '', regex=True)

    in_R = dfR.loc[(dfR['Country/Region'] == Country) & (dfR['Province/State'] == State)]

    Recovered = in_R.to_numpy()
    try:
        Recovered = list(Recovered[0][4:])
    except IndexError:
        Recovered = []
    # print(Recovered)
    return Recovered


def data_Deaths(Country, State=''):
    # -->Deaths

    dfD = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    dfD = dfD.replace(np.nan, '', regex=True)

    in_D = dfD.loc[(dfD['Country/Region'] == Country) & (dfD['Province/State'] == State)]

    Deaths = in_D.to_numpy()
    # print(list(Deaths[0][4:]))
    return list(Deaths[0][4:])


def test():
    country = "India"
    state = ''
    data_Confirmed(country, state)
    data_Recovered(country, state)
    data_Deaths(country, state)


def new_cases_c(Country, State=''):
    index, confirmed = data_Confirmed(Country, State)
    recoverd = data_Recovered(Country, State)
    deaths = data_Deaths(Country, State)
    new_c = []
    new_r = []
    new_d = []
    for i in range(len(confirmed) - 1):
        new_c.append(confirmed[i + 1] - confirmed[i])
        new_r.append(recoverd[i + 1] - recoverd[i])
        new_d.append(deaths[i + 1] - deaths[i])
    return index[1:], new_c, new_r, new_d


def list_of_country_state():
    df = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    df = df.replace(np.nan, '', regex=True)
    data = df[['Country/Region', 'Province/State']]
    data = np.array(data)
    return data


def data_of_world_wide():
    dfC = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

    dfC = dfC.replace(np.nan, '', regex=True)

    dfR = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    dfR = dfR.replace(np.nan, '', regex=True)

    new = list(dfC.head())[-1]
    co = list(dfC.head(0))[1]
    print(co, new)
    dC = dfC[[co, new]]
    dR = dfR[[co, new]]

    dC = dC.groupby([co]).sum()
    dR = dR.groupby([co]).sum()

    dC = dC.rename(columns={new: 'Confirmed'})
    dR = dR.rename(columns={new: 'Recovered'})

    dCR = pd.merge(dC, dR, how='outer', on='Country/Region')
    dCR.insert(0, "Country", dCR.index)
    return dCR.values.tolist()


# print(data_of_world_wide())
""""

if __name__=='__main__':
    print(__name__)
    test()

"""
