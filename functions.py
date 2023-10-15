import copy
import datetime
import os
import re
from pathlib import Path
from Args import Args
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
def getFilteredEntries(searchStr):
    sortedEntries = sortEntries(False, False, False)

    filtered = list()
    searchStr = searchStr.lower()  # ignore case during search.
    for e in sortedEntries:
        if re.search(searchStr, e.activity.lower()):
            filtered.append(e)

    return filtered


# prints all entries with optional options
def printAllEntries(reversed, showDedicatedHours, showCalendarSpan, sortByDH, sortByCS):
    sortedEntries = sortEntries(sortByDH, sortByCS, reversed)

    # Imitate a pager (like git log)
    lines = shutil.get_terminal_size().lines
    output = ''
    for i in range(len(sortedEntries)):
        output += sortedEntries[i].getAsStr(showDedicatedHours, showCalendarSpan) + '\n'
        if i and (i % lines == 0 or i == len(sortedEntries) -1):
            print(output, end='')
            if i != len(sortedEntries) -1:
                input('*'*10 + ' press Enter to show next page ' + '*'*10)
            output = ''

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
def sum_(searchStr):
    filtered = getFilteredEntries(searchStr)
    if len(filtered) == 0:
        print(f'Activity \'{searchStr}\' was not found!')
        return

    # print sum
    print(_summarizeEntries(filtered, searchStr).getAsStr(1,1))

    # print detailed view
    print('\nDetailed view:')
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
        lines[i] = re.sub(r'\s[\[(][\w, ]*last one[\w, !?\])]*', '', lines[i],
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
            if file.endswith('.txt'):
                txtFilePath = os.path.join(dirPath, file)
                lines = removeInactivePart(txtFilePath)
                lines = removeTrailingTags(lines)
                addEntries(lines, Path(file).stem)


def printHelp():
    print('Dedicated hours counter\n'
          'v.1.0.0 released: 15.10.2023\n'
    '=============== command: list ===============\n'
    'list <dir_path> [options]\n'
    'list <dir_path> /<regex_sub_str>\n'
    'Lists all entries in dir_path using specified options or show entries that only match regex_sub_str.\n'
    'You can combine options to achieve the desired output.\n'
    'Possible options:\n'
    '    r - show entries in reverse order\n'
    '    d - show total amount of dedicated hours\n'
    '    c - show calendar span in days between first entry and last one\n'
    '    sd - sort by amount of dedicated hours\n'
    '    sc - sort by amount of calendar span\n'
    '\n'
    '    /<regex_sub_str> - show entries that only match the sub-string')

    print('')
    print('=============== command: sum ===============\n'
    'sum <dir_path> <activity_regex_str>\n'
    'Summarizes total number of dedicated hours for the specified activity_regex_str'
    'in dir_path.\n')

# Parses user arguments
def parseCommand(argv):
    args = getArgs(argv)
    collectAllEntries(args.dirPath)  # must be executed before any command

    if args.cmd == 'list':
        if args.activityStr:
            for e in getFilteredEntries(args.activityStr):
                print(e.getAsStr(True, True))
        else:
            printAllEntries('r' in args.options, 'd' in args.options,
                    'c' in args.options, 'sd' in args.options, 'sc' in args.options)
    elif args.cmd == 'sum':
        sum_(args.activityStr)
    elif args.cmd == 'help':
        printHelp()


def getArgs(argv):
    count = len(argv) -1  # -1 to ignore 0th argument, which is always the path of the script
    result = Args()
    if count == 0 or argv[1] in ('help','-h','/h','/?'):
        result.cmd = 'help'
        return result
    if count >= 2:  # 1st argument is always the command, 2nd the dirPath
        result.cmd = argv[1]
        result.dirPath = argv[2]

    if result.cmd == 'list':
        if count == 3 and argv[3][0] == '/':
            result.activityStr = argv[3][1:]
        elif count >=3:
            result.options = argv[3:]
    elif result.cmd == 'sum':
        result.activityStr = argv[3]
    else:
        print('Unsupported command. Exiting')
        exit(1)
        
    return result
