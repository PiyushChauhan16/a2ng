from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import csv
    
class CSV():
    def __init__(self):
        pass

    def CSVGenerator(self,header, data, fileName="output", filePath="./"):
        csv_file = filePath+fileName+".csv"
    
        print(header)
        print(data)

        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows([header])
            writer.writerows(data)
        


class WebScraper():
    def __init__(self):
        self._driver = webdriver.Chrome (service=Service(ChromeDriverManager().install()), options= Options().add_experimental_option("detach", True))

    # This can be improved by using FluentWait instead of explicit wait.
    def _waitTillPageLoads(self):
        time.sleep(10)

    #function to start the driver
    def startDriver(self):
        self._driver.get("https://data.stats.gov.cn/english/easyquery.htm?cn=A01")
    
    #function used to open the drop down menu based on the levels
    def OpenDropDown(self, level, requiredEntry):
        #waiting to ensure the element is available while parsing
        #The code gives runtime error in case of exception
        #TODO: Use try-catch for better error handling
        self._waitTillPageLoads()

        levelEntries = self._driver.find_elements(By.CLASS_NAME, "level"+str(level))
        for entry in levelEntries:
            print("entry", entry.get_attribute("innerHTML"))
            if requiredEntry in entry.get_attribute("innerHTML"):
                entry.find_element(By.TAG_NAME, 'a').click()
                return
    
    #function to set filter
    def SetFilter(self, value):
        filterRef = self._driver.find_element(By.CLASS_NAME, "dtHtml").find_element(By.CLASS_NAME, "dtHead")
        filterRef.click()

        input = self._driver.find_element(By.CLASS_NAME, "dtText")
        input.send_keys(value)

        submitBtn = self._driver.find_element(By.CLASS_NAME, "dtTextBtn")
        submitBtn.click()

    #function to scrap data from the table based on indicator
    def GetData(self, indicator):
        self._waitTillPageLoads()
        soup = BeautifulSoup(self._driver.page_source, "html.parser")
        data = []
        header = []
    
        for tr in soup.find("table", class_= "public_table").find("thead").find_all("tr"):
            for th in tr:
                header.append(th.text)
                    
    
        for tr in soup.find("table", class_= "public_table").find("tbody").find_all("tr"):
            isValid = False
            for td in tr:
                if isValid == False:
                    if td.text == indicator:
                        isValid = True
                    else:
                        continue
                
                # 0 is used to initialise the fields with no data
                if isValid == True:
                    if td.text == "":
                        data.append("0")
                    else:
                        data.append(td.text)
                    
        return [header,data]

    #function to sanitize the header i.e converting May 2024 to 2024-05-31
    def Sanitize(self, data):
        def isLeapYear(year):
            if (year % 4 == 0):
                if (year % 100 == 0):
                    if (year % 400 == 0):
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                return False
            
        exHeader = data[0]
        exData = data[1]
        
        dates = {
            "Jan": "01-31",
            "Feb": "02-28",
            "Feb-leap":"02-29",
            "Mar": "03-31",
            "Apr": "04-30",
            "May": "05-31",
            "Jun": "06-30",
            "Jul": "07-31",
            "Aug": "08-31",
            "Sep": "09-30",
            "Oct": "10-31",
            "Nov": "11-30",
            "Dec": "12-31"
        }
        header = []

        for value in exHeader:
            if value == "Indicators":
                header.append(value)
            else:
                month = value[0:3]
                year = value[4:]

                #takes leap year into consideration
                if isLeapYear(int(year)):
                    if month == "Feb":
                        header.append('\"'+year+"-"+dates[month+"-leap"]+'\"')
                    else:
                        header.append('\"'+year+"-"+dates[month]+'\"')
                else:
                    header.append('\"'+year+"-"+dates[month]+'\"')
        
        return [header, data]




requiredFields = [
    "Thermal Power", 
    "Hydro-electric Power",
    "Nuclear Power", 
    "Wind Power", 
    "Solar power"
]
requiredIndicators = [
    "Output of Thermal Power, Current Period(100 million kwh)",
    "Output of Hydro-electric Power, Current Period(100 million kwh)",
    "Output of Nuclear Power, Current Period(100 million kwh)",
    "Output of Wind Power, Current Period(100 million kwh)",
    "Output of Solar Power, Current Period(100 million kwh)"
]

ws = WebScraper()
ws.startDriver()
ws.OpenDropDown(1, "Energy")
ws.OpenDropDown(2, "Output of Energy Products")
ws.SetFilter("2015-") 

header = []
data = []
for i in range(len(requiredFields)):
    ws.OpenDropDown(3, requiredFields[i])
    res = ws.GetData(requiredIndicators[i])
    
    if i == 0:
        sanitisedRes = ws.Sanitize(res)
        header = sanitisedRes[0]
    data.append(res[1])
        

CSV().CSVGenerator(header, data)