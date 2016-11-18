import sys
if sys.version_info[0] < 3:
	import Tkinter as tk
else:
	import tkinter as tk
from PIL import Image, ImageTk


master = tk.Tk()
master.title('Optimal Itinerary')

# Works only if there is a single display; otherwise sums the value from each display
screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()
screen_width_factor = 0.9
screen_height_factor = 0.8
screen_size_ratio = 9.0 / 16.0
number_frame = 3	# number of frames
frame_width = int(screen_width_factor * screen_width) / number_frame
frame_height = int(screen_height_factor * screen_height)
master.minsize(frame_width, int(screen_size_ratio * frame_width))
master.maxsize(screen_width, screen_height)
master.geometry("%dx%d%+d%+d" % (int(1.03 * number_frame * frame_width), screen_height, 0, 0))		# "%dx%d%+d%+d" % (width, height, xoffset, yoffset)



def AddFrame(parentwidget, width = frame_width, height = frame_height, relief = tk.SUNKEN):
	return tk.Frame(parentwidget, height = height, width = width, relief = relief, bd = 3)

# Create 3 frames -- map frame, Itinerary frame, reviews frame
map_frame = AddFrame(master)
itinerary_frame = AddFrame(master)
review_frame = AddFrame(master)


# Create Menu items
menu = tk.Menu(master)
master.config(menu = menu)	# attach menu to master

# Menu operations
def CmdNewSearch():
	print 'New Search'

def CmdPrint():
	print 'Itinerary'

def CmdExit():
	master.destroy()

def HelpAbout():
	print 'Version 1.0'

def MailAuthor(name):
	import webbrowser
	email = {'Melissa': 'mmlee246@gmail.com', 'Paul': 'pjruess@gmail.com', 'Sudesh': 'sudesh@utexas.edu'}[name]
	link = 'mailto:{0}?subject={1}&body=Hi%20{2}\n'.format(email, 'Help%20with%20Optimal%20Itinerary', name)
	webbrowser.open(link)

# Commands Menu
filemenu = tk.Menu(menu)
menu.add_cascade(label = 'Commands', menu = filemenu)
filemenu.add_command(label = 'New Search', command = CmdNewSearch)
filemenu.add_command(label = 'Print Itinerary', command = CmdPrint)
filemenu.add_separator()
filemenu.add_command(label = 'Exit', command = CmdExit)

# Help Menu
helpmenu = tk.Menu(menu)
menu.add_cascade(label = 'Help', menu = helpmenu)
helpmenu.add_command(label = 'About', command = HelpAbout)
# Authors
authormenu = tk.Menu(helpmenu)
helpmenu.add_cascade(label = 'Email authors', menu = authormenu)
authormenu.add_command(label = 'Melissa Lee', command = lambda: MailAuthor('Melissa'))
authormenu.add_command(label = 'Paul Ruess', command = lambda: MailAuthor('Paul'))
authormenu.add_command(label = 'Sudesh Agrawal', command = lambda: MailAuthor('Sudesh'))



# Add elements to map frame
map_frame_label = tk.Label(map_frame, text = 'Map:', font = 'Literata 20', justify = tk.CENTER, bd = 0, cursor = 'spider')
# Add map
image = Image.open('ToRudys.png')
width, height = image.size
map_width = frame_width
map_height = (map_width * height) / width
resized_image = image.resize((map_width, map_height), Image.ANTIALIAS)
route_map = ImageTk.PhotoImage(resized_image)
image_label = tk.Label(map_frame, image = route_map, relief = tk.SUNKEN)
image_label.image = route_map
# Add button to remove everything save the map
def ZoomMap():
	itinerary_frame.grid_remove()
	review_frame.grid_remove()
	map_frame_button.grid_remove()
	map_frame_hidden_button.grid()

	image = Image.open('ToRudys.png')
	route_map = ImageTk.PhotoImage(image)
	image_label['image'] = route_map
	image_label.image = route_map
	

def RestoreMap():
	itinerary_frame.grid()
	review_frame.grid()
	map_frame_hidden_button.grid_remove()
	map_frame_button.grid()

	image = Image.open('ToRudys.png')
	width, height = image.size
	map_width = frame_width
	map_height = (map_width * height) / width
	resized_image = image.resize((map_width, map_height), Image.ANTIALIAS)
	# resized_image = image.resize((1024, frame_height), Image.ANTIALIAS)
	route_map = ImageTk.PhotoImage(image)
	image_label['image'] = route_map
	image_label.image = route_map


map_frame_button = tk.Button(map_frame, text = 'Zoom', font = '16', command = ZoomMap)
map_frame_hidden_button = tk.Button(map_frame, text = 'Restore', font = '16', command = RestoreMap)



# Add elements to itinerary_frame



# Position the widgets
map_frame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.W)
itinerary_frame.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = tk.N + tk.W)
review_frame.grid(row = 0, column = 2, padx = 5, pady = 5, sticky = tk.N + tk.W)

map_frame_label.grid(row = 0, column = 0, sticky = tk.W + tk.E)
image_label.grid(row = 1, column = 0, sticky = tk.W + tk.E)
map_frame_button.grid(row = 2, column = 0)
map_frame_hidden_button.grid(row = 3, column = 0)
map_frame_hidden_button.grid_remove()

master.mainloop()