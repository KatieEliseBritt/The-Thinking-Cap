'''
The Algorithm will be passed in the path to the file, and a list of keys the user wishes to track.
It will then capture all the keypresses and their timestamps the user cares about.
It will then search the EEG data for a keypress and capture X samples of data before the press, storing hashes of keys and the data before that press
It will then, finally, output a one hot encoded logfile with the X samples of data labeled with the key it corresponded to.

'''
import re
import os
from datetime import datetime as time
from copy import deepcopy

#Regular expressions will be used to extract character presses & timestamps from lines of the log into groups
#Grabs AB:CD:EF.GH(I) without last decimal place "I" in group 2
timeGroup1keyGroup2 = re.compile(r".* (.*:.*:.*,\d\d)\d: (.*):") 
#keysToLog will be REPLACED with sys.argv[2] when actually being run:
keysToLog = list(["'w'","'a'","'s'","'d'","'1'","'2'","'3'"])
#This is the list of hashes that will contain keylog appearances and their timestamps:
loggedKeys = list()

# When actually running code, change r'C:...' to with open(sys.argv[1], 'r') as f: \n\t contents = f.read()
with open(r'C:\Users\Gandalf\Documents\Senior Design\Internal Automation\keypresses_sample.txt') as logFile:
    for eachLine in logFile:
        match = re.match(timeGroup1keyGroup2, eachLine)
        if match:
            for eachChar in keysToLog:
                if match.group(2)==eachChar:
                    #print(match.group(1).replace(',','.') + " : " +match.group(2))
                    keyTimestampPair = dict([(match.group(1).replace(',','.'), match.group(2))])
                    loggedKeys.append(deepcopy(keyTimestampPair))
        
#Uncomment to see what keys and timestamps were captured
#for eachThing in loggedKeys:
#    print(eachThing)

#Now parse the EEG file to find the relevant timestamps. This parameter defines the total window of data around an event
samplesBeforePress = 2 #Samples of EEG data before the event
samplesBeforePressWindow = list()
#This will store the relevant data correlating the key to the EEG data (list of lists)
eegDataEncoded      = list()
logfileTimeStamp    = re.compile(r".*, (.*\d\d)\d,") #Grabs AB:CD:EF.GH(I) without last decimal place "I"
#This grabs ONLY the 8 sensor readings from a line of the EEG data file without ancillary data
eegDataStripped     = re.compile(r"\d*, ([\d\-\.]*), ([\d\-\.]*), ([\d\-\.]*), ([\d\-\.]*), ([\d\-\.]*), ([\d\-\.]*), ([\d\-\.]*), ([\d\-\.]*), (?:.*)")

with open(r'C:\Users\Gandalf\Documents\Senior Design\Internal Automation\EEG_data_sample.txt') as eegFile:
    for eachLine in eegFile:
        #Put the next line of EEG data in the window
        samplesBeforePressWindow.append(eachLine)
        #If the samples stored in the sliding window are fewer than samplesBeforePress, append and start over
        if len(samplesBeforePressWindow) < samplesBeforePress:
            continue

        #From this point on there are enough samples in the window to check if the keypress timestamp matches an EEG timepress
        match = re.match(logfileTimeStamp, eachLine)
        if match:
            #For each timestamp in the EEG (to second.XY) check to see if there is a keypress in the logfile associated with it
            for eachDict in loggedKeys:
                for timeStamp, pressedKey in eachDict.items():
                    #If the timestamp of the EEG data matches a timestamp in the keylog data - save all the EEG data in the window with the key it matches
                    if timeStamp == match.group(1):
                        #Now samplesBeforePressWindow has the key that data corresponds to at the end of the list to be encoded by the last section
                        samplesBeforePressWindow.append(pressedKey)
                        eegDataEncoded.append(deepcopy(samplesBeforePressWindow))
                        #Also remove the label from the last index of the window
                        samplesBeforePressWindow.pop()

        #Regardless, now it is time to remove the oldest (first) index and add the newest one at the beginning of the loop
        samplesBeforePressWindow.pop(0)

#Create a uniquely named (with datetime) file in the encodedEEG folder to paste the encoded data
dt = time.now()
outputFilename = dt.strftime("%m-%d-%Y,%H-%M-%S-%f")
encodedFile = open(r"C:\Users\Gandalf\Documents\Senior Design\Internal Automation\encodedEEG\\"+outputFilename,"w+")

#Now that the uniquely named file has been created, write out one-hot encoded data to it 
for eachList in eegDataEncoded:
    #Each list has elements that are lines of EEG data, or a label at the last index
    label = eachList.pop()
    for eachElement in eachList:
        data = re.match(eegDataStripped, eachElement)
        if data:
            iterableData = data.groups()
            for eachDatum in iterableData:
                encodedFile.write(eachDatum + ', ')
            #Now write the label and a newline and move to the next list of data
    encodedFile.write(label + '\n')

#Now the uniquely named file has samplesBeforePress number of EEG samples and a key-press label  
encodedFile.close()
