import sys

##
## Return an array containing the data received 
## from a sample
##
def file_to_array(csv_file):
    array = []
    
    tmpF = open(csv_file, 'r')
    for line in tmpF:
        line = line.replace('\n','').split(" ")

        array.append(float(line[0]))

    return array


##
## Verify if the movement is valid
##
def emg_isValid(data_vec):
    count = 0
    
    # get the percentage of each range of data
    for entry in data_vec:
        if (abs(entry) > 0.3) and (abs(entry) < 0.8):
            count += 1
    
    # check if the movement is valid
    if (float(count) / len(data_vec) > 0.05):
        print "valid"
    else:
        print "invalid"

def acc_isValid(data_vecx, data_vecy):
    countX = 0
    countY = 0

    valids = [0,0]

    for entry in data_vecx:
        if(float(entry) < 0.0):
            countX += 1
    if (float(countX) / len(data_vecx)) > 0.85:
        valids[0] = 1


    for entry in data_vecy:
        if( float(entry) < 0.0):
            countY += 1
    if (float(countY) / len(data_vecy)) < 0.65:
        valids[1] = 1


    print valids
    if sum(valids) == 2:
        print "valid"
    else:
        print "invalid"


## get the wave
#samples = sys.argv[1]

## generate the array containing the data
## to be analyzed
#array_data = file_to_array(samples)

## Verify if the movement is correct
#isValid(array_data)
