#parse.py

from bs4 import BeautifulSoup
import requests
import sys

#function to parse page source raw data
def parsePageSource(page_source):
    
    parseFile = "output.txt"                                                                                                #File storing parsed data
    soup = BeautifulSoup(page_source, "html.parser")

    #read input and save to list
    flight_rows = soup.find_all("div", class_ = "app-components-Shopping-GridItem-styles__flightRow--1E4Sk")                #Flight rows per website
    rows = (len(flight_rows))

    flight_elements = [[[] for _ in range(7)] for _ in range(rows)]                                                         #List to hold flight information per flight

    rowIndex = 0
    for flight_rows in flight_rows:
        flight_info = flight_rows.find_all("span", class_ = "app-components-AriaMessage-styles__visuallyHidden--2RXE0")     #Same class is used for almost all relevant text
        colIndex = 0
        for flight_info in flight_info:
            flight_elements[rowIndex][colIndex].append(flight_info.text.strip())
            colIndex += 1
        flight_elements[rowIndex][colIndex].append(flight_rows.find("div", class_ = "app-components-Shopping-PriceCard-styles__top--2IU8G").get_text()) #Get miles and cost
        rowIndex += 1

    #write to file
    with open(parseFile, "w") as f:                    
        for i in range(len(flight_elements)):
            for j in range(len(flight_elements[i])):
                print(*flight_elements[i][j], file = f)
            print("", file = f)