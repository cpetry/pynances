from datetime import datetime
from dateutil.relativedelta import relativedelta
import plotly
from plotly.graph_objs import Bar, Layout, Scatter

class Annuity():
    class AnnuityInfo():
        def __init__(self, loan, interest, annuity, startDate, duration):
            self._loan = loan
            self._interest = interest
            self._annuity = annuity
            self._startDate = startDate
            self._timeLimited = (duration != 0)
            self._duration = duration
            
    class AnnuityData():
        def __init__(self, loan, date, interest, repayment):
            self._loan = loan
            self._date = date
            self._interest = interest
            self._repayment = repayment

    def __init__(self, loan, interest, annuity, startDate=datetime.now(), duration=0):
        self._annuityInfo = []
        self.addAnnuity(loan, interest, annuity, startDate, duration)
        
    def addAnnuity(self, loan, interest, annuity, startDate=datetime.now(), duration=0):
        self._annuityInfo.append(Annuity.AnnuityInfo(loan, interest, annuity, startDate, duration))
    
    def plotAnnuityGraph(self):
        annuityDataGroup = []
        self.annuityCurrentMonth(self._annuityInfo, annuityDataGroup)
        deltaYears = annuityDataGroup[0][-1]._date.year - datetime.now().year
        startMonth = datetime.now().month
        endMonth = annuityDataGroup[0][-1]._date.month
        
        if startMonth > endMonth:
            deltaMonths = startMonth - 12 + endMonth
        else:
            deltaMonths = endMonth - startMonth
        
        loan = self._annuityInfo[0]._loan
        interest = self._annuityInfo[0]._interest
        annuity = self._annuityInfo[0]._annuity
        
        titleStr = "Time: " + "{:10.2f}".format(deltaYears + (deltaMonths/12)) + " Years\n" + "Loan: " + str(loan) + "€ Interest: " + str(interest) + " Annuity: " + str(annuity) + "€"
        
        data = []

        for annuityData in annuityDataGroup:
            dataDates     = [x._date for x in annuityData]
            dataLoan      = [x._loan for x in annuityData]
            dataInterest  = [x._interest for x in annuityData]
            dataRepayment = [x._repayment for x in annuityData]
            
            data.append(
                Scatter(
                    x=dataDates,
                    y=dataRepayment,
                    name='repayment',
                )
            )
            data.append(
                Scatter(
                    x=dataDates,
                    y=dataInterest,
                    name='interest',
                )
            )
            data.append(
                Scatter(
                    x=dataDates,
                    y=dataLoan,
                    name='loan',
                    fill='tonexty'
                )
            )
        
        # IPython notebook
        plotly.offline.iplot({
            "data": data,
            "layout": Layout(
                barmode='stack',
                title=titleStr,
                autosize=True,
            )
        })
        
        return plotly.offline.plot({
            "data": data,
            "layout": Layout(
                barmode='stack',
                title=titleStr,
                autosize=True,
            )
        }, output_type='div')
        
    def annuityCurrentMonth(self, annuityInfoGroup, annuityDataGroup):
        completeLoan = 0
        additionalAnnuity = 0
        for i in range(0,len(annuityDataGroup)):
            if annuityDataGroup[i][-1]._loan == 0:
                additionalAnnuity = additionalAnnuity + annuityInfoGroup[i]._annuity
        
        for i in range(0,len(annuityInfoGroup)):
            if len(annuityDataGroup) < i+1:
                annuityDataGroup.append([])
                currentLoan = annuityInfoGroup[i]._loan
                currentDate = annuityInfoGroup[i]._startDate
            else:
                currentLoan = annuityDataGroup[i][-1]._loan
                currentDate = annuityDataGroup[i][-1]._date

            interest = annuityInfoGroup[i]._interest * currentLoan / 100 / 12
            annuity = annuityInfoGroup[i]._annuity
            if currentLoan > 0:
                annuity = annuity + additionalAnnuity
            repayment = min(annuity - interest, currentLoan)
            currentLoan = currentLoan - repayment
            currentDate = currentDate + relativedelta(months=1)

            annuityDataGroup[i].append(
                Annuity.AnnuityData(currentLoan,currentDate,interest,repayment))
            
            completeLoan = completeLoan + currentLoan
                
        if (completeLoan > 0):
            self.annuityCurrentMonth(annuityInfoGroup, annuityDataGroup)