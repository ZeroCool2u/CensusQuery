# 22c16 (CS1) Project 1: Baby Names
# Theo Linnemann
# 22C:016:A05
# Based on code provided by Professor Alberto Maria Segre and
# code provided by Sriram Pemmaraju
# Developed using JetBrains excellent and generous educational PyCharm IDE

import csv
import matplotlib.pyplot as plt


def readNames(filename='names.csv'):
    '''Reads in a file consisting of one entry per line; returns list of lists containing name data.'''
    # Open the names_tiny.csv file for read.
    infile = open(filename, 'r')

    dataFile = csv.reader(infile)

    # Read in the file and split by whitespace (includes \n).
    namelist = [[int(year), name, gender, int(count)] for year, name, gender, count in dataFile]

    # Cleaning up.
    infile.close()

    return (namelist)


def nameIndex(names):
    '''Produces a dictionary that uses the baby name as a key, with each value consisting
   consisting of a list of tuples (year,male,female). Tuples within each name are sorted by
   birth year.'''

    # Creates a dict called babyNames with var name as the key and instantiates a empty list.
    babyNames = {name: [] for year, name, gender, count in names}

    # for loop going through the entire list and assigning a variable name to each value in the list of lists.
    # (Naming each column.)
    for year, name, gender, count in names:
        # Assumption for base case, as most names will not be androgenous.
        androgenous = False

        for yearTuple in range(len(babyNames[name])):

            if babyNames[name][yearTuple][0] == year:
                androgenous = True
                a, b, c = babyNames[name][yearTuple]

                if gender == 'M':
                    babyNames[name][yearTuple] = year, count, c

                else:
                    babyNames[name][yearTuple] = year, b, count

        if androgenous == False:  # Androgenous comparison for the sketchy names.

            # if the gender is Male, then add to the male column. Male column is the middle, female is last.
            if gender == 'M':
                nameEntry = year, count, 0

            else:
                # else, gender is female and last column is modified, because female coulmn is last.
                nameEntry = year, 0, count
            babyNames[name].append(nameEntry)

    # for loops used for sorting
    for name in babyNames:
        babyNames[name].sort()

    return babyNames


def yearIndex(names):
    '''Produces a dictionary that uses the year as the key and generates a second dictionary, embedded, as
  the value. The embedded dictionary uses name as the key and has a tuple (male, female) as its value.'''
    yearDictionary = {}
    for year, name, gender, count in names:
        if year not in yearDictionary:
            yearDictionary[year] = {}

            if gender == 'M':
                yearDictionary[year][name] = (count, 0)  # Places value in the Male position.

            else:
                yearDictionary[year][name] = (0, count)  # Places value in the Female position.

        else:

            if name not in yearDictionary[year]:
                if gender == 'M':
                    yearDictionary[year][name] = (count, 0)  # Places value in the Male position.
                else:
                    yearDictionary[year][name] = (0, count)  # Places value in the Female position.
            else:
                a, b = yearDictionary[year][name]

                if gender == 'M':
                    yearDictionary[year][name] = count, b  # Places value in the Male position.
                else:
                    yearDictionary[year][name] = a, count  # Places value in the Male position.

    return yearDictionary


def getBirthsByName(name, gender=None, start=None, end=None, interval=None, yearDict=yearIndex(readNames())):
    '''1st access function'''
    # names = readNames()
    # yearDict = yearIndex(names)

    if interval == None:
        interval = 1

    else:
        assert start != None and end != None  # Please provide a value for both start and end.

    if end != None:
        assert start != None  # When specifying start, you must also explicitly specify end.

    else:
        end = max(yearDict)

    if start == None:
        start = min(yearDict)

    totalNumberOfBirths = []  # Init empty list

    if gender == 'M':  # Case for Males
        for y in range(start, end + 1, interval):
            totalNumberOfBirths.append((y, yearDict[y][name][0]))
        return totalNumberOfBirths

    elif gender == 'F':  # Case for Females
        for y in range(start, end + 1, interval):
            totalNumberOfBirths.append((y, yearDict[y][name][1]))
        return totalNumberOfBirths

    else:  # Base case for retrieving full data
        for y in range(start, end + 1, interval):
            totalNumberOfBirths.append((y, sum(yearDict[y][name])))
        return totalNumberOfBirths


def getNamesByYear(yearIndex, N=None, pattern=None, gender=None, start=None, end=None, interval=None):
    '''2nd Access Function, returns dictionary of total number of births. Primary determining factor is gender for process flow.'''

    if interval == None:
        interval = 1

    else:
        assert start != None and end != None  # Please provide a value for both start and end.

    if pattern == None:
        pattern = ''

    if end != None:
        assert start != None  # When specifying start, you must also explicitly specify end.

    else:
        end = max(yearIndex)

    if start == None:
        start = min(yearIndex)

    totalNumberOfBirths = {}

    if gender == 'M':
        for y in range(start, end + 1, interval):
            for name in yearIndex[y]:
                if pattern in name.lower():
                    try:
                        totalNumberOfBirths[name] += yearIndex[y][name][0]
                    except:
                        totalNumberOfBirths[name] = yearIndex[y][name][0]
        return sorted(totalNumberOfBirths.items(), key=lambda tuple0: tuple0[1])[::-1][
               :N]

    elif gender == 'F':
        for y in range(start, end + 1, interval):
            for name in yearIndex[y]:
                if pattern in name.lower():
                    try:
                        totalNumberOfBirths[name] += yearIndex[y][name][1]
                    except:
                        totalNumberOfBirths[name] = yearIndex[y][name][1]
        return sorted(totalNumberOfBirths.items(), key=lambda tuple0: tuple0[1])[::-1][
               :N]

    else:
        for y in range(start, end + 1, interval):
            for name in yearIndex[y]:
                if pattern in name.lower():
                    try:
                        totalNumberOfBirths[name] += sum(yearIndex[y][name])
                    except:
                        totalNumberOfBirths[name] = sum(yearIndex[y][name])
        return sorted(totalNumberOfBirths.items(), key=lambda tuple0: tuple0[1])[::-1][
               :N]


