import copy
import datetime
import os
import re
from pathlib import Path
from Entry import Entry

# Global list that contains all entries
entries = dict()


# returns a list of Entry objects
def sortEntries(sortByDH, sortByCS, reversed):
    resultList = list(entries.values())

    if sortByDH:
        resultList.sort(key=lambda e: e.minutes)
    elif sortByCS:
        resultList.sort(key=lambda e: e.calcCalendarSpan())
    else:
        resultList.sort(key=lambda e: e.activity.lower())

    if reversed:
        resultList.reverse()
    return resultList


# Returns a list of Entries that match 'searchStr'.
# If exactSearch is True, searchStr is treated like a usual String and must match exactly.
# If exactSearch is False, searchStr is treated like a Regex pattern and partial search will be perfomed.
def getFilteredEntries(searchStr, exactSearch=False):
    sortedEntries = sortEntries(False, False, False)

    filtered = list()
    searchStr = searchStr.lower()  # ignore case during search.
    if exactSearch:
        for e in sortedEntries:
            if searchStr == e.activity.lower():
                filtered.append(e)
    else:
        for e in sortedEntries:
            if re.search(searchStr, e.activity.lower()):
                filtered.append(e)

    return filtered


# prints all entries with optional options
def printAllEntries(reversed, showDedicatedHours, showCalendarSpan, sortByDH, sortByCS):
    sortedEntries = sortEntries(sortByDH, sortByCS, reversed)
    for e in sortedEntries:
        print(e.getAsStr(showDedicatedHours, showCalendarSpan))

    print('\n' + '='*15 + ' Total amount of activities: ' + str(len(sortedEntries)) + ' ' + '='*15)


# Combines all Entries in filteredEntries into one Entry object
def _summarizeEntries(filteredEntries, name):
    sumEntry = copy.deepcopy(filteredEntries[0])
    sumEntry.activity = name
    for i in range(len(filteredEntries) - 1):
        sumEntry.minutes += filteredEntries[i + 1].minutes
        sumEntry.setLastDay(filteredEntries[i + 1].lastDay)
    return sumEntry


# You must call collectAllEntries() function before calling sum_()!
# Collects activities that match 'searchStr' and prints summarized DH and CS.
# For 'exactMatch' meaning, check documentation of getFilteredEntries() function.
def sum_(searchStr, exactMatch):
    filtered = getFilteredEntries(searchStr, exactMatch)
    if len(filtered) == 0:
        print(f'Activity \'{searchStr}\' was not found!')
        return

    # print sum
    print(_summarizeEntries(filtered, searchStr).getAsStr(1,1))

    # print detailed view
    print('\n\nDetailed view:')
    for e in filtered:
        print(e.getAsStr(True, True))


# Takes purified lines and adds them to the global 'entries' variable
def addEntries(lines, day):
    for line in lines:
        entry = extractEntry(line)
        date = datetime.datetime.strptime(day, '%d.%m.%Y')
        entry.setLastDay(date)
        key = entry.activity.lower()
        if not(key in entries):     # add a brand new entry
            entries[key] = entry
        else:
            entries[key].minutes += entry.minutes
            entries[key].setLastDay(entry.lastDay)


# Removes all lines after '------' separator in the file
def removeInactivePart(filePath):
    with open(filePath, 'r', encoding='utf-8-sig') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            if '---' in lines[i] and i > 0:
                return lines[:i]
    return []


# Removes extra "tags" from the lines
def removeTrailingTags(lines):
    for i in range(len(lines)):
        lines[i] = lines[i].replace(" (couldn't stop)", '')  # remove (couldn't stop) tag
        lines[i] = re.sub(r'\s[\[\(][\w, ]*last one[\w, !?\]\)]*', '', lines[i],
                          flags=re.IGNORECASE)  # remove [last one] tags
        lines[i] = lines[i].strip()  # remove \n
    return lines


# Takes a string like "30' Learning Python" and converts to an Entry object
def extractEntry(string):
    match = re.match(r'^((\d+)[\s\']+)?(.*)', string)
    if match.group(2) is not None:
        mins = int(match.group(2))
    else:
        mins = 60

    activity = match.group(3)
    return Entry(mins, activity)


# Walks through all files and collects all data into 'entries' dictionary
def collectAllEntries(pathToDir):
    for dirPath, dirs, files in os.walk(pathToDir):
        for file in files:
            txtFilePath = os.path.join(dirPath, file)
            lines = removeInactivePart(txtFilePath)
            lines = removeTrailingTags(lines)
            addEntries(lines, Path(file).stem)
