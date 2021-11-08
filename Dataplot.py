import pandas as pd
import plotly.express as px
# from DataGatheringEnvelope import Gatherenvelopedata
# from config import sensorconfig
#from NeuralNetworkULD import trainmodel
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import filecmp

def checkconfig(run_ID_list):

    originalpath = "./output/run_" + str(run_ID_list[0]) + "/config.txt"
    for run_ID in run_ID_list:
        path = "./output/run_" + str(run_ID)
        output = filecmp.cmp(path + "/config.txt", originalpath)
        if output != True:
            print("config of:", run_ID, "is not equal to:", run_ID_list[0])
            exit()
    return

def retrievewastebindataframe(run_ID_list):
    #checkconfig(run_ID_list)
    dataframe_list = []
    if isinstance(run_ID_list, list) is not True:
        run_ID_list = [run_ID_list]

    for run_ID in run_ID_list:
        path = r"..\output\wastebin\run_" + str(run_ID)
        raw_data_df = pd.read_pickle(path + "\output.pkl")
        if 'time' in raw_data_df.columns.tolist():
            raw_data_df = raw_data_df.set_index("time")
        dataframe_list.append(raw_data_df)

    return dataframe_list


def retrievedataframe(run_ID_list):
    #checkconfig(run_ID_list)
    dataframe_list = []
    if isinstance(run_ID_list, list) is not True:
        run_ID_list = [run_ID_list]

    for run_ID in run_ID_list:
        path = "../output/run_" + str(run_ID)
        raw_data_df = pd.read_pickle(path + "/output.pkl")
        if 'time' in raw_data_df.columns.tolist():
            raw_data_df = raw_data_df.set_index("time")
        dataframe_list.append(raw_data_df)


    return dataframe_list

def retrievefulldata(run_ID_list_list, no_ulds):
    output = []
    fulldataframes_list = []
    for i in range(len(run_ID_list_list[0])):
        listwithrunID = [item[i] for item in run_ID_list_list]
        listwithrunID.append(no_ulds[i])
        output.append(listwithrunID)

        print("break")

    for run_ID_list in output:
        dataframes = retrievedataframe(run_ID_list[:-1])
        print("break2")
        fulldataframe = pd.concat(dataframes, axis=1)
        fulldataframe["0ULD"] = 1 if run_ID_list[-1:][0] == 0 else 0
        fulldataframe["1ULD"] = 1 if run_ID_list[-1:][0] == 1 else 0
        fulldataframe["2ULD"] = 1 if run_ID_list[-1:][0] == 2 else 0
        fulldataframe = fulldataframe.mean(axis=0)
        fulldataframes_list.append(fulldataframe)


    return fulldataframes_list



def concatenatedata(df_list):
    previousmaxvalue = 0
    for dataframe in df_list:


        maxvalue = previousmaxvalue - round(dataframe.index.min(), 0)
        dataframe.index += (maxvalue+1)

        previousmaxvalue = round(dataframe.index.max(), 0)


    final_df = pd.concat(df_list)
    print("breakpoint")
    return final_df

def meandata(df_list, no_bins):

    #meandata = pd.dataframe()
    meandata_list = []
    for dataframe in df_list:
        binneddata = bindata(dataframe, no_bins)
        meandata_list.append(binneddata.mean())

        #print(dataframe)
    final_df = pd.concat(meandata_list, axis=1)


    return final_df.T



def bindata(dataframe, no_bins):
    total_columns = dataframe.shape[1]-1
    #print("total columns:" + str(total_columns))


    binned_df = pd.DataFrame(index=dataframe.index)



    #binned_df["time"] = dataframe.iloc[:,-1:]

    for i in range(no_bins):
        #print(i)

        binname = "bin_[" + str(round(float(dataframe.columns[int(round((total_columns/no_bins)*i, 0))]),2)) + " " + str(round(float(dataframe.columns[int(round((total_columns/no_bins)*(i+1), 0)-1)]),2)) + "]"

        #print(binname)

        binned_df[binname] = dataframe.iloc[:, int(round((total_columns / no_bins) * i, 0)):int(
            round((total_columns / no_bins) * (i + 1), 0))].mean(axis=1).tolist()

    #print("\n")
    #print(binned_df.shape)

    return binned_df

