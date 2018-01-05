import pandas as pd
import locale
import csv

class VR(object):
        
    @staticmethod
    def convertToIBAN(accountNumber, blz, loc="DE"):
        bban = str(blz) + str(accountNumber).zfill(10)
        countryString = str(ord(loc[0]) - ord('A') + 10) + str(ord(loc[1]) - ord('A') + 10) + str("00")
        checksum = int(bban + countryString)
        checkNumber = str(98 - (checksum % 97)).zfill(2)
        return loc + checkNumber + bban

    @staticmethod
    def getCurrentMoney(filepath):
        locale.setlocale( locale.LC_ALL, 'German' ) 
        currentMoney = 0
        with open(filepath, 'rt') as f:
            rows = list(csv.reader(f,delimiter=';'))
            currentMoney = rows[-1][-2].replace('.', '').replace(',','.')
                
        return currentMoney

    @staticmethod
    def readCSV_giro(filename, columnNaming):
        locale.setlocale(locale.LC_NUMERIC, '')
        df = pd.read_csv(filename, skiprows=12, skipfooter=2, sep=';', engine='python', parse_dates=[0,1], \
                         converters={'Umsatz': lambda x: float(x.replace('.','').replace(',','.'))}, dayfirst=True)
        df.rename(columns={'Buchungstag': columnNaming._date}, inplace=True)
        df.rename(columns={'Empfänger/Zahlungspflichtiger': columnNaming._client}, inplace=True)
        df.rename(columns={'Vorgang/Verwendungszweck': columnNaming._info}, inplace=True)
        df.rename(columns={'Umsatz': columnNaming._value}, inplace=True)
        
        # convert 'S'oll -> negative values
        df.loc[df.ix[:,-1] == 'S', columnNaming._value] = 0 - df[df.ix[:,-1] == 'S'][columnNaming._value]
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
        
        with open(filename, 'rt') as f:
            csvList = list(csv.reader(f,delimiter=';'))
            blz = csvList[4][1]
            accountNumber = csvList[5][1]
            accountNumber = VR.convertToIBAN(accountNumber, blz)
        currentMoney = VR.getCurrentMoney(filename)
        return (accountNumber, currentMoney, df)
        