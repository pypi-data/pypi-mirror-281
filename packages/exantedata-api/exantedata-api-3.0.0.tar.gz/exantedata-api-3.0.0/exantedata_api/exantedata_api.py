import inspect
import requests
import pandas as pd


API_URL = 'https://apidata.exantedata.com/'


def _errorHandler(response):
    print (f'\n---------------------------------------')
    print(f'Error retrieving data from API in {inspect.stack()[1][3]}')
    print (f'---------------------------------------')
    if 'ERROR' in response.json().keys():
        print(f"API Error Code: \t{response.json()['ERROR']}")
    if 'MESSAGE' in response.json().keys():
        print(f"API Error Message: \t{response.json()['MESSAGE']}")
    print (f'---------------------------------------\n')


def getToken(username, password, proxies=None):
    response = requests.post(
        url=API_URL + 'getToken',
        data={
            'username': username,
            'password': password
        },
        proxies=proxies,
        verify=True
    )
    if response.status_code == 200 and response.json():
        return response.json()['TOKEN']
    else:
        return _errorHandler(response)


def getMetaData(token, tickerQuery, proxies=None):
    response = requests.post(
        url=API_URL + 'Data/Metadata',
        headers={'Authorization': 'Bearer ' + token},
        data=({'ticker': tickerQuery}),
        proxies=proxies,
        verify=True
    )
    if response.status_code == 200 and response.json():
        return pd.DataFrame.from_dict(response.json()['METADATA'])
    else:
        return _errorHandler(response)


def getData(
        token,
        tickerQuery,
        startDate=None,
        endDate=None,
        period=None,
        freq=None,
        agg_method=None,
        fill_method=None,
        fill_value=None,
        proxies=None
    ):
    response = requests.post(
        url=API_URL + 'Data/Data',
        headers={'Authorization': 'Bearer ' + token},
        data=({
            'ticker': tickerQuery,
            'startDate': startDate,
            'endDate': endDate,
            'period': period,
            'freq': freq,
            'agg_method': agg_method,
            'fill_method': fill_method,
            'fill_value': fill_value,
        }),
        proxies=proxies,
        verify=True
    )
    if response.status_code == 200 and response.json():
        return pd.DataFrame.from_dict(response.json()['DATA'])
    else:
        return _errorHandler(response)
