import json
from datetime import datetime

def update(track, time):
    print(track)
    print(time)
    with open('daily_records.json', 'r') as file:
        records = json.load(file)
        old_time = datetime.strptime(records[track],'%M:%S.%f').time()
        new_time = datetime.strptime(time,'%M:%S.%f').time()
    
    print("OLD:", old_time)
    print("NEW:", new_time)
    if old_time > new_time:
        old_record = records[track]
        with open('daily_records.json', 'w') as file:
            records[track] = time
            json.dump(records, file, indent=4)
        return old_record