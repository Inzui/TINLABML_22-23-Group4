import json
import csv
import os

# Open the log file for reading
with open(os.path.join(__file__, "../", "Race_Log.log"), "r") as log_file:

    # Open the CSV file for writing
    with open(os.path.join(__file__, "../", "Output.csv"), "w+", newline="") as csv_file:
        writer = csv.writer(csv_file)

        # Write the header row to the CSV file
        header = ["SPEED","TRACK_POSITION","ANGLE_TO_TRACK_AXIS","TRACK_EDGE_0","TRACK_EDGE_1","TRACK_EDGE_2","TRACK_EDGE_3","TRACK_EDGE_4","TRACK_EDGE_5","TRACK_EDGE_6","TRACK_EDGE_7","TRACK_EDGE_8","TRACK_EDGE_9","TRACK_EDGE_10","TRACK_EDGE_11","TRACK_EDGE_12","TRACK_EDGE_13","TRACK_EDGE_14","TRACK_EDGE_15","TRACK_EDGE_16","TRACK_EDGE_17","TRACK_EDGE_18","ACCELERATION","BRAKE","STEERING"]
        writer.writerow(header)

        # Parse each line as a JSON object and write the values to the CSV file
        for line in log_file:
            try:
                line = line.split(" - ")[2]
            except:
                continue

            data = json.loads(line)
            row = [data["speed"][0], data["trackPos"], data["angle"], data["track"][0], data["track"][1], data["track"][2], data["track"][3], data["track"][4], data["track"][5], data["track"][6], data["track"][7], data["track"][8], data["track"][9], data["track"][10], data["track"][11], data["track"][12], data["track"][13], data["track"][14], data["track"][15], data["track"][16], data["track"][17], data["track"][18], data["acceleration"], data["brake"], data["steering"]]
            writer.writerow(row)