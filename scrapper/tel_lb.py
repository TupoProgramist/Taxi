import pyautogui
import time
from pynput.keyboard import Controller, Key
import pyperclip
import math

class Tel:
    #initializing the class +
    def __init__(self,coordinates,keyboard,pauses):
        self.coordinates = coordinates
        self.pauses = pauses
        #the keyboard to write down
        self.keyboard = keyboard

    #completely scrams some channel
    def scram_channel(self,name):
        children_list = []
        
        #A) typing in the name
        self.type_find_input(name)
        
        #B) Selecting the first recommended channel
        self.click_first_channel()
        
        #C) Subscribing on the channel
        self.click_subscribe()
        
        #E) Picking the "show more"
        self.click_show_more()
        
        #F) Farcing
        
        #1. initializing the current
        current = self.coordinates["first_recommended"].copy()  
        
        #2. reading the firs 15 channels
        for i in range(16): # 16
            current[1] += self.coordinates["next_dis"][1]
            pyautogui.moveTo(current[0],current[1])
            children_list.append(self.check_reccomendation())
        
        #iii. reading the other 85 channels
        for i in range(90-16): #95
            pyautogui.moveTo(current[0],current[1])
            jumps = math.floor(i/8)
            for j in range(jumps):
                pyautogui.scroll(-self.coordinates["scroll_dis"]*8)
            for j in range(i % 8):
                pyautogui.scroll(-self.coordinates["scroll_dis"])
            children_list.append(self.check_reccomendation())
            
        return children_list
        
    def check_reccomendation(self):
        #A) selecting the current reccomendation
        self.click(pyautogui.position())
        
        self.click(self.coordinates["header"])
        
        self.click(self.coordinates["title"])
        self.click(self.coordinates["title"])
        self.click(self.coordinates["title"])
        
        copied_title = self.copy_focused_value()
        
        self.click(self.coordinates["close_description"])
        self.click(self.coordinates["close_recommendation"])
        time.sleep(self.pauses["close_recommendation"])
        
        self.click_show_more()
        
        print(copied_title)
        return copied_title
        
        
        
    
    #leaving the channel
    def leave_channel(self, name):
        #A) typing in the name
        self.type_find_input(name)
        
        #B) selecting the first channel
        first_channel = self.coordinates["first_channel"]
        self.click(first_channel, False)
        
        #C) clicking the leave button
        leave_channel = self.coordinates["leave_channel"]
        self.click(leave_channel)
        
        #D) Confirming the left
        leave_channel_confirmation = self.coordinates["leave_channel_confirmation"]
        self.click(leave_channel_confirmation)
    
    #type in the name of channel in find input
    def type_find_input(self,name):
        #A) Clearing find input
        self.clean_find_input()
        #B) Focus on find input
        self.click_find_input()
        self.keyboard.type(name)
        
        time.sleep(self.pauses["find_channel"])
    
    #click on the find input
    def click_find_input(self):
        find_input = self.coordinates["find_input"]
        self.click(find_input)
    
    #click on the firt reccomended channel   
    def click_first_channel(self):
        first_channel = self.coordinates["first_channel"]
        self.click(first_channel)
        
        time.sleep(self.pauses["load_channel"])
    
    #click on the "suscribe the channel" button
    def click_subscribe(self):
        subscribe = self.coordinates["subscribe"]
        self.click(subscribe)

        time.sleep(self.pauses["subscribe"])
    
    #click on "show more channels"
    def click_show_more(self):
        show_more = self.coordinates["show_more"]
        self.click(show_more)

        time.sleep(self.pauses["show_more"])
    
    #cleaning find input
    def clean_find_input(self):
        
        clean_find_input = self.coordinates["clean_find_input"]
        self.click(clean_find_input)
        time.sleep(self.pauses["clean_find"])
    
    #modified clicking function (which works properly)
    def click(self, coords, left = True):
        pyautogui.moveTo(coords[0], coords[1])
        time.sleep(self.pauses["click"])
        
        if left:
            pyautogui.click()
        else:
            pyautogui.click(button='right')
            
    def copy_focused_value(self):
        # Press 'Ctrl + C'
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('c')
        self.keyboard.release('c')
        self.keyboard.release(Key.ctrl)

        # Allow a small delay for the clipboard to update
        time.sleep(self.pauses["copy"])
        return pyperclip.paste()