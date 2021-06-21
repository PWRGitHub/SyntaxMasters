#!/usr/bin/env python
# coding: utf-8

# In[3]:


# FUNCTION: “GET FROM INTERNET” 

import urllib.request
from bs4 import BeautifulSoup


def GetFromInteret (Stock, YearGDP):
    """Gets Beta, Dividend, ROE, GDP_Growth, ExpInflRate, GerTenYRate for Stock, YearGDP"""

    # Funktion needs (Stock, YearGDP)
    stock = Stock

    # scrape from the net:
    # Beta for the stock
    # dividend for the stock
    # Return On Equity (In Percent)

    print ('looking for Beta, Dividend, and Return On Equity for the stock: ' + str(stock))
    print('')

    technicals = {}
    try:
        url = ('http://finance.yahoo.com/q/ks?s='+stock)
        print ('using following url: ')
        print (url)
        print('')
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')

        tables = soup.findAll('table')
        for table in tables:
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')

            for row in rows:
                col_name = row.find_all('span')      # Use span to avoid supscripts
                col_name = [cell.text.strip() for cell in col_name]
                #print ('col_name: ')
                #print (col_name)
                col_val = row.find_all('td')
                col_val = [cell.text.strip() for cell in col_val]
                #print ('col_value: ')
                #print (col_val)
                technicals[col_name[0]] = col_val[1] # col_val[0] is the name cell (with subscript)

    except Exception as e:
        print('Failed, exception: ', str(e))

    interested = ['Beta (5Y Monthly)', 'Trailing Annual Dividend Rate', 'Return on Equity']
    for ind in interested:
        print(ind + ": " + technicals[ind])
        print("------")

    Beta = technicals['Beta (5Y Monthly)']
    #print ('Beta: ' + str(Beta))
    Dividend = technicals['Trailing Annual Dividend Rate']
    #print ('Dividend: ' + str(Dividend))
    ROE = technicals['Return on Equity']
    #print ('ROE: ' + str(ROE))

    #-------------------------------------------------------------------------------------
    ###NEUE LÖSUNG MIT einem Excel Sheet 

    # scrape from the net:      
    # GDP growth (real)
    # Expected Inflation Rate

    import pandas as pd
    import numpy as np

    YearGDP = 2021
    print ('looking for GDP Growth and Expected Inflation Rate for year: ' + str(YearGDP))
    print ('')

    economicals = {}
    try:
        url = ('https://ec.europa.eu/info/business-economy-euro/economic-performance-and-forecasts/economic-performance-country/euro-area_en')
        page = urllib.request.urlopen(url)
        print ('using following url: ')
        print (url)
        print ('')
        soup = BeautifulSoup(page, 'html.parser')

        # Screaping the Table Head
        tableHead = soup.findAll('th', scope = "col")
        tableHead = [cell.text.strip() for cell in tableHead]
        print ('Table Head: ')
        print (tableHead)
        print('')

        #Scraping the Table Topics
        tableTopics = soup.findAll("td", class_ = 'topic')
        tableTopics = [cell.text.strip() for cell in tableTopics]
        print ('Table Topics:')
        print (tableTopics)
        print ('')

        #Scraping the Table Content
        tableContent = soup.findAll("td", class_ = 'content')
        tableContent = [cell.text.strip() for cell in tableContent]
        print ('Table Content:')
        print (tableContent)
        print ('')
        #Replacing al "," in Content List with "."
        print ('Replacing al "," in Content List with "."')
        tableContent = [i.replace(",", ".") for i in tableContent]
        print ('Table Content with dots, not commas:')
        print (tableContent)
        print ('')
        #Converting all strings in Content List to float items
        print ('Converting all strings in Content List to float items')
        tableContent = [float(i) for i in tableContent]
        print ('Converted Table Content with float items only:')
        print (tableContent)
        print ('')
        #Dividing Table Content in Years
        print ('Dividing Table Content in Years')
        print ('length Table Head: ' + str(len(tableHead)))
        print ('')
        tableContentYears = [1, 2, 3, 4, 5, 6]
        for n in range(len(tableHead)-1):
            print ('n: ' + str(n))
            tableContentYears[n] = [tableContent[n], tableContent[n+4], tableContent[n+8], tableContent[n+12], tableContent[n+16], tableContent[n+20]]
            print ('Table Content Year: ' + str(tableHead[n+1]))
            print (tableContentYears[n])
            print ('')


        ##Building Excel Sheet out of Head Topics and Content

        #Creating empty Excel File
        writer = pd.ExcelWriter('euro_area_eco_forcast.xlsx', engine='xlsxwriter')
        writer.save()

        #Opening created Excel File
        forcastSheet = pd.read_excel('euro_area_eco_forcast.xlsx')

        #Constructing Forcast Dictionary.
        print ('Adding Table Topics to Forcast Dictionary')
        forcastDict = {tableHead[0]: tableTopics}
        print ('Forcast Dictionary with Table Topics: ')
        print (forcastDict)
        print ('')

        for n in range(len(tableHead)-1):
            print ('Adding Table Content for Year: ' + str(tableHead[n+1]))
            forcastDict[tableHead[n+1]] = tableContentYears[n]
            print (str(forcastDict[tableHead[n+1]]))
        print ('')
        print ('Forcast Dictionary: ')
        print (forcastDict)
        print ('')


        ##Constructing DataFrame from a dictionary.

        print ('Constructing DataFrame from a dictionary:')
        forcastSheet = pd.DataFrame(data=forcastDict)
        print ('Forcast Sheet')
        forcastSheet

        print (forcastSheet.head())
        print ('')

        #Transfering GDP Groth value for needed Year to Return Variable.
        print ('Transfering GDP Growth value for Year ' + str(YearGDP) + ' to Return Variable.')
        print (forcastSheet.loc[0])
        GDP_Growth = forcastSheet.at[0, str(YearGDP)]
        print ('GDP_Growth = ' + str(GDP_Growth))
        print ('')

        #Transfering Expected Inflation Rate value for needed Year to Return Variable.
        print ('Transfering Expected Inflation Rate value for Year ' + str(YearGDP) + ' to Return Variable.')
        print (forcastSheet.loc[1])
        ExpInflRate = forcastSheet.at[1, str(YearGDP)]
        print ('ExpInflRate = ' + str(GDP_Growth))
        print ('')

        writer = pd.ExcelWriter('./euro_area_eco_forcast.xlsx')
        forcastSheet.to_excel(writer, 'euro_area_eco_forcast')
        writer.save()

    except Exception as e:
        print('Failed, exception: ', str(e))

    #------------------------------------------------------------------------------------
    # German 10 Year Bond Rate (-0,25%)
    print ('Looking for current German Ten Year Bond Rate...')

    try:
        url = ('https://www.deutsche-finanzagentur.de/de/institutionelle-investoren/')
        page = urllib.request.urlopen(url)
        print ('using following url: ')
        print (url)
        print ('')
        soup = BeautifulSoup(page, 'html.parser')

        # Screaping the German 10 Year Bond Rate
        print ('Finding all Division Tags "div" with class "valueCont center":')
        divTags = soup.findAll('div', class_ = "valueCont center")
        print (divTags)
        print ('')

        print ('extracting "span" Tag:')
        for divTag in divTags:
            spanTag = divTag.find_all('span')
        print (spanTag)
        print ('')

        print ('Striping Text from "span" Tag:')
        GerTenYRate = [cell.text.strip() for cell in spanTag]
        print ('converting Variable from list to String:')
        GerTenYRate = GerTenYRate[0]
        print (type (GerTenYRate))
        print ('German 10 Year Bond Rate als String: ')
        print ('GerTenYRate = ' + str(GerTenYRate))
        print ('')

    except Exception as e:
        print('Failed, exception: ', str(e))   


    # FUNCTION RETURN: (GDP_Growth, ExpInflRate, Beta, Dividend, GerTenYRate, ROE)
    return Beta, Dividend, ROE, GDP_Growth, ExpInflRate, GerTenYRate

Stock = 'DAI.DE'
YearGDP = '2021'
result = GetFromInteret (Stock, YearGDP)
print ('The Funktion returns ')
print ('Beta, Dividend, ROE, GDP_Growth, ExpInflRate, GerTenYRate')
print ('as a Tuple-Variable:')
print (result)

