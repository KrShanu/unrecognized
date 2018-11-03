import csv
import sys

#Question: What output does the model give? 
#frame_index = 99 #strIntToTimestamp(sys.argv[2])


#eg: index == 99, FPS == 100, nearestSecond => 0th
#eg:index == 100, FPS == 100, nearestSecond => 1st
def indexToNearestSecond(index, FPS):
    if isinstance(index, int) and isinstance(FPS, int):
        return index // FPS #integer quotient

#input: second, frame index
#outputs [SECOND, VALUE] to path as csv row
def outputResultToCSV(second, value, path):
    with open(path, mode = 'a') as my_csv:
            my_csv_writer = csv.writer(my_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            my_csv_writer.writerow([second, value])

'''
#SOME FUNCTIONS TO FORMAT INPUT
def strBoolToBinary(str_bool):
    if isinstance(str_bool, str):
        if str_bool == "True":
            return 1
        else:
            return 0
    elif isinstance(str_bool, int):
        return str_bool

#what format will input timestamp be?
def strIntToTimestamp(str_input):
    if isinstance(str_input, str):
        return str_input
    elif isinstance(str_input, int):
        return str_input
'''
