from data_hunting import getDeparturesFromTerminus, makeListOfDepartures
from hours import findClosestHoursFromVariations


SCHEDULE_PAGE_NUMBER = 1
SCHEDULE_VARIATION = ["LUNDI au VENDREDI", "SAMEDI", "DIMANCHE"]


def main():
    printScheduleChanges(45)


def printDepartures(lineNumber: int, futureSchedule : bool = False) -> None:
    content = "Horaire actuel:\n" if not futureSchedule else "Horaire à venir:\n"
    departures = getDeparturesFromTerminus(lineNumber, futureSchedule).split("Direction")

    variationCount = 0
    for variation in departures:
        if len(variation) > 10:
            if variationCount < 6:
                content += '\n' + SCHEDULE_VARIATION[variationCount // 2] + '\n'
                variationCount += 1
            content += "Direction" + variation

    print(content)



def printScheduleChanges(lineNumber: int) -> None:
    try:
        currentDepartures = makeListOfDepartures(lineNumber)
        futureDepartures = makeListOfDepartures(43, True)

        currentVariation = 0
        scheduleComparaison = findClosestHoursFromVariations(currentDepartures, futureDepartures)

        for i, variation in enumerate(scheduleComparaison):
            print('\n' + SCHEDULE_VARIATION[currentVariation // 2])
            currentVariation += 1
        
            moreDepartures = hasMoreDeparture(len(currentDepartures[i]), len(futureDepartures[i]))

            for time, otherTime in variation:
                line = str(otherTime + " -> " + time) if moreDepartures else str(time + " -> " + otherTime)

                if 'X' in time or 'X' in otherTime:
                    line += "\t  NOUVEAU PASSAGE" if moreDepartures else "\tPASSAGE RETIRÉ"
                elif time != otherTime:
                    line += "\t    CHANGEMENT"

                print(line)
    except:
        print("ERREUR : Hors période de changement d'horaire...")



def hasMoreDeparture(currentDepartureNb: int, futureDepartureNb: int) -> bool:
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