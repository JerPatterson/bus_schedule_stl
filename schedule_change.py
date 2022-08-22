from data_hunting import makeListOfDepartures
from hours import findClosestHoursFromVariations


SCHEDULE_PAGE_NUMBER = 1
SCHEDULE_VARIATION = ["Dimanche", "Samedi", "Lundi au Vendredi"]


def main():
    printScheduleChanges(45)


def printDepartures(lineNumber: int, futureSchedule : bool = False) -> None:
    content = "\n" if not futureSchedule else "\nHoraire à venir:"
    schedule = makeListOfDepartures(lineNumber, futureSchedule)

    currentVariation = 0
    for variations in schedule:
        content = '\n' + SCHEDULE_VARIATION[currentVariation // 2] + '\n'
        currentVariation += 1
        
        for hour in variations:
            content += hour + ' '

    print(content + '\n')


def printScheduleChanges(lineNumber: int):
    currentDepartures = makeListOfDepartures(lineNumber)
    futureDepartures = makeListOfDepartures(lineNumber, True)

    currentVariation = 0
    scheduleComparaison = findClosestHoursFromVariations(currentDepartures, futureDepartures)

    for i, variation in enumerate(scheduleComparaison):
        print('\n' + SCHEDULE_VARIATION[currentVariation // 2])
        currentVariation += 1
    
        moreDepartures = isMoreDeparture(len(currentDepartures[i]), len(futureDepartures[i]))

        for time, otherTime in variation:
            line = str(otherTime + " -> " + time) if moreDepartures else str(time + " -> " + otherTime)

            if 'X' in time or 'X' in otherTime:
                line += "\t  NOUVEAU PASSAGE" if moreDepartures else "\tPASSAGE RETIRÉ"
            elif time != otherTime:
                line += "\t    CHANGEMENT"

            print(line)


def isMoreDeparture(currentDepartureNb, futureDepartureNb):
    departureChange = futureDepartureNb - currentDepartureNb

    if departureChange > 0:
        print(f"{abs(departureChange)} départs ont été ajouté" + ("s. " if abs(departureChange) > 1 else ". ") +
            f"Maintenant {futureDepartureNb} départs.")
        return True 

    elif departureChange == 0:
        print(f"Toujours autant de départ ({currentDepartureNb}).")
    elif departureChange < 0:
        print(f"{abs(departureChange)} départs ont été retiré" + ("s. " if abs(departureChange) > 1 else ". ") +
            f"Maintenant {futureDepartureNb} départs.")

    return False



if __name__ == "__main__":
    main()