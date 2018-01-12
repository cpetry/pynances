# Import all libraries needed for the tutorial

# General syntax to import specific functions in a library: 
##from (library) import (specific library function)
from pandas import DataFrame, read_csv

import numpy as np
# General syntax to import a library but no functions: 
##import (library) as (give the library a nickname/alias)
import matplotlib.pyplot as plt
import pandas as pd #this is how I usually import pandas
import sys #only needed to determine Python version number
import matplotlib #only needed to determine Matplotlib version number
import time
import functools
import operator
import re
import locale
import calendar
import collections
import datetime
from IPython.display import display
import plotly
from plotly.graph_objs import Bar, Layout, Pie

pd.options.display.float_format = '{:,.2f}'.format

import pandas as pd
from pandas import DataFrame, read_csv
from datetime import datetime

import numpy as np

#local imports
from pynances.DKB import DKB
from pynances.VR import VR
from pynances.consors import Consors

class Pynance(object):
    class ColumnNaming():
        def __init__(self):
            language = locale.getdefaultlocale()
            self._date = 'date'
            self._client = 'client'
            self._value = 'value'
            self._info = 'info'
            self._account = 'account'
            if language[0] == 'de_DE':
                self._unknownType = 'Undefiniert'
                self._transfer = 'Verschiebungen'
                self._type = 'Typ'
            else:
                self._unknownType = 'undefined'
                self._transfer = 'transfer'
                self._type = 'type'

    def __init__(self):
        self.df = None;
        self.accountNumbers = []
        self.currentMoney = {}
        self.parsedCategories = []
        self.columnNaming = self.ColumnNaming()

    def setGroups(self, groupDict):
        self.groupDict = groupDict
        self.renameSimilars(self.columnNaming._client, self.columnNaming._type)

        
    def renameSimilars(self, renameField, groupField):
        # renaming similar stuff
        for key, values in self.groupDict.items():
            for val in values:
                self.df[renameField]= self.df[renameField].str.replace(val+".*", val, case=False)

        for key, values in self.groupDict.items():
            group_filter = self.df[renameField].str.contains('|'.join(map(re.escape, values)), flags=re.IGNORECASE)==True
            self.df.ix[group_filter, groupField] = key

    
    def getCurrentMoney(self, filepath, bank):
        locale.setlocale( locale.LC_ALL, 'German' ) 
        currentMoney = 0
        with open(filepath, 'rt') as f:
            rows = list(csv.reader(f,delimiter=';'))
            if bank == "DKB":
                moneyStr = rows[4][1]
                if moneyStr.find(',') > 0:
                    currentMoney = moneyStr.replace('.', '').replace(',','.')
                elif moneyStr.find('EUR'):
                    currentMoney = moneyStr[:moneyStr.find('EUR')]
            elif bank == "VR":
                currentMoney = rows[-1][-2].replace('.', '').replace(',','.')
                
        #print(currentMoney)
        return currentMoney

    
    def getColumns(self,filter):
        return self.df.filter(items=filter)

    def setColumns(self,filter):
        self.df = self.df.filter(items=filter)
    
    def readCSV(self, filename, banktype):
        if banktype == 'DKB_giro':
            (accountNumber, currentMoney, df) = DKB().readCSV_giro(filename, self.columnNaming)
        elif banktype == 'DKB_visa':
            (accountNumber, currentMoney, df) = DKB().readCSV_visa(filename, self.columnNaming)
        elif banktype == 'VR_giro':
            (accountNumber, currentMoney, df) = VR().readCSV_giro(filename, self.columnNaming)
        elif banktype == 'Consors_giro':
            (accountNumber, currentMoney, df) = Consors().readCSV_giro(filename, self.columnNaming)
            
        
        if df.empty:
            return
        
        # changing header
        if self.columnNaming._type not in df.columns:
            df.insert(1, self.columnNaming._type, pd.Series(self.columnNaming._unknownType, index=df.index))
        else:
            self.parsedCategories.extend(df[self.columnNaming._type].unique())
        df.insert(0, self.columnNaming._account, pd.Series(accountNumber, index=df.index))
        
        df.set_index(self.columnNaming._date, inplace=True)
        
        #remove empty entries
        df = df[df[self.columnNaming._value] != 0]
        
        if isinstance(self.df, pd.DataFrame):
            self.df = self.df.append(df)
        else:
            self.df = df;
        
        condition = self.df[self.columnNaming._client].str.contains('|'.join(self.accountNumbers), flags=re.IGNORECASE)==True
        self.df.ix[condition, self.columnNaming._type] = self.columnNaming._transfer
        self.df.sort_index(ascending=1, inplace=True)
        
        # add to account numbers
        self.accountNumbers.append(accountNumber)
        # add to current money
        self.currentMoney[accountNumber] = currentMoney
        
    def getCategories(self):
        return set(self.df[self.columnNaming._type].unique())
        
        
    def createMonthlySums(self, categories=None, filterPosValues=False, filterNegValues=False, negateValues=False, useParsedCategories=True):
        columnValue = self.columnNaming._value
        columnType = self.columnNaming._type
        columnInfo = self.columnNaming._info
        columnClient = self.columnNaming._client

        monthly = pd.DataFrame();
        
        if categories == None or not categories:
            monthly = self.df
        
        else:
            flat_list = []
            for sublist in categories:
                if type(sublist) is list:
                    for item in sublist:
                        flat_list.append(item)
                else:
                    flat_list.append(sublist)
            if useParsedCategories:
                flat_list.extend(self.parsedCategories)

            for category in set(flat_list):
                part = self.df[self.df[columnType].str.contains(re.escape(category))]
                monthly = monthly.append(part)
                
        if filterPosValues:
            monthly = monthly[monthly[columnValue] <= 0]
        if filterNegValues:
            monthly = monthly[monthly[columnValue] > 0]
        if negateValues:
            monthly[columnValue] = monthly[columnValue]*-1

        if monthly.empty:
            return monthly
            
        monthly.index = monthly.index.to_period('M')
        monthly = monthly.loc[:,[columnType, columnValue, columnClient]]
        monthly[columnInfo] = monthly[columnValue].apply(str) + ', ' + monthly[columnClient].apply(str) # concat money, info
        monthly[columnInfo] = monthly[columnInfo].str[:30] # shorten it to 30 chars
        aggFunc = { columnValue: { columnValue : lambda x: np.sum(x)}, columnInfo: { columnInfo : lambda x: '<br>'.join(x)}}
        monthlyTypes = monthly.groupby([monthly.index,columnType]).agg(aggFunc)
        monthlyTypes.columns = monthlyTypes.columns.droplevel(0)
        return monthlyTypes
    
    def createCurrentMoney(self):
        dictlist = []
        for key, value in self.currentMoney.items():
            temp = [key,value]
            dictlist.append(temp)
    
        #print(dictlist)
        zippedList = list(map(list, zip(*dictlist)))
        data = Pie(values=zippedList[1],
                labels=zippedList[0],
                textinfo="value",        
                visible=False)
        return data
         
        
    def plotCurrentMoney(self):
        dictlist = []
        for key, value in self.currentMoney.items():
            temp = [key,value]
            dictlist.append(temp)
    
        #print(dictlist)
        zippedList = list(map(list, zip(*dictlist)))
        plotly.offline.iplot({
            "data": [{
                "values": zippedList[1],
                "labels": zippedList[0],
                "type": "pie",
                "textinfo" : "value"}],
            "layout": Layout(
                title="Current money",
                autosize=False,
                width=800,
                height=350,
            )
        })
        return plotly.offline.plot({
            "data": [{
                "values": zippedList[1],
                "labels": zippedList[0],
                "type": "pie",
                "textinfo" : "value"}],
            "layout": Layout(
                title="Current money",
                autosize=False,
                width=800,
                height=350,
                )},
            output_type='div')
        
    def getMonthly(self, categories, filterPosValues=False, filterNegValues=False, negateValues=False,):
        monthly = self.createMonthlySums(categories, filterPosValues, filterNegValues, negateValues)
        monthly = monthly.unstack(1)[self.columnNaming._value].abs()
        monthly.reset_index(inplace=True)
        monthly.fillna(0, inplace=True)
        monthlyTable = monthly.describe()
        monthlyTable['sum'] = monthly.describe().sum(axis=1)
        return monthlyTable
    
    def createMonthlyStacked(self, categories, plotTitle, filterPosValues=False, filterNegValues=False, negateValues=False, useParsedCategories=True):
        columnValue = self.columnNaming._value
        columnInfo = self.columnNaming._info
        columnDate = self.columnNaming._date

        monthly = self.createMonthlySums(categories, filterPosValues, filterNegValues, negateValues)
        if monthly.empty:
            print('Dataframe is empty!')
            return
        
        # detailed info about payments 
        monthlyInfo = monthly.unstack(1)[columnInfo]
        monthlyInfo.reset_index(inplace=True)

        # rough values and month dates
        monthlyValue = monthly.unstack(1)[columnValue]
        monthlyValue.reset_index(inplace=True)
        if columnDate in monthlyValue.columns:
            monthlyValue = monthlyValue.set_index(columnDate)
        elif 'index' in monthlyValue.columns:
            monthlyValue = monthlyValue.set_index('index')
                
        data = []
        for column in monthlyValue.columns:
            data.append(
                Bar(
                    x=monthlyValue.index.map(str),
                    y=monthlyValue[column],
                    text=monthlyInfo[column],
                    name=column,
                    hoverlabel=dict( font=dict(color='white', size=8))
                ),
            )
            
        return data
        
    
    def plotMonthlyStackedBar(self, categories, plotTitle, filterPosValues=False, filterNegValues=False, negateValues=False, plotInNotebook=True, useParsedCategories=True):
        
        
        data = self.createMonthlyStacked(categories, plotTitle, filterPosValues, filterNegValues, negateValues, useParsedCategories)
        
        currentMoneyData = self.createCurrentMoney()
        
        # IPython notebook        
        plotly.offline.iplot({
                "data": data,
                "layout": Layout(
                    barmode='stack',
                    title=plotTitle,
                    autosize=True,
                    height=500,
                )
            })        
        return plotly.offline.plot({
                "data": data,
                "layout": Layout(
                    barmode='stack',
                    title=plotTitle,
                    autosize=True,
                    height=500,
                )
            }, output_type='div')
    
    def createMonthlyHTMLReport(self, filepath):
        divCurrentMoney = self.plotCurrentMoney()
        
        categories = self.getCategories()
        categories.remove(self.columnNaming._transfer)

        ids = {'expenses': 'Monatliche Kosten',
               'expensesDescribe': 'Monatliche Kosten Tabelle',
               'income': 'Einkommen',
               'transfer' : 'Verschiebungen'}

        divExpenses = self.plotMonthlyStackedBar(categories, plotTitle=ids['expenses'], filterPosValues=True, negateValues=True)
        divExpenses = '<div id="'+ids['expenses']+'" class="tabcontent">' + divExpenses + '</div>'
        monthlyExpenses = self.getMonthly(categories, filterPosValues=True, negateValues=True)
        divExpensesDescribe = "<div style='height:40px;'></div>" + monthlyExpenses.to_html()
        divExpensesDescribe = '<div id="'+ids['expensesDescribe']+'" class="tabcontent">' + divExpensesDescribe + '</div>'

        divIncome = self.plotMonthlyStackedBar(categories, filterNegValues=True, plotTitle=ids['income'])
        divIncome = '<div id="'+ids['income']+'" class="tabcontent">' + divIncome + '</div>'

        divTransfer = self.plotMonthlyStackedBar([self.columnNaming._transfer], plotTitle=ids['transfer'])
        divTransfer = '<div id="'+ids['transfer']+'" class="tabcontent">' + divTransfer + '</div>'

        divTabs = self.getTabDiv(list(ids.values()))
        divJS = self.getJS()
        f = open(filepath,'w')
        f.write(divTabs + divExpenses + divExpensesDescribe + divIncome + divTransfer + divJS)
        f.close()

    def getTabDiv(self, ids):
        div = """<style>
        /* Style the tab */
.tab {
    overflow: hidden;
    border: 1px solid #ccc;
    background-color: #f1f1f1;
}

/* Style the buttons that are used to open the tab content */
.tab button {
    background-color: inherit;
    float: left;
    border: none;
    outline: none;
    cursor: pointer;
    padding: 14px 16px;
    transition: 0.3s;
}

/* Change background color of buttons on hover */
.tab button:hover {
    background-color: #ddd;
}

/* Create an active/current tablink class */
.tab button.active {
    background-color: #ccc;
}

/* Style the tab content */
.tabcontent {
    display: block;
    padding: 6px 12px;
    border: 1px solid #ccc;
    border-top: none;
}
</style>
"""
        div += '<div class="tab">'
        for id in ids:
            div += '<button class="tablinks" onclick="openTab(event, \'' + id + '\')" >' + id + '</button>'
        div += '</div>'
        return div

    def getJS(self):
        return """
        <script>
        function hideAll(){
            // Get all elements with class="tabcontent" and hide them
            tabcontent = document.getElementsByClassName("tabcontent");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
            }

            // Get all elements with class="tablinks" and remove the class "active"
            tablinks = document.getElementsByClassName("tablinks");
            for (i = 0; i < tablinks.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }
        }
        function openTab(evt, tabName) {
            // Declare all variables
            var i, tabcontent, tablinks;

            hideAll()

            // Show the current tab, and add an "active" class to the button that opened the tab
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " active";
        } 
        
        hideAll()
        </script>
        """