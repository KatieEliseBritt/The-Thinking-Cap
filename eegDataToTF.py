import csv
import tensorflow as tf 
tf.enable_eager_execution()
'''
This program takes in a csv file of EEG data output from chronoSync.py and creates a Tensorflow dataframe object from it
'''
#FThis function formats each line of CSV into features (8 tensors with numSamples number of EEG readings) and a class label for the button pressed
def _parse_csv_row(*vals):
    #The label (keypress) is the first col of the row
    class_label = tf.argmax(vals[0], axis=0)
    featureNames = []
    #Create an array of names to pair give to the features
    for i in range(1, numElectrodes):
        featureNames.append(('Electrode'+str(i)+' Samples'))
    
    #Now for each individual electrode grab the samples and put it in a tensor (E1 starts at row[2])
    electrodeTensors = []
    firstSampleOfElectrode = 2
    lastSampleOfElectrode = firstSampleOfElectrode+numSamples 
    for i in range(1, numElectrodes):
        electrodeTensors.append(tf.convert_to_tensor(vals[firstSampleOfElectrode:lastSampleOfElectrode]))
        #Now slide the window to grab the next electrode's values
        firstSampleOfElectrode = firstSampleOfElectrode+numSamples
        lastSampleOfElectrode = lastSampleOfElectrode+numSamples
    
    #For each tensor of Electrode samples, make it a dictionary with the key of the electrode name for TF
    features = dict(zip(featureNames, electrodeTensors))
    return features, class_label


#Open the CSV to extract numSamples - tensorflow needs this before
numSamples = 0
numElectrodes = 8

with open('exampleEEGData.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        numSamples = int(row[1])
        break
    csv_file.close()
#Now that we have the number of samples, its time to read in the CSV as a tensorflow dataset object. Label + 8*numSamples size
defaults = [tf.float32] * (2 + (8*numSamples))
dataset = tf.contrib.data.CsvDataset(['exampleEEGData.csv'], defaults)
dataset = dataset.map(_parse_csv_row)
print(dataset)



        


