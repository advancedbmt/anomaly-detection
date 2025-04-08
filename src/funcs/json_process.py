import json
from datetime import datetime



def parse_entry(entry):
    time_part, state_part = entry.split(" ", 1)
    

    if ":" in time_part:
        time_obj = datetime.strptime(time_part.lower(), "%I:%M%p").time()
    else:
        time_obj = datetime.strptime(time_part.lower(), "%I%p").time()
    
    time_str = time_obj.strftime("%H:%M")
    state_clean = state_part.replace("\\", " ")
    
    return (time_str, state_clean)


if __name__ == "__main__":
    with open("config.json", "r") as file:
        config = json.load(file)


    batch_data = config["state_timeline"]["batch"]

    parsed_batch = [parse_entry(entry) for entry in batch_data]


    print("Parsed batch schedule:")
    print(parsed_batch)
