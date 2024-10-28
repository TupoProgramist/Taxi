import time
import keyboard
import pyautogui
import pyperclip

import json
from pynput.keyboard import Controller
import msvcrt

import tel_lb

#Uploads program useful data
def configuration():
    #A) uploading the coordinates 
    with open('json/coordinates.json', 'r') as file:
        coordinates = json.load(file)
        
    #B) uploading the time pauses
    with open('json/pauses.json', 'r') as file:
        pauses = json.load(file)
        
    return coordinates, pauses

def channels():
    pass

def read_json_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}  

def add_new_key_with_list(file_name, new_key, new_list):
    # Read the current data from the JSON file
    data = read_json_file(file_name)
    
    # Add the new key with the list value
    data[new_key[:-1]] = new_list
    
    # Step 3: Write the updated data back to the file
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def delete_first_row(parent_channels):
    with open(parent_channels, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Remove the first line
    got = lines[0]
    lines = lines[1:]
    # Open the file in write mode and save the remaining lines
    with open(parent_channels, 'w', encoding='utf-8') as file:
        file.writelines(lines)
    
    return got

def complete_parent(parent_channels, used):
    parent = delete_first_row(parent_channels)
    # Open the file in append mode and add the new line
    with open(used, 'a', encoding='utf-8') as file:
        file.write(parent)  # Adding a newline character at the end

#Starts the process of verification of channels in "unchecked_channels"
def verification(tel):
    with open('accepted_channels.txt', 'w', encoding='utf-8') as file_a, open('denied_channels.txt', 'w', encoding='utf-8') as file_d:
        
        for unchecked_channel in unchecked_channels:
            tel.verification(unchecked_channel)
            # This code snippet is performing a verification process for a specific channel. Here's a
            # breakdown of what it does:
            pyautogui.click(x=1500, y=900)
            key = 0
            
            while key != 'a' and key != 'd':
                key = msvcrt.getch().decode('utf-8')
                time.sleep(1/30)    
    
        if key == 'a':
            file_a.write(f"{unchecked_channel}")
            print('accepted V')
        elif key == 'd':
            file_d.write(f"{unchecked_channel}")
            print('denied X')

def scram(tel, file, parent):
    children_screenshots = tel.scram_channel(parent)
    for image in children_screenshots:
        try:
            text = pytesseract.image_to_string(image, lang='ukr+eng')
            
            if text == "":
                continue
            
            file.write(f"{text}")
        except:
            continue
        
if __name__ == '__main__':    
    #0. Initilazing
    coordinates, pauses = configuration()
    keyboard = Controller()
    

    # Output the copied text
    # print(f"{copied_text}")
    # while 1:
    #     time.sleep(2)
    #     print(pyautogui.position())
    
    tel = tel_lb.Tel(coordinates, keyboard, pauses)
    
    with open('lists/farcing/parent_channels.txt', 'r', encoding='utf-8') as file:
        # Read all lines into a list
        parents = file.readlines()
    
    for parent in parents:
        childrens = tel.scram_channel(parent)
        add_new_key_with_list("lists/farcing/childrens.json", parent, childrens)
        
        complete_parent("lists/farcing/parent_channels.txt", "lists/farcing/used.txt")
    
    