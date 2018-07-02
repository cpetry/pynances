import pandas as pd
import locale
import csv

class Paypal(object):

    @staticmethod
    def getCurrentMoney(filepath):
        locale.setlocale(locale.LC_NUMERIC, '')
        currentMoney = 0
        with open(filepath, 'rt', encoding="utf8") as f:
            rows = list(csv.reader(f, delimiter=','))
            # if bank == "DKB":
            moneyStr = rows[-1][29]
            if moneyStr.find(',') > 0:
                moneyStr = moneyStr.replace('.', '').replace(',', '.')
            currentMoney = float(moneyStr)

        return currentMoney

    @staticmethod
    def readCSV(filename, columnNaming):
        locale.setlocale(locale.LC_NUMERIC, '')
        df = pd.read_csv(filename, skiprows=0, sep=',', engine='python', parse_dates=[0], \
                         converters={'Netto': lambda x: float(x.replace('.', '').replace(',', '.'))}, \
                         dayfirst=True)
        df.rename(columns={list(df)[0]: columnNaming._date}, inplace=True)
        df.rename(columns={'Name': columnNaming._client}, inplace=True)
        df.rename(columns={'Netto': columnNaming._value}, inplace=True)
        df.rename(columns={'Typ': columnNaming._type}, inplace=True)
        df.rename(columns={'Artikelbezeichnung': 'name2'}, inplace=True)
        df = df[df["Status"] == "Abgeschlossen"]
        df = df[df[columnNaming._client].notnull()]
        
        df.loc[df[columnNaming._type] != 'Spendenzahlung', columnNaming._type] = "Paypal" 
        df[columnNaming._client] = df[columnNaming._client] + ', ' + df['name2']
		
        # add account number
        accountNumber = "Paypal"

        currentMoney = Paypal.getCurrentMoney(filename)
        return (accountNumber, currentMoney, df)
