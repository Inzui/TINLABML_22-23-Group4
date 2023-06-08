import pandas as pd


# df = pd.read_csv('combined_data.csv')
df = pd.read_csv('manual_combined.csv')
print(startLen := df.shape[0])
brakeCount = 0
brakeList = []
accelList = []
accelCount = 0
for index, row in df.iterrows():
    # print(row['BRAKE'])

    if row['BRAKE'] == 1:
        brakeCount +=1
        brakeList.append(index)
    
    if row['ACCELERATION'] == 0:
        accelCount +=1
        accelList.append(index)

    if row['ACCELERATION'] == 1: 

        # print(len(accelList))
        
        if 0 < brakeCount <= 3:
            for index in brakeList:
                df.drop(index=index, inplace=True)   

        # try:
        #     if 0 < accelCount <= 2:
        #         for index in brakeList:
        #             df.drop(index=index, inplace=True)
        #         # print(len(brakeList))
        # except KeyError:
        #     pass
        

        brakeCount = 0
        brakeList = []
        accelCount = 0
        accelList = []
print(startLen - df.shape[0])

# print(brakeCount)   

df.to_csv('combined_data.csv',index=False)
