import os
import Tkinter
import tkFont

# Script to run
script = 'scrape.py'

# Create Tkinter window
root = Tkinter.Tk()
root.title('Get TripAdvisor Data')

# Adjust window size
w = root.winfo_screenwidth() # get screen width
h = root.winfo_screenheight() # get screen height
s = 2 # set scaling constant (2 = 1/4 screen size)
WINDOW_SIZE = str(w/s) + 'x' + str(h/(s*2))
root.geometry(WINDOW_SIZE)

# Create label for input box
labelText = Tkinter.StringVar()
labelText.set('Please enter a location (City, State)')
labelDir = Tkinter.Label(root,textvariable=labelText,height=2)
labelDir['font'] = tkFont.Font(size=h/60) # fontsize ~ 36pt
labelDir['fg'] = 'black'
labelDir.pack()

# Create text entry box for user to specify location
e = Tkinter.Entry(root)
e['font'] = tkFont.Font(size=h/60) # fontsize ~ 36pt
e['fg'] = 'grey'
e.insert(0,'Austin, TX')
e.pack()
e.focus_set()

# Blank space
blank = Tkinter.Label(root,height=0)
blank['font'] = tkFont.Font(size=h/120) # fontsize ~ 36pt
blank.pack()

# Retrieve user input and submit as query to 'scrapy.py'
def callback():
	search = e.get() # collect user input to str 'search'
	search = search.split(', ') # split 'city' and 'state'
	search = [s.replace(' ','_') for s in search]
	print 'Argument passed to script...'
	os.system('python ' + script + ' -q=' + search[0] + ' -s=' + search[1])
	root.destroy() # kill window after running script

# Catch enter key as search
def enter(event):
	callback() # run query
root.bind('<Return>', enter)

# Create button to run script
b = Tkinter.Button(root, text='Scrape TripAdvisor!',command=callback)
b['font'] = tkFont.Font(size=h/60) # fontsize ~ 36pt
b.configure(foreground='black')
b.pack()

# Start loop
root.mainloop()