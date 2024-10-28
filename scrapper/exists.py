import os

parent_channels = 'lists/farcing/parrent_channels.txt'

# Check if the directory exists
if not os.path.exists(os.path.dirname(parent_channels)):
    print(f"Directory '{os.path.dirname(parent_channels)}' does not exist.")
else:
    print(f"Directory '{os.path.dirname(parent_channels)}' exists.")

# Check if the file exists
if not os.path.isfile(parent_channels):
    print(f"File '{parent_channels}' does not exist.")
else:
    print(f"File '{parent_channels}' exists.")