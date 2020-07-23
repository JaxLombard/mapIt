#! python3
#mapit.py launches a google map in the browser using an address from the command line or clipboard

#import modules
import webbrowser, sys, pyperclip
if len(sys.argv) > 1:
    #grab address from cmd line
    address = ' '.join(sys.argv[1:])
else:
    #get address from clipboard
    address = pyperclip.paste()

webbrowser.open('https://www.google.com/maps/place/' + address)