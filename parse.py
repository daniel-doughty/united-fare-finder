# parse.py

from bs4 import BeautifulSoup


def parsePageSource(page_source):
    # function to parse page source raw data

    soup = BeautifulSoup(page_source, "html.parser")

    # flight listings per website layout (from top to bottom)
    flight_rows = soup.find_all(
        "div",
        class_="app-components-Shopping-GridItem-styles__flightRow--1E4Sk")
    rows = (len(flight_rows))

    # list to hold flight information for each flight
    flight_elements = [[[] for _ in range(7)] for _ in range(rows)]

    rowIndex = 0
    for flight_rows in flight_rows:

        # same class is used for almost all relevant text
        flight_info = flight_rows.find_all(
            "span",
            class_="app-components-AriaMessage-styles__visuallyHidden--2RXE0")

        colIndex = 0
        for flight_info in flight_info:
            flight_elements[rowIndex][colIndex].append(
                flight_info.text.strip())
            colIndex += 1

        # miles and cost uses a different class
        flight_cost = flight_rows.find(
            "div",
            class_="app-components-Shopping-PriceCard-styles__top--2IU8G")
        flight_elements[rowIndex][colIndex].append(
            flight_cost.text.strip())
        rowIndex += 1

    # write to file
    parseFile = "output.txt"
    with open(parseFile, "w") as f:
        for i in range(len(flight_elements)):
            for j in range(len(flight_elements[i])):
                print(*flight_elements[i][j], file=f)
            print("", file=f)
