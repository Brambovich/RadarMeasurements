import pandas as pd
from DataGathering.DataGatheringEnvelope import Gatherenvelopedata
from DataGathering.config import sensorconfig
from DataGathering.Dataplot import retrievewastebindataframe, Spectogramsubplot, meandata, Spectogramplot, WastebinSpectogramsubplot
import os
import random
from datetime import datetime

def DataplotWastebin(run_ID_list, no_bins):
    dataoption = int(input("Which plot? 1:short, 2:mid, 3:long, 4:subplot"))
    df_list = []
    if dataoption == 4:
        for run_ID in run_ID_list:
            df = retrievewastebindataframe([run_ID])
            meaneddata = meandata(df, no_bins)
            df_list.append(meaneddata)
        Spectogramsubplot(df_list)
    else:
        df = retrievewastebindataframe(run_ID_list[dataoption-1])
        meaneddata = meandata(df, no_bins*3)
        Spectogramplot(meaneddata)

def GatherWastebinData():
    hash_bits = random.getrandbits(128)
    runtime_length = 1
    fillgrade = input("What is the fillgrade? (1-5)")
    wastetype = input("what is the Wastetype (1: Paper, 2: Plastic, 3: Other, 4: Organic)")
    Binsize = input("What is the size of the bin? (in cm)")
    Wastedepth = input("What is the depth to the trash? in cm)")
    notes = input("Further notes?")
    run_ID1 = Gatherenvelopedata(runtime_length, sensorconfig["env_short_range"], [fillgrade, wastetype, Binsize, Wastedepth, notes], hash_bits)
    run_ID2 = Gatherenvelopedata(runtime_length, sensorconfig["env_mid_range"], [fillgrade, wastetype, Binsize, Wastedepth, notes], hash_bits)
    run_ID3 = Gatherenvelopedata(runtime_length, sensorconfig["env_wastebin_config"], [fillgrade, wastetype, Binsize, Wastedepth, notes], hash_bits)


    run_ID_list = [run_ID1, run_ID2, run_ID3]

    return run_ID_list

def convertodatetime(time_string):
    datetime_object = datetime.strptime(time_string[:-4], "%d_%m_%Y %Hh%Mm%Ss")
    return datetime_object

def checkrange(directory, run_ID):
    path = directory + "run_" + run_ID + "/config.txt"
    #print("CHECKRANGE:", path)
    config_txt = open(path, 'r')
    profile = config_txt.readlines()[4][-2:-1]
    #print("profile is: ", profile)
    if profile == '1':
        return 0
    elif profile == '2':
        return 1
    else:
        return 2

def RecoverRangeData(directory,given_subdir,time):
    #print("RecoverRangeData")
    config = open(given_subdir + '/config.txt', 'r')
    run_ID_list = []
    originaltime = convertodatetime(time)

    for subdir, dirs, files in os.walk(directory):
        if len(files) == 6:

            difference = (convertodatetime(files[0]) - originaltime).total_seconds()
            #print(convertodatetime(files[0]), originaltime, difference)
            if abs(difference) < 10:
                #print(subdir)
                run_ID_list.append(subdir[-6:])


    print("RecoverRangeData:", run_ID_list)
    config.close()
    return run_ID_list

def filterWastebinData(wastebin_type):
    short_ID1 = []
    mid_ID2 = []
    long_ID3 = []
    x1 = []
    x2 = []
    fillgrade_list = []
    wastedistance_list = []
    directory = r'../output/wastebin/'
    for subdir, dirs, files in os.walk(directory):
        #print(subdir, dirs, files)
        if len(files) == 6:
            if subdir[-6:] not in (short_ID1 + mid_ID2 + long_ID3):
                print(subdir[-6:])
                wastebin_txt = open(subdir+ '/wastebin.txt', 'r')
                wastebin_lines = wastebin_txt.readlines()

                if int(wastebin_lines[1][:-1]) in wastebin_type:
                    print("searchhhhh")
                    fillgrade_list.append(wastebin_lines[0][:-1])
                    wastebin_txt.readline()
                    wastedistance_list.append(wastebin_lines[3][:-1])
                    run_ID_list = RecoverRangeData(directory,subdir,files[0])
                    #print(run_ID_list)
                    for run_ID in run_ID_list:
                        print("PROFILE IS:", checkrange(directory, run_ID))
                        if checkrange(directory, run_ID) == 2:
                            short_ID1.append(run_ID)
                        elif checkrange(directory, run_ID) == 1:
                            mid_ID2.append(run_ID)
                        else:
                            long_ID3.append(run_ID)

            wastebin_txt.close()

        #for file in os.listdir(directory+dirs):
        #    print(file)
    run_ID_array = [short_ID1, mid_ID2, long_ID3]
    print(run_ID_array)

    return (run_ID_array, fillgrade_list, wastedistance_list)



def main():
    #run_ID_list = [553443, 539145, 524041]
    #run_ID_list = GatherWastebinData()
    no_bins = 100
    df_list = []
    titles = ['long range', 'mid range', 'short range']
    #DataplotWastebin(run_ID_list, no_bins)
    (run_ID_list, fillgrade_list, wastedistance_list) = filterWastebinData([1,2,3])
    #print("fillgrade list:\n" ,fillgrade_list)
    # input("what is the Wastetype (1: Paper, 2: Plastic, 3: Other, 4: Organic)")
    for run_ID in run_ID_list:
        df = retrievewastebindataframe(run_ID)
        meaneddata = meandata(df, no_bins)
        df_list.append(meaneddata)


    #meaneddata = meandata(df, no_bins)
    #df_list.append(meaneddata)
    xlist = ["fill:" + x + " - " +  y + "cm" for x, y in zip(fillgrade_list, wastedistance_list)]
    #Spectogramplot(df_list[1], xlist)
    # WastebinSpectogramsubplot(df_list, xlist, titles)
    # Spectogramplot(df_list[1].ge(500)*1, xlist)
    Spectogramplot(df_list[1], xlist)
    print([int(x) for x in fillgrade_list])


    #print(list(round((df_list[1].sum(axis=1)),0)), "\n")
    #print([str(x) + ':'+ str(y) for x,y in zip([int(x[:-1]) for x in fillgrade_list],list(round((df_list[1].sum(axis=1)),0)) )])


if __name__ == "__main__":
    main()