def LinePlot(raw_data_df):

    fig = px.line(raw_data_df, x=raw_data_df.index, y=raw_data_df.columns, title="Data")
    try:
        fig.write_html(r"../output/figures/Line_plot.html", auto_open=True, include_plotlyjs="cdn")
    except:
        fig.write_html(r"./output/figures/Line_plot.html", auto_open=True, include_plotlyjs="cdn")
    print("printed!")

def Spectogramplot(raw_data_df, x_list):

    #binneddata = bindata(raw_data_df, no_bins)
    if x_list != None:
        listofzeros = list(range(len(x_list)))
        x_values = [listofzeros, x_list]
    else:
        x_values = raw_data_df.index



    trace = [go.Heatmap(
        x=x_values,
        y=raw_data_df.columns,
        #z=(raw_data_df.T),
        z=np.log10(raw_data_df.T),
        colorscale='Jet'
    )]
    layout = go.Layout(
        title='Spectrogram',
        yaxis=dict(title='Amplitude'),  # x-axis label
        xaxis=dict(title='Time')
    )
    fig = go.Figure(data=trace, layout=layout)
    try:
        fig.write_html(r"../output/figures/Spectogram_plot.html", auto_open=True, include_plotlyjs="cdn")
    except:
        fig.write_html(r"./output/figures/Spectogram_plot.html", auto_open=True, include_plotlyjs="cdn")

def subplotspectogramfigure(fig):

    layout = go.Layout(
        title='Spectrogram',
        yaxis=dict(title='Amplitude'),  # x-axis label
        xaxis=dict(title='Experiment')
    )
    fig.update_layout(layout)
    try:
        fig.write_html(r"../output/figures/Spectogram_subplot_ULDTest.html", auto_open=True, include_plotlyjs="cdn")
    except:
        fig.write_html(r"./output/figures/Spectogram_subplot_ULDTest.html", auto_open=True, include_plotlyjs="cdn")


def Spectogramsubplot(raw_data_df_list):
    fig = make_subplots(rows=3, cols=1)
    i = 1
    for raw_data_df in raw_data_df_list:
        fig.append_trace(go.Heatmap(
            x=raw_data_df.index,
            y=raw_data_df.columns,
            #z = (raw_data_df.T),
            z=np.log10(raw_data_df.T),
            colorscale='Jet'
        ), row=i, col=1)
        i += 1
        print(i)

    subplotspectogramfigure(fig)



def WastebinSpectogramsubplot(df_list,x_list, titles):

    if titles != None:
        fig = make_subplots(rows=len(df_list), cols=1, subplot_titles=titles)
    else:
        fig = make_subplots(rows=len(df_list), cols=1)
    i = 1
    listofzeros = list(range(len(x_list)))
    x_list = [listofzeros,x_list]

    for raw_data_df in df_list:
        fig.append_trace(go.Heatmap(
            x=x_list,
            y=raw_data_df.columns,
            z=np.log10(raw_data_df.T),
            colorscale='Jet'
        ), row=i, col=1)
        i += 1
        print(i)

    subplotspectogramfigure(fig)
    print("WastebinSpectogramsubplot")


def Gatherlensdata():
    x_list = []
    run_bool = True
    runtime_length = 1
    if run_bool:
        run_ID1 = []
        run_ID2 = []
        run_ID3 = []
        cont_bool = True
        while cont_bool == True:
            inputstring = input("next run?")
            if inputstring != 'n':
                x_list.append(inputstring)

                print("start gathering data...")
                if input("no lens...") != 'n':
                    print("Running no lens!")
                    run_ID1.append(Gatherenvelopedata(runtime_length, sensorconfig["env_short_range"], None, None))
                if input("double cone lens...") != 'n':
                    run_ID2.append(Gatherenvelopedata(runtime_length, sensorconfig["env_short_range"], None, None))
                if input("diamond lens...") != 'n':
                    run_ID3.append(Gatherenvelopedata(runtime_length, sensorconfig["env_short_range"], None, None))
            else:
                cont_bool = False
    titles = ['no lens', 'double cone', 'diamond']

    run_IDs = [run_ID1, run_ID2, run_ID3]
    return (run_IDs, x_list, titles)

