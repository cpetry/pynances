import pandas as pd
import locale
import csv

class VR(object):

    @staticmethod
    def getCurrentMoney(filepath):
        locale.setlocale( locale.LC_ALL, 'German' ) 
        currentMoney = 0
        with open(filepath, 'rt') as f:
            rows = list(csv.reader(f,delimiter=';'))
            currentMoney = rows[-1][-2].replace('.', '').replace(',','.')
                
        return currentMoney

    @staticmethod
    def readCSV_giro(self, filename):
        locale.setlocale(locale.LC_NUMERIC, '')
        df = pd.read_csv(filename, skiprows=12, skipfooter=2, sep=';', engine='python', parse_dates=[0,1], \
                         converters={'Umsatz': lambda x: float(x.replace('.','').replace(',','.'))}, dayfirst=True, index_col=0)
        df.rename(columns={'Empfänger/Zahlungspflichtiger': 'Auftraggeber'}, inplace=True)
        df.rename(columns={'Vorgang/Verwendungszweck': 'Buchungstext'}, inplace=True)
        df.rename(columns={'Umsatz': 'Betrag'}, inplace=True)
        
        # convert 'S'oll -> negative values
        df.loc[df.ix[:,-1] == 'S','Betrag'] = 0 - df[df.ix[:,-1] == 'S'].Betrag
        df.drop('Auftraggeber/Zahlungsempfänger', axis=1, inplace=True)
        df.drop('Konto-Nr.', axis=1, inplace=True)
        df.drop('IBAN', axis=1, inplace=True)
        df.drop('BIC', axis=1, inplace=True)
        df.drop('BLZ', axis=1, inplace=True)
        df.drop('Kundenreferenz', axis=1, inplace=True)
        df.drop('Währung', axis=1, inplace=True)
        df.drop('Valuta', axis=1, inplace=True)
        df.drop(' ', axis=1, inplace=True)
        df = df[df.columns[~df.columns.str.contains('Unnamed:')]]
        
        accountNumber = list(csv.reader(f,delimiter=';'))[5][1]
        currentMoney = VR.getCurrentMoney(filename)
        return (accountNumber, currentMoney, df)
        