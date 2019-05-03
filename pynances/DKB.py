import pandas as pd
import locale
import csv
import os
import datetime


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

        # DKB changed format somewhere around April 2019
        rowskip = 6
        creationTime = os.path.getctime(filename)
        creationDate = datetime.datetime.fromtimestamp(creationTime)
        formatChangeDate = datetime.datetime(2019, 5, 1, 0, 0)
        if creationDate > formatChangeDate:
            rowskip = 8

        df = pd.read_csv(filename, skiprows=rowskip, sep=';', engine='python', parse_dates=[0,1], \
                         converters={'Betrag (EUR)': lambda x: float(x.replace('.','').replace(',','.'))}, \
                         dayfirst=True)
        df.rename(columns={'Buchungstag': columnNaming._date}, inplace=True)
        df.rename(columns={'Kontonummer': columnNaming._iban}, inplace=True)
        df.rename(columns={'Auftraggeber / Begünstigter': columnNaming._client}, inplace=True)
        df.rename(columns={'Verwendungszweck': columnNaming._usageType}, inplace=True)
        df.rename(columns={'Betrag (EUR)': columnNaming._value}, inplace=True)
        df = df[df.columns[~df.columns.str.contains('Unnamed:')]]
        df = df[df[columnNaming._client] != ""]
        df = df[df[columnNaming._client].notnull()]

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
        try:
            df = pd.read_csv(filename, skiprows=7, sep=';', engine='python', parse_dates=[1,2], \
                         converters={'Betrag (EUR)': lambda x: float(x.replace('.','').replace(',','.'))}, dayfirst=True, index_col=0)

        except:
            return (0, 0, pd.DataFrame())
            
        # add account number
        with open(filename, 'rt') as f:
            accountNumber = list(csv.reader(f,delimiter=';'))[0][1]
            accountNumber = accountNumber.replace('*','.') # regex

        if df.shape[0] == 0:
            return (accountNumber, 0, df)

        df.rename(columns={'Belegdatum': columnNaming._date}, inplace=True)
        df.rename(columns={'Beschreibung': columnNaming._client}, inplace=True)
        df.rename(columns={'Betrag (EUR)': columnNaming._value}, inplace=True)
        df = df[df.columns[~df.columns.str.contains('Unnamed:')]]
        if columnNaming._client in df.columns:
            df = df[df[columnNaming._client] != ""]
        else:
            return (accountNumber, 0, pd.DataFrame())

        currentMoney = DKB.getCurrentMoney(filename)
        return (accountNumber, currentMoney, df)
