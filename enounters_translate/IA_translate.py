import json
import time
import os

#JSON SAMPLE

input_file = "encounters_short.json"
output_file = "encounters_sp.json"

output_file_exists = os.path.exists(output_file)
if not output_file_exists:
    data = read_json_file(input_file)
    write_json_file(output_file, data)
else:
    data = read_json_file(output_file)

json_data_sample = {
    "EMPTY": [
        {
            "text": "",
            "ambient": "NULL_MUSIC",
            "ambientVolume": 1
        }
    ],
    "STORY-END": [
        {
            "text": "Thank you so much! This is the current end of story mode - please be sure to try out the Create a Character/Adventure mode to get the full extent of what's currently in Tales of Androgyny!",
            "animatedForeground": {
                "animation": "GHOST",
                "parameters": []
            }
        },
        {
            "text": "There are more characters, more scenarios, and a lot more play area in Adventure mode, and you can create your character and select their skills, perks, and spells.  Enjoy!"
        }
    ]
}

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_json_file(file_path, data):
    with open(file_path, 'w', encoding="utf-8") as file:
        file.write("\n")
        json.dump(data, file, indent=4)

#dummy translate
def translate(text, dest="es"):
    if text == "":
        raise Exception("Empty text")
    text_split = text.split("\n")
    for idx, item in enumerate(text_split):
        text_split[idx] = f"[{dest}]{item}"

    text = "\n".join(text_split)
    return text

def get_all_keys():
    data = read_json_file(input_file)
    return data.keys()

def get_text(key):
    data = read_json_file(input_file)
    text = []
    for item in data[key]:
        text.append(item["text"])
    output_text = "\n".join(text)
    return output_text

def log_output(text):
    date_time_stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    text = f"[{date_time_stamp}] {text}"
    with open("output_log.txt", "a") as f:
        f.write(text + "\n")

def log_error(text):
    date_time_stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    text = f"[{date_time_stamp}] {text}"
    with open("error_log.txt", "a") as f:
        f.write(text + "\n")
    print(text)

def log_debug(text, file_name="debug_log.txt"):
    date_time_stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    text = f"[{date_time_stamp}] {text}"
    with open(file_name, "a") as f:
        f.write(text + "\n")

def save_text(key, text):
    try:
        # Use global keyword if output_file_exists is defined outside the function
        global output_file_exists
        
        # Load data from appropriate file
        if output_file_exists:
            data = read_json_file(output_file)
        else:
            data = read_json_file(input_file)
            output_file_exists = True
            
        # Validate inputs
        if key not in data:
            raise KeyError(f"Key '{key}' not found in data")
        if len(data[key]) != len(text):
            raise ValueError(f"Length mismatch: expected {len(data[key])} items, got {len(text)}")
            
        # Update text values more efficiently using list comprehension
        data[key] = [dict(item, text=new_text) for item, new_text in zip(data[key], text)]
        
        # Write updated data to file
        write_json_file(output_file, data)

        
    except Exception as e:
        print(f"Error in save_text: {e}")
        raise


def print_all_text():
    for key in get_all_keys():
        print(key)
        print(get_text(key))

def print_all_keys():
    for key in get_all_keys():
        print(key)
#secure translate function
def translate_section(section):
    text = get_text(section)
    try:
        translated_text = translate(text, "es")
        translated_text_array = translated_text.split("\n")
        save_text(section, translated_text_array)
        log_output(f"Translated section: {section}")
    except Exception as e:
        # save log
        error_text = f"Error translating section: {section} \n\t{e}"
        log_error(error_text)

def translate_all(start_at=0, stop_at=-1):
    max_entries = len(get_all_keys())
    for idx, key in enumerate(get_all_keys()):
        if idx < start_at:
            continue
        if stop_at != -1 and idx > stop_at:
            break
        translate_section(key)
        time.sleep(0.5)
        print(f"Translated {idx+1}/{max_entries} sections")

# character count by section
def count_characters():
    for key in get_all_keys():
        text = get_text(key)
        log_debug(f"{key}: {len(text)}")
        #print(f"{key}: {len(text)}")
        if len(text) > 5000:
            log_debug(f"{key}: {len(text)}", "long_sections.txt")