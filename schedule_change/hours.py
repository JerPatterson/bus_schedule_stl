from typing import List, Tuple


def findClosestHoursFromVariations(currentSchedule: List[List[str]], upcomingSchedule: List[List[str]]) -> List[List[str]]:
    closestHours = []

    for i in range(len(currentSchedule)):
        closestHours.append(findClosestHours(currentSchedule[i], upcomingSchedule[i]))

    return closestHours


def findClosestHours(hours: List[str], otherHours: List[str]) -> List[Tuple[str]]:
    differences = []
    matchingHours = hours if len(hours) >= len(otherHours) else otherHours

    bestDifference = difference = bestMatch = 0
    for i, time in enumerate(matchingHours):
        for otherTime in hours if len(hours) < len(otherHours) else otherHours:
            hour, minute = Tuple(time.split(':'))
            otherHour, otherMinute = Tuple(otherTime.split(':'))
            if hour == otherHour:
                difference = abs(int(minute) - int(otherMinute))

                if difference < bestDifference or difference == 0 or bestDifference == 0:
                    bestDifference = difference
                    bestMatch = (hour, otherHour)

                if difference == 0:
                    break
        
        matchingHours[i] = bestMatch
        differences.append(bestDifference)
        bestDifference = 0

    return eliminateSameHours(matchingHours, differences)


def eliminateSameHours(matches: List[Tuple[str]], differences: List[int]) -> List[Tuple[str]]:
    for i, match in enumerate(matches[:len(matches) - 2]):
        if match[1] == matches[i - 1][1]:
            if differences[i] > differences[i-1]:
                matches[i] = (match[0], "X:XX")
        elif match[1] == matches[i+1][1]:
            if differences[i] > differences[i+1]:
                matches[i] = (match[0], "X:XX")

    return matches
    