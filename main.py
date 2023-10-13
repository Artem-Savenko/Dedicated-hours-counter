import os
import sys
import code

path = sys.argv[1]
activity = sys.argv[2]
entries = dict()

for dirPath, dirs, files in os.walk(path):
    for file in files:
        txtFileName = os.path.join(dirPath, file)
        lines = code.removeInactivePart(txtFileName)
        lines = code.removeTrailingTags(lines)
        code.addEntries(entries, lines)

code.printAllEntries(entries)