def lineGraph(birthsByName, name=""):  # Linegraph generator
    """Plotting functions used to create line graphs."""
    plt.title('Births By Year For Input Name')
    plt.xlabel('Year')
    plt.ylabel('Births')
    plt.plot([y for (y, v) in birthsByName], [v for (y, v) in birthsByName], 'r-', label=name)
    plt.legend(loc=2)
    plt.show()


def barGraph(namesByYear):  # Bargraph generator
    """Plotting function used to create bar graphs."""
    plt.title('Births By Name For Input Year')
    plt.xlabel('Births')
    plt.yticks(range(len(namesByYear), 0, -1), [n for (n, t) in namesByYear])
    plt.barh(range(len(namesByYear), 0, -1), [t for (n, t) in namesByYear])
    plt.show()


def names(infile='names.csv'):
    """User interaction function. Uses commands defined in list userInput."""
    # Next three lines create usable variables from input data for use within the names() function.
    formattedData = readNames(filename=infile)
    nameStructure = nameIndex(formattedData)
    yearStructure = yearIndex(formattedData)

    cmd = ''  # Init

    queue = []  # Commands flow through and are processed here.

    while (cmd != 'x'):

        userInput = input("Please enter input: ")
        userInput = userInput.split()

        for i in range(6):
            userInput.append(None)

        if userInput[0] not in ["q", "p", "c", "b", "r", "s", "x"]:
            return "I'm sorry Dave, I'm afraid I can't do that."  # Don't forget your helmet when you exit the airlock.
        else:

            cmd = userInput[0]

            if cmd == 'q':  # Query command
                for i in range(2, len(userInput[2:])):
                    if userInput[i] == None:
                        break
                    if userInput[i] not in ['m', 'f']:
                        userInput[i] = int(userInput[i])
                    else:
                        userInput[i] = userInput[i].upper()
                if not ('M' in userInput or 'F' in userInput):
                    userInput.insert(2, None)
                print(
                    userInput)  # Optional: Prints the full commands inputed by user as determined by the positional logic for debug purposes.
                print(getBirthsByName(userInput[1], userInput[2], userInput[3], userInput[4], userInput[5],
                                      yearDict=yearStructure))

            elif cmd == 'p':  # Plot command (Copy and pasted Bargraph command, attempting to modify for use.)
                getBirthsByName(userInput[1])
                for i in range(3, len(userInput[3:])):
                    if userInput[i] == None:
                        break
                    if userInput[i] not in ['m', 'f']:
                        userInput[i] = int(userInput[i])
                    else:
                        userInput[i] = userInput[i].upper()
                if not ('M' in userInput or 'F' in userInput):
                    userInput.insert(3, None)
                queue.append(getNamesByYear(yearStructure, int(userInput[1]), userInput[2], userInput[3], userInput[4],
                                            userInput[5]))
                continue


            elif cmd == 'c':  # Count command
                for i in range(3, len(userInput[3:])):
                    if userInput[i] == None:
                        break
                    if userInput[i] not in ['m', 'f']:
                        userInput[i] = int(userInput[i])
                    else:
                        userInput[i] = userInput[i].upper()
                if not ('M' in userInput or 'F' in userInput):
                    userInput.insert(1, None)
                print(getNamesByYear(yearStructure, int(userInput[1]), userInput[2], userInput[3], userInput[4],
                                     userInput[5]))

            elif cmd == 'b':  # Bargraph command
                for i in range(3, len(userInput[3:])):
                    if userInput[i] == None:
                        break
                    if userInput[i] not in ['m', 'f']:
                        userInput[i] = int(userInput[i])
                    else:
                        userInput[i] = userInput[i].upper()
                if not ('M' in userInput or 'F' in userInput):
                    userInput.insert(3, None)
                queue.append(getNamesByYear(yearStructure, int(userInput[1]), userInput[2], userInput[3], userInput[4],
                                            userInput[5]))
                continue

            elif cmd == 'r':  # Clears the command queue.
                print(queue)
                queue = []
                continue

            elif cmd == 's':  # Shows the plot.
                plt.title("Runtime Graph")
                plt.show()
                plt.clf()
                continue

            elif cmd == 'x':  # Exit command
                return


# Debug code only after this line.
'''
d = getBirthsByName("Michael")
f = lineGraph(d)
a = readNames()
b = nameIndex(a)
c = yearIndex(a)
print("starting getNamesByYear")
e = getNamesByYear(c,N=10)
g = barGraph(e)
'''