def main():
    runtime_length = 1
    run_bool = True
    #run_ID = [305386, 395725, 358044, 348056]
    #run_ID = [356320, 308816] #0 and 1
    #run_ID = [337743, 384909] #0 and 0
    #run_ID = [388573, 399008, 326988, 310069]

    # run_ID1= [321239, 364883, 361893, 354844] #short 0012
    # run_ID2 = [342064, 326089, 353782, 310419] #mid 0012
    # run_ID3 = [389070, 366924, 385938, 399227] #long 0012
    # titles = ['Short range', 'Mid range', 'Long range']
    # x_list = ['0 ULD', '0 ULD', '1 ULD', '2 ULDs']
    #run_ID = [341075, 327596, 327095, 301720] #short 0012
    #run_ID = [395464, 384608, 398438, 328505] #mid 0012
    #run_ID = [337743, 384909, 377738, 342806] #long 0012
    #run_ID = [369169]
    #run_ID = [399008, 388573, 326988, 310069] #short 2011
    #run_ID = [323425, 387207, 390230, 320314] #mid 0012

    #run_ID = [321239, 361893, 364883, 341075, 363688, 327596] #short 0101010
    #run_ID = [342064, 353782, 395464, 317338, 384608, 398438, 387207] #mid 0101010
    
    #run_ID = [389070, 399227, 337743, 342806, 395725] #long 02020

    # run_ID1 = [321239, 361893, 354844, 363688, 341075, 327095, 301720, 317730, 388573]  # 012101210 short
    # run_ID2 = [326089, 353782, 310419, 317338, 395464, 398438, 328505, 332745, 387207] #012101210 mid
    # run_ID3 = [389070, 385938, 399227, 381630, 337743, 377738, 342806, 384072, 395725]  # 012101210 long
    # titles = ['Long range', 'Mid range', 'Short range']
    # x_list = ['0 ULD', '1 ULD', '2 ULDs', '1 ULD','0 ULD','1 ULD','2 ULDs','1 ULD','0 ULD']

    run_ID1 = [309993, 311870, 340846]
    titles = ['full', 'full', 'full']
    x_list = ['xaxis']
    #run_ID1 = [327596, 328323, 353850, 388573]  #0330 short
    #run_ID2 = [384608, 397421, 357573, 387207]  #0330 mid
    #run_ID3 = [384909, 302510, 358089, 395725]  #0330 long

    #run_ID1 = [388573, 326988, 310069, 327596]  #0110 short
    #run_ID2 = [387207, 390230, 320314, 384608]  #0110 mid
    #run_ID3 = [395725, 358044, 348056, 384909]  #0110 Long

    #run_ID2 = [389070, 385938, 381630, 337743]

    #order: 1(next to the edge) 1(over the edge) 2 1(otherside, over the edge.)
    #without lens: [473167, 458661, 449739, 471003, 404374, 401151, 409835] [432612, 420360, 487437, 494859, 430686, 484959, 403169] [431234, 468745, 402244, 434984, 452319, 453680, 448583]
    #with hyperbolic lens: [496749, 423062, 412505, 465650, 493725, 447126, 470909] [420942, 481742, 422777, 488176, 470945, 490160, 492966] [458948, 410121, 493157, 444519, 411860, 480808, 497565]
    # with cone lens: [592556, 517350, 538461, 599594, 544161, 551431, 555619] [533265, 517011, 522983, 599916, 579379, 525387, 517872] [569913, 505949, 513109, 559793, 583951, 574280, 561538]

    # run_ID1 = [473167, 458661, 449739, 471003, 404374, 401151, 409835]
    # run_ID2 = [432612, 420360, 487437, 494859, 430686, 484959, 403169]
    # run_ID3 = [431234, 468745, 402244, 434984, 452319, 453680, 448583]

    #run_ID1 = [592556, 517350, 538461, 599594, 544161, 551431, 555619]
    #run_ID2 = [533265, 517011, 522983, 599916, 579379, 525387, 517872]
    #run_ID3 = [569913, 505949, 513109, 559793, 583951, 574280, 561538]

    # run_ID1 = [496749, 423062, 412505, 465650, 493725, 447126, 470909]
    # run_ID2 = [420942, 481742, 422777, 488176, 470945, 490160, 492966]
    # run_ID3 = [458948, 410121, 493157, 444519, 411860, 480808, 497565]


    #run_ID4 = [371462]

    #no_ULDs = [0,1,2,1,0,1,2,1,0,0,0]
    run_bool = False
    cont_bool = True
    # run_ID1 = []
    # run_ID2 = []
    # run_ID3 = []
    # x_list = []
    if run_bool == True:
        cont_bool = True
        while cont_bool == True:
            inputstring = input("next run?")
            if inputstring != 'n':
                x_list.append(inputstring)
                #(run_IDs, x_list, titles) = Gatherlensdata()
                #input("without lens")
                run_ID1.append(Gatherenvelopedata(runtime_length, sensorconfig["env_short_range"], None, None))
                #input("with lens")
                run_ID2.append(Gatherenvelopedata(runtime_length, sensorconfig["env_long_range"], None, None))
                run_ID3.append(Gatherenvelopedata(runtime_length, sensorconfig["env_xlong_range"], None, None))
            else:
                cont_bool = False
    #run_IDs = [[557120, 521102, 583003, 567222, 541722, 568541],[514853, 510796, 595747, 599712, 537608, 534162],[529330, 551292, 576947, 561087, 579272, 563251]] #distance lens measurement
    # x_list = ['50cm', '40cm', '30cm', '20cm', '10cm', '6cm']
    #run_IDs = [[588902, 598529, 506557, 544008], [517956, 522920, 509307, 583078], [516129, 501009, 592204, 572788]]
    #x_list = ['40cm', '30cm', '20cm', '10cm']

    #x_list = [[558160, 584689, 558444, 512457, 569855], [581706, 537512, 572963, 565807, 526589],
     #[590102, 505835, 562364, 561483, 574873]]

    #titles = ['no lens', 'double cone', 'diamond']

    run_IDs = [run_ID1]
    #run_IDs = [[544123, 504311, 578663, 576426, 581896], [574269, 597489, 557681, 539858, 535543]]
    #run_IDs=[[549802, 536834, 557157, 546284, 505033],[565132, 583099, 582903, 546677, 502962]]
    #x_list = ['no ULD', '1 ULD left', '2 ULD', '1 ULD right', 'no ULD']
    #titles = ['no lens', 'diamond lens']
    # titles = ['Short range', 'Mid range', 'Long range']
    no_bins = 60
    df_list = []

    for run_ID in run_IDs:
        df_list = retrievedataframe(run_ID)

        # meaneddata = meandata(df, no_bins)

    df = concatenatedata(df_list)
    # meaneddata = bindata(df, 10)
    #x_list = ['1 ULD','2 ULD far', '2 ULD close']
    #df_list.append(df_list[0].subtract(df_list[1]))
    # WastebinSpectogramsubplot(df_list, x_list, titles)
    #Spectogramplot(df_list[1], x_list)
    LinePlot(df)



    print(run_IDs)
    print(x_list)
    #LinePlot(df_list[0])
    # LinePlot(df_list[0])
    #average = [bindata(dataframe, no_bins).mean(axis=0) for dataframe in df]
    #summation = [sum(number) for number in average]
    #comparedtofirst = [sum(abs(average[0]-number)) for number in average]
    #print(average)
    #print("bin 1.63 1.7 = ", [abs(average[0]['bin_[1.63 1.7]'] - number['bin_[1.63 1.7]']) for number in average]) #get difference in one bin
    #print("bin 1.7 1.77 = ", [abs(average[0]['bin_[1.7 1.77]'] - number['bin_[1.7 1.77]']) for number in average])
    #print(comparedtofirst)




    #Spectogramplot(run_ID, no_bins)


if __name__ == "__main__":
    main()