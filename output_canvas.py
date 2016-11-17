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

number_frame = 3	# number of frames
frame_width = screen_width / number_frame
frame_height = screen_height

def AddFrame(parentwidget, width = frame_width, height = frame_height, relief = tk.SUNKEN):
	return tk.Frame(parentwidget, height = height, width = width, relief = relief)

# Create three frames
map_frame = AddFrame(master)
map_frame.pack(side = tk.LEFT)

itinerary_frame = AddFrame(master)
itinerary_frame.pack(side = tk.LEFT)

review_frame = AddFrame(master)
review_frame.pack(side = tk.LEFT)

# Add image to the first frame
image = Image.open('ToRudys.png')
width, height = image.size
map_width = frame_width
map_height = (map_width * height) / width
resized_image = image.resize((map_width, map_height), Image.ANTIALIAS)
route_map = ImageTk.PhotoImage(resized_image)
image_label = tk.Label(map_frame, image = route_map, relief = tk.SUNKEN)
image_label.image = route_map
image_label.pack()



# Create Menu items
menu = tk.Menu(master)
master.config(menu = menu)	# attach menu to master

# Menu operations
def CmdNewSearch():
	print 'New Search'

def CmdExit():
	master.destroy()

def HelpAbout():
	print 'Version 1.0'

def HelpEmail():
	print 'Email authors'

# Commands Menu
filemenu = tk.Menu(menu)
menu.add_cascade(label = 'Commands', menu = filemenu)
filemenu.add_command(label = 'New Search', command = CmdNewSearch)
filemenu.add_separator()
filemenu.add_command(label = 'Exit', command = CmdExit)

# Help Menu
helpmenu = tk.Menu(menu)
menu.add_cascade(label = 'Help', menu = helpmenu)
helpmenu.add_command(label = 'About', command = HelpAbout)
helpmenu.add_command(label = 'Email authors', command = HelpEmail)


# review_frame = tk.Frame(master, bd = 2, relief = tk.SUNKEN)
# review_frame.grid_rowconfigure(0, weight = 1)	# configure row index of a grid
# review_frame.grid_columnconfigure(0, weight = 1)

# # vertical scrollbar
# # vscrollbar = tk.Scrollbar(master)
# # vscrollbar.pack(side = tk.RIGHT, fill = tk.Y)
# vscrollbar = tk.Scrollbar(review_frame)
# vscrollbar.grid(row = 0, column = 1, sticky = tk.N + tk.S)

# # # horizontal scrollbar
# # hscrollbar = tk.Scrollbar(master, orient = tk.HORIZONTAL)
# # hscrollbar.pack(side = tk.BOTTOM, fill = tk.X)

# # wrap: WORD, CHAR, NONE
# # review_text = tk.Text(master, wrap = tk.WORD, yscrollcommand = vscrollbar.set)
# # review_text.pack()
# # # Alternatively for wrap = NONE
# # review_text = tk.Text(master, wrap = tk.NONE, xscrollcommand = hscrollbar.set, yscrollcommand = vscrollbar.set)
# # review_text.pack()
# review_text = tk.Text(review_frame, wrap = tk.NONE, bd = 0, yscrollcommand = vscrollbar.set)
# review_text.grid(row = 0, column = 0, sticky = tk.N+tk.S+tk.E+tk.W)

# review_text.insert(tk.END, 'Hello World!\nYeah')
# # hscrollbar.config(command = review_text.xview)
# vscrollbar.config(command = review_text.yview)
# review_frame.pack()

tk.mainloop()