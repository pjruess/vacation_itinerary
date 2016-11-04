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
s = 4 # set scaling constant (2 = 1/4 screen size)
WINDOW_SIZE = str(w/s) + 'x' + str(h/s)
root.geometry(WINDOW_SIZE)

# Create text entry box for user to specify location
e = Tkinter.Entry(root)
e['font'] = tkFont.Font(size=h/60) # fontsize ~ 36pt
e.pack()
e.focus_set()

# Retrieve user input and submit as query to 'scrapy.py'
def callback():
	search = e.get() # collect user input to str 'search'
	search = search.replace(' ','_')
	os.system('python ' + script + ' -q=' + (search))
	root.destroy() # kill window after running script

# Catch enter key as search
def enter(event):
	callback() # run query
root.bind('<Return>', enter)

# Create button to run script
b = Tkinter.Button(root, text="Scrape TripAdvisor!",command=callback)
b['font'] = tkFont.Font(size=h/60) # fontsize ~ 36pt
b.pack()

# Start loop
root.mainloop()