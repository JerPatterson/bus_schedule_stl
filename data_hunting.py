from urllib import request
from PyPDF4 import PdfFileReader
from io import BytesIO
from typing import List
from copy import deepcopy


def readSchedulePdf(lineNumber: int, futureSchedule = False) -> List[str]:
    if not futureSchedule:
        url = f"https://stlaval.ca/public/stl/maps/routes/{lineNumber}.pdf" 
    else:
        url = f"https://stlaval.ca/public/stl/maps/routes/futur-horaire/{lineNumber}.pdf"

    remoteFile = request.urlopen(url).read()
    memoryFile = BytesIO(remoteFile)
    pdfFile = PdfFileReader(memoryFile)

    wholeDocText = []
    for page in pdfFile.pages:
            text = page.extractText()
            wholeDocText.append(text.split(' '))

    return wholeDocText


def getDepartures(lineNumber: int, futureSchedule : bool = False) -> str:
    schedule = readSchedulePdf(lineNumber, futureSchedule)

    departures = ""
    memorize = False
    for word in schedule[1]:

        if "Départ" in word:
            departures += '@'
            memorize = True

        elif memorize and len(word) > 4 and word[3] == 'h':
            departures += word

        else:
            memorize = False

    return departures


def formatDepartures(departureTimes: str) -> str:
    textFormated = ""
    
    for char in departureTimes:
        if char.isdigit() or char == 'h' or char == '@':
            textFormated += char

    return textFormated


def makeListOfDepartures(lineNumber: int, futureSchedule = False) -> List[str]:
    variationList = []
    departuresList = []
    departureTimes = formatDepartures(getDepartures(lineNumber, futureSchedule))

    content = ""
    digitEncountered = 0
    for char in departureTimes:
        if char.isdigit():
            digitEncountered += 1
        elif char == '@':
            if len(variationList) != 0:
                departuresList.append(deepcopy(variationList))
                variationList = []
            continue
        elif digitEncountered == 0 or char != 'h':
            continue

        content += char

        if digitEncountered == 4:
            digitEncountered = 0
            variationList.append(content)
            content = ""
    
    departuresList.append(deepcopy(variationList))

    return departuresList