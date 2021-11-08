from acconeer.exptool import configs, utils
from acconeer.exptool.clients import SocketClient, UARTClient, SPIClient
import os
import pandas as pd
import numpy as np
from random import randint
from datetime import datetime
from DataGathering.config import sensorconfig



def Gatherenvelopedata(runtime_length, config, Wastebin, Hash):
    run_ID = randint(500000, 599999)

    #client = UARTClient("COM16")
    #client = SocketClient("192.168.43.241") #pi 3b+
    client = SocketClient("192.168.1.195") #pi at undagrid
    updaterate = config.update_rate

    total_range = config.range_interval[1] - config.range_interval[0]


    # config.bin_count = 10

    print(config)

    session_info = client.setup_session(config)
    print("Session info:\n", session_info, "\n")


    client.start_session()
    info, data = client.get_next()
    data_length = len(data)
    emptylist = [0] * data_length
    empty_np = np.array(emptylist)
    raw_data = np.array(emptylist)
    paused = False

    time = 0
    timelist = []
    interrupt_handler = utils.ExampleInterruptHandler()
    print("Press Ctrl-C to end session\n")

    #while not interrupt_handler.got_signal:
    while time < runtime_length:
        info, data = client.get_next()

        timelist.append(time)

        raw_data = np.vstack((raw_data, data))

        print("   ---   ", round(time, 2), "   ---   ")
        time = time + (1 / updaterate)

    raw_data = np.delete(raw_data, 0, 0)

    # mean_data_df = pd.dataframe(mean_data)

    raw_data_df = pd.DataFrame(data=raw_data[0:, 0:],
                               index=[str(i + 1)
                                      for i in range(raw_data.shape[0])],
                               columns=[str(i + 1)
                                        for i in range(raw_data.shape[1])])

    raw_data_df.columns = [str(round((config.range_interval[0] + int(col_name) * (total_range / raw_data.shape[1])), 4))
                           for col_name in raw_data_df.columns]
    raw_data_df['time'] = timelist


    #    for column in raw_data_df:
    #        if column.isnumeric():
    #            #column_name = "MA_" + str(column) + "_Range_" + str(config.range_interval[0]+round((int(column)*range_interval),2))
    #            mean_data_df["Data_"+str(column)] = raw_data_df.loc[:,column].rolling(window=updaterate).mean()


    # plot_data_df = (plot_data_df - plot_data_df.min()) / (plot_data_df.max() - plot_data_df.min())




    Wastebin_bool = False
    if Wastebin is not None:
        Wastebin_bool = True
        path = r"..\output\wastebin\run_" + str(run_ID)
    else:
        path = "../output/run_" + str(run_ID)
    print(path)



    os.mkdir(path)

    if Hash is not None:
        hashfile = open(path + '/hash.txt', 'a')
        hashfile.write(str(Hash))
        hashfile.close()
    #np.savetxt(path + "/output.csv", raw_data_df, delimiter=',')
    #print("saved csv")

    raw_data_df.to_pickle(path + r"\output.pkl")

    configfile = open(path + r"\config.txt", "a")
    configfile.write(str(config))
    configfile.close()

    now = datetime.now()

    print("now =", now)

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d_%m_%Y %Hh%Mm%Ss")

    timestamp = open(path + "/" + dt_string + ".txt", "a")
    timestamp.write("  ")
    timestamp.close()

    if Wastebin_bool:
        wastebin_txt = open(path + r"\wastebin.txt", "a")
        wastebin_txt.write(Wastebin[0] + "\n" + Wastebin[1] + "\n" + Wastebin[2] + "\n" + Wastebin[3] + "\n\n" + Wastebin[4])
        wastebin_txt.close()

    print("Disconnecting...")
    client.disconnect()
    return run_ID
    # print(datalist)

def main():
    updaterate = 60

    # config.profile = config.Profile.PROFILE_3
    # config.gain = 0.2
    # config.maximize_signal_attenuation = True

    Gatherenvelopedata(20, sensorconfig["env_long_range"])

if __name__ == "__main__":
    main()