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
                currentMoney = moneyStr.replace('.', '').replace(',','.')
            elif moneyStr.find('EUR'):
                currentMoney = moneyStr[:moneyStr.find('EUR')]
            #elif bank == "VR":
            #    currentMoney = rows[-1][-2].replace('.', '').replace(',','.')
                
        #print(currentMoney)
        return currentMoney

    @staticmethod
    def readCSV_giro(filename, columnNaming):
        locale.setlocale(locale.LC_NUMERIC, '')
        df = pd.read_csv(filename, skiprows=6, sep=';', engine='python', parse_dates=[0,1], \
                         converters={'Betrag (EUR)': lambda x: float(x.replace('.','').replace(',','.'))}, \
                         dayfirst=True, index_col=0)
        df.rename(columns={'Auftraggeber / Begünstigter': columnNaming._client}, inplace=True)
        df.rename(columns={'Betrag (EUR)': columnNaming._value}, inplace=True)
        df = df[df.columns[~df.columns.str.contains('Unnamed:')]]
        #df['Kosten'] = pd.Series(np.random.randn(len(df.index)), index=df.index)

        # changing headers
        df.insert(2, columnNaming._type, pd.Series(columnNaming._unknownType, index=df.index))
        # add account number
        accountNumber=""
        with open(filename, 'rt') as f:
            accountNumber = list(csv.reader(f,delimiter=';'))[0][1]
            accountNumber = accountNumber.split('/')[0].strip()
            df.insert(0, columnNaming._account, pd.Series(accountNumber, index=df.index))

        currentMoney = DKB.getCurrentMoney(filename)
        return (accountNumber, currentMoney, df)
        
        
    @staticmethod
    def readCSV_visa(filename, columnNaming):
        locale.setlocale(locale.LC_NUMERIC, '')
        df = pd.read_csv(filename, skiprows=7, sep=';', engine='python', parse_dates=[1,2], \
                         converters={'Betrag (EUR)': lambda x: float(x.replace('.','').replace(',','.'))}, dayfirst=True, index_col=0)
        df.set_index('Belegdatum', inplace=True)
        df.rename(columns={'Beschreibung': columnNaming._client}, inplace=True)
        df.rename(columns={'Betrag (EUR)': columnNaming._value}, inplace=True)
        df = df[df.columns[~df.columns.str.contains('Unnamed:')]]

        # changing header
        df.insert(1, columnNaming._type, pd.Series(columnNaming._unknownType, index=df.index))
        # add account number
        with open(filename, 'rt') as f:
            accountNumber = list(csv.reader(f,delimiter=';'))[0][1]
            df.insert(0, columnNaming._account, pd.Series(accountNumber, index=df.index))

        currentMoney = DKB.getCurrentMoney(filename)
        return (accountNumber, currentMoney, df)
