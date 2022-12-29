from urllib import request
from pypdf import PdfReader
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
    pdfFile = PdfReader(memoryFile)

    text = ""
    for page in pdfFile.pages:
            text += page.extract_text()

    return text.split(' ')


def getDeparturesFromTerminus(lineNumber: int, futureSchedule : bool = False) -> str:
    stopsSchedule = readSchedulePdf(lineNumber, futureSchedule)

    departures = ""
    appendInfos = False
    appendTimes = False
    for word in stopsSchedule:
        if "Direction" in word:
            departures += "\nDirection "
            appendInfos = appendTimes = True
        elif appendTimes and len(word) >= 4 and (word[1] == ':' or word[2] == ':'):
            departures += ("\n" if appendInfos else " ") + word[:5]
            appendInfos = False
        elif appendInfos:
            departures += word + " "
        elif '\n' not in word:
            appendTimes = False

    return departures


def makeListOfDepartures(lineNumber: int, futureSchedule = False) -> List[str]:
    variationList = []
    departuresList = []
    departureTimes = getDeparturesFromTerminus(lineNumber, futureSchedule)

    for word in departureTimes.split(' '):
        word = word.removeprefix("\n")
        if len(word) >= 4 and (word[1] == ':' or word[2] == ':'):
            variationList.append(word[:5].removesuffix("\n"))
            
        if "Direction" in word:
            if len(variationList) != 0:
                departuresList.append(variationList[:])
                variationList = []
    
    departuresList.append(variationList[:])

    return departuresList