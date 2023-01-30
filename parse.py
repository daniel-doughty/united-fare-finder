# parse.py

def parsePageSource(soup):
    # function to parse page source raw data

    # flight listings per website layout (from top to bottom)
    flight_rows = soup.find_all(
        "div",
        class_="app-components-Shopping-GridItem-styles__flightRow--1E4Sk")

    # list to hold flight information for each flight
    flight_elements = [[[] for _ in range(7)] for _ in range(len(flight_rows))]

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

    return flight_elements
