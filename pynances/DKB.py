import pandas as pd
import locale
import csv

class DKB(object):
    
    @staticmethod
    def getCurrentMoney(filepath):
        locale.setlocale( locale.LC_ALL, 'German' ) 
        currentMoney = 0
        with open(filepath, 'rt') as f:
            rows = list(csv.reader(f,delimiter=';'))
            #if bank == "DKB":
            moneyStr = rows[4][1]
            if moneyStr.find(',') > 0:
                moneyStr = moneyStr.replace('.', '').replace(',','.')
            if moneyStr.find('EUR'):
                moneyStr = moneyStr[:moneyStr.find('EUR')]
            currentMoney = float(moneyStr)
            #elif bank == "VR":
            #    currentMoney = rows[-1][-2].replace('.', '').replace(',','.')
                
        #print(currentMoney)
        return currentMoney

    @staticmethod
    def readCSV_giro(filename, columnNaming):
        locale.setlocale(locale.LC_NUMERIC, '')
        df = pd.read_csv(filename, skiprows=6, sep=';', engine='python', parse_dates=[0,1], \
                         converters={'Betrag (EUR)': lambda x: float(x.replace('.','').replace(',','.'))}, \
                         dayfirst=True)
        df.rename(columns={'Buchungstag': columnNaming._date}, inplace=True)
        df.rename(columns={'Auftraggeber / Begünstigter': columnNaming._client}, inplace=True)
        df.rename(columns={'Betrag (EUR)': columnNaming._value}, inplace=True)
        df = df[df.columns[~df.columns.str.contains('Unnamed:')]]
        df = df[df[columnNaming._client] != ""]

        # add account number
        accountNumber=""
        with open(filename, 'rt') as f:
            accountNumber = list(csv.reader(f,delimiter=';'))[0][1]
            accountNumber = accountNumber.split('/')[0].strip()

        currentMoney = DKB.getCurrentMoney(filename)
        return (accountNumber, currentMoney, df)
        
        
    @staticmethod
    def readCSV_visa(filename, columnNaming):
        locale.setlocale(locale.LC_NUMERIC, '')
        df = pd.read_csv(filename, skiprows=7, sep=';', engine='python', parse_dates=[1,2], \
                         converters={'Betrag (EUR)': lambda x: float(x.replace('.','').replace(',','.'))}, dayfirst=True, index_col=0)
        df.rename(columns={'Belegdatum': columnNaming._date}, inplace=True)
        df.rename(columns={'Beschreibung': columnNaming._client}, inplace=True)
        df.rename(columns={'Betrag (EUR)': columnNaming._value}, inplace=True)
        df = df[df.columns[~df.columns.str.contains('Unnamed:')]]

        # add account number
        with open(filename, 'rt') as f:
            accountNumber = list(csv.reader(f,delimiter=';'))[0][1]
            accountNumber = accountNumber.replace('*','.') # regex
            
        currentMoney = DKB.getCurrentMoney(filename)
        return (accountNumber, currentMoney, df)
