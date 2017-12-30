# Pynances
Python library to read in bank account csv files and print out some financial graphs.

- Currently only usable inside python notebooks (jupyter).
- Categories can be defined by the user himself.
- Multiple bank accounts can be merged together.
- Annuity loans can be calculated and plotted as graph ouput.

### Security: Every file and every data is processed and displayed locally! 

Categories can be defined like this:
```python
categories = {
    'Overhead'     : ['Evil landlord', 'Insurance'],
    'Orderings'    : ['Amazon', 'Paypal'],
    'Housekeeping' : ['Rewe', 'Aldi', 'Real', 'Edeka', 'E-Center', 'Rossmann', 'OBI', 'LIDL'],
    'Gas'          : ['Aral', 'Esso', 'Shell', 'Total', 'Jet', 'OMV', 'ELO', 'SUPOL'],    
    'Income'       : ['Some Company']}
```

Example html output (plotly) see here:
https://github.com/cpetry/pynances/blob/master/example.html

Example graph outputs (plotly) see below:

![Expenses screenshot](https://github.com/cpetry/pynances/blob/master/screenshot_expenses.PNG "Expenses")

![Income screenshot](https://github.com/cpetry/pynances/blob/master/screenshot_income.PNG "Expenses")

See example notebook for usage!
