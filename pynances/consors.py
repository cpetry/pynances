import pandas as pd
import locale
import csv

class Consors(object):
        
    @staticmethod
    def getCurrentMoney(filepath):
        locale.setlocale( locale.LC_ALL, 'German' ) 
        currentMoney = 0
        #with open(filepath, 'rt') as f:
        #    rows = list(csv.reader(f,delimiter=';'))
        #    currentMoney = rows[-1][-2].replace('.', '').replace(',','.')
                
        return currentMoney

    @staticmethod
    def readCSV_giro(filename, columnNaming):
        locale.setlocale(locale.LC_NUMERIC, '')
        df = pd.read_csv(filename, encoding="utf-8", skiprows=0, skipfooter=0, sep=';', engine='python', parse_dates=[0,1], \
                         converters={'Betrag in EUR': lambda x: float(x.replace('.','').replace(',','.'))}, dayfirst=True)
        df.rename(columns={'Valuta': columnNaming._date,
                          'Sender / Empfänger': columnNaming._client,
                          'Verwendungszweck': columnNaming._info,
                          'Betrag in EUR': columnNaming._value,
                          'Kategorie': columnNaming._type}, inplace=True)
        df = df[df.columns[~df.columns.str.contains('Unnamed:')]]
        
        df.drop('IBAN / Konto-Nr.', axis=1, inplace=True)
        df.drop('BIC / BLZ', axis=1, inplace=True)
        if ' ' in df.columns:
            df.drop(' ', axis=1, inplace=True)
        df = df[df.columns[~df.columns.str.contains('Unnamed:')]]
        
        #with open(filename, 'rt') as f:
        #    csvList = list(csv.reader(f,delimiter=';'))
        #    blz = csvList[4][1]
        #    accountNumber = csvList[5][1]
        currentMoney = Consors.getCurrentMoney(filename)
        accountNumber = "Some consors account..."
        return (accountNumber, currentMoney, df)
        