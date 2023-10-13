import re

from Entry import Entry


def printAllEntries(entries):
    sortedEntries = list(entries)
    sortedEntries.sort()
    for e in sortedEntries:
        # print(entries[e].activity)
        print(entries[e])


# Takes purified lines and adds them to the 'entries' variable
def addEntries(entries, lines):
    for line in lines:
        entry = extractEntry(line)
        key = entry.activity.lower()
        if not(key in entries):     # add a brand new entry
            entries[key] = entry
        else:
            entries[key].minutes += entry.minutes


# removes all lines after '------' separator in the file
def removeInactivePart(filePath):
    with open(filePath, 'r', encoding='utf-8-sig') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            if '---' in lines[i] and i > 0:
                return lines[:i - 1]
    return []


# removes extra "tags" from the lines
def removeTrailingTags(lines):
    for i in range(len(lines)):
        lines[i] = lines[i].replace(" (couldn't stop)", '')  # delete (couldn't stop) tag
        lines[i] = re.sub(r'\s[\[\(][\w, ]*last one[\w, !?\]\)]*', '', lines[i],
                          flags=re.IGNORECASE)  # remove [last one] tags
        lines[i] = lines[i].strip()  # get rid of end line chars
    return lines


# takes a string like "30' Learning Python" and converts to Entry object
def extractEntry(string):
    match = re.match(r'^((\d+)[\s\']+)?(.*)', string)
    if match.group(2) is not None:
        mins = int(match.group(2))
    else:
        mins = 60

    activity = match.group(3)
    return Entry(mins, activity)
