import os
import Tkinter
import tkFont

# Script to run
script = 'scrape_final.py'

# Create Tkinter window
root = Tkinter.Tk()
root.title('Get TripAdvisor Data')

# Adjust window size
w = root.winfo_screenwidth() # get screen width
h = root.winfo_screenheight() # get screen height
s = 2 # set scaling constant (2 = 1/4 screen size)
WINDOW_SIZE = str(w/s) + 'x' + str(h/s)
root.geometry(WINDOW_SIZE)

# # Create default font
# font = tkFont.Font(size=h/60,weight='bold')

# Create label for city/state input box
citylabeltext = Tkinter.StringVar()
citylabeltext.set('Please enter a destination (City, State)')
citylabel = Tkinter.Label(root,textvariable=citylabeltext,height=2)
citylabel['font'] = tkFont.Font(size=h/60) # fontsize ~ 36pt
citylabel['fg'] = 'black'
citylabel.pack()

# Create text entry box for user to specify location
city = Tkinter.Entry(root)
city['font'] = tkFont.Font(size=h/60) # fontsize ~ 36pt
city['fg'] = 'grey'
city.insert(0,'Austin, TX')
city.pack()
city.focus_set()

# Create label for hotel input box
baselabeltext = Tkinter.StringVar()
baselabeltext.set('Please enter a Hotel at your destination')
baselabel = Tkinter.Label(root,textvariable=baselabeltext,height=2)
baselabel['font'] = tkFont.Font(size=h/60) # fontsize ~ 36pt
baselabel['fg'] = 'black'
baselabel.pack()

# Create text entry box for user to specify hotel
base = Tkinter.Entry(root)
base['font'] = tkFont.Font(size=h/60) # fontsize ~ 36pt
base['fg'] = 'grey'
base.insert(0,'Hotel Ella')
base.pack()
base.focus_set()

# Blank space
blank = Tkinter.Label(root,height=0)
blank['font'] = tkFont.Font(size=h/120) # fontsize ~ 36pt
blank.pack()

# Retrieve user input and submit as query to 'scrapy.py'
def callback():
	search = city.get() # collect user input to str 'search'
	search = search.split(', ') # split 'city' and 'state'
	search = [s.replace(' ','_') for s in search]
	hotelname = base.get()
	hotelname = hotelname.replace(' ','_')
	print 'Argument passed to script...'
	os.system('python ' + script + ' -city=' + search[0] + ' -state=' + search[1] + ' -base=' + hotelname)
	root.destroy() # kill window after running script

# Catch enter key as search
def enter(event):
	callback() # run query
root.bind('<Return>', enter)

# Create button to run script
b = Tkinter.Button(root, text='Get my itinerary!',command=callback)
b['font'] = tkFont.Font(size=h/60) # fontsize ~ 36pt
b.configure(foreground='black')
b.pack()

# Start loop
root.mainloop()