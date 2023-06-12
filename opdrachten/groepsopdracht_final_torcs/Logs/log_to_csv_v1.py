import json
import csv

# Open the log file for reading
with open('opdrachten\groepsopdracht_final_torcs\Logs\Race_Log.log', 'r') as log_file:

    # Open the CSV file for writing
    with open('opdrachten\groepsopdracht_final_torcs\Logs\output.csv', 'w+', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Write the header row to the CSV file
        header = ['timestamp', 'angle', 'curLapTime', 'damage', 'distFromStart', 'distRaced', 'fuel', 'gear', 'lastLapTime', 'racePos', 'rpm', 'speedX', 'speedY', 'speedZ', 'track', 'trackPos', 'wheelSpinVel', 'z', 'focus', 'x', 'y', 'roll', 'pitch', 'yaw', 'speedGlobalX', 'speedGlobalY']
        writer.writerow(header)

        # Parse each line as a JSON object and write the values to the CSV file
        for line in log_file:
            try:
                line = line.split(' - ')[2]
            except:
                continue

            data = json.loads(line)
            row = [data['angle'], data['curLapTime'], data['damage'], data['distFromStart'], data['distRaced'], data['fuel'], data['gear'], data['lastLapTime'], data['racePos'], data['rpm'], data['speedX'], data['speedY'], data['speedZ'], data['track'], data['trackPos'], data['wheelSpinVel'], data['z'], data['focus'], data['x'], data['y'], data['roll'], data['pitch'], data['yaw'], data['speedGlobalX'], data['speedGlobalY']]
            writer.writerow(row)