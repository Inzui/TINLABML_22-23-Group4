import pandas as pd
import os

names = ['ACCELERATION','BRAKE','STEERING','SPEED','TRACK_POSITION','ANGLE_TO_TRACK_AXIS','TRACK_EDGE_0','TRACK_EDGE_1','TRACK_EDGE_2','TRACK_EDGE_3','TRACK_EDGE_4','TRACK_EDGE_5','TRACK_EDGE_6','TRACK_EDGE_7','TRACK_EDGE_8','TRACK_EDGE_9','TRACK_EDGE_10','TRACK_EDGE_11','TRACK_EDGE_12','TRACK_EDGE_13','TRACK_EDGE_14','TRACK_EDGE_15','TRACK_EDGE_16','TRACK_EDGE_17','TRACK_EDGE_18']

# df = pd.read_csv('aalborg.csv')


# print(df['ACCELERATION'])

files = os.listdir()
files.remove('suzuka.csv')
print(files)

path = os.getcwd()
frames = []
for file in files:
    if '.csv' in file:
        
        # print(file)
        df = pd.read_csv(file)
        frames.append(df)


# df1 = pd.read_csv('aalborg.csv')
# df2 = pd.read_csv('alpine-1.csv')
# frames = [df1,df2]



finalDataFrame = pd.concat(frames).drop_duplicates().reset_index(drop=True)

print(len(finalDataFrame.index))
# finalDataFrame.drop_duplicates(inplace=True)
print(len(finalDataFrame.index))
# finalDataFrame.drop
print(len(finalDataFrame.index))
print(finalDataFrame)



finalDataFrame.to_csv('manual_combined.csv',index=False)
        



