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
master.geometry("%dx%d%+d%+d" % (int(number_frame * (frame_width + 25)), screen_height, 0, 0))		# "%dx%d%+d%+d" % (width, height, xoffset, yoffset)


font_content = 'Literata 12'
font_head = ''


# def AddFrame(parentwidget, width = frame_width, height = frame_height, relief = tk.SUNKEN):
# 	return tk.Frame(parentwidget, height = height, width = width, relief = relief, bd = 3)

def AddFrame(parentwidget, text, height = frame_height, width = frame_width, relief = tk.SUNKEN):
	return tk.LabelFrame(parentwidget, text = text,  height = height, width = width, relief = relief, bd = 3, font = 'Literata 20 bold')


# Create 3 frames -- map frame, Itinerary frame, reviews frame
map_frame = AddFrame(master, text = 'Map')
itinerary_frame = AddFrame(master, text = 'Schedule')
review_frame = AddFrame(master, text = 'Reviews')


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
	print map_frame['width']
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

	map_frame.config(width = frame_width, height = frame_height)
	image = Image.open('ToRudys.png')
	width, height = image.size
	map_width = frame_width
	map_height = (map_width * height) / width
	resized_image = image.resize((map_width, map_height), Image.ANTIALIAS)
	# resized_image = image.resize((1024, frame_height), Image.ANTIALIAS)
	route_map = ImageTk.PhotoImage(image)
	image_label.config(image = route_map)
	# image_label['image'] = route_map
	image_label.image = route_map


map_frame_button = tk.Button(map_frame, text = 'Zoom', font = '16', command = ZoomMap)
map_frame_hidden_button = tk.Button(map_frame, text = 'Restore', font = '16', command = RestoreMap)



# Add elements to itinerary_frame
itinerary_frame_list = tk.Listbox(itinerary_frame, bd = 0, font = 'Literata 14')
# Add scrollbars
itinerary_yscrollbar = tk.Scrollbar(itinerary_frame)
# attach list box to scrollbar
itinerary_frame_list.config(yscrollcommand = itinerary_yscrollbar.set)
itinerary_yscrollbar.config(command = itinerary_frame_list.yview)

for i in range(20):
	itinerary_frame_list.insert(tk.END, u'09:00\u201309:30 Hotel {}'.format(i+1))



# Add elements to review frame
# number_reviews = 0
# review_frame_review_label = []

# def CreateReviewLabel(root, text, number_reviews):
# 	review_frame_review_label.append(tk.Label(root, text = text, font = 'Literata 14', justify = tk.LEFT, bd = 2, relief = tk.SUNKEN, padx = 0, pady = 0))
# 	review_frame_review_label[number_reviews].grid(row = number_reviews, column = 0, sticky = tk.W + tk.E)
# 	review_frame_review_label[number_reviews].columnconfigure(0, weight = 1)

# CreateReviewLabel(review_frame, 'Sudesh\nRating: 4.3\nGood!\n', number_reviews)
# number_reviews += 1
# CreateReviewLabel(review_frame, 'Melissa\nRating: 4.0\nGood!\n', number_reviews)
# number_reviews += 1
# CreateReviewLabel(review_frame, 'Paul\nRating: 3.9\nExcellent!\n', number_reviews)


review_frame_review_text = tk.Text(review_frame, bd = 1, exportselection = 1, font = font_content, width = 45)
text = 'Sudesh\nRating: 4.3\nGood!\n\n' + 'Melissa\nRating: 4.0\nGood!\n\n' + 'Paul\nRating: 3.9\nExcellent!\n\n'
review_frame_review_text.insert(tk.END, text)
review_frame_review_text.config(state = tk.DISABLED)
# Add scrollbars
review_text_yscrollbar = tk.Scrollbar(review_frame)
review_text_xscrollbar = tk.Scrollbar(review_frame, orient = tk.HORIZONTAL)
# attach review text to scrollbars
review_frame_review_text.config(yscrollcommand = review_text_yscrollbar.set, xscrollcommand = review_text_xscrollbar.set)
review_text_yscrollbar.config(command = review_frame_review_text.yview)
review_text_xscrollbar.config(command = review_frame_review_text.xview)


# review_frame_review_text = []

# review_frame_review_text.append(tk.Text(review_frame, bd = 1, cursor = 'spider', exportselection = 1, font = 'Literata 12', width = 45))
# review_frame_review_text[0].grid(row = 0, column = 0, sticky = tk.W)
# review_frame_review_text[0].insert(tk.END, 'Hello\nBrother')
# # review_frame_review_text[0].config(state = tk.DISABLED)
# review_frame_review_text[0].insert(tk.END, 'Hello\nBrother')
# for x in xrange(1,1000):
# 	review_frame_review_text[0].insert(tk.END, 'Hello\nBrother')



# Position the widgets
map_frame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.W)
map_frame.columnconfigure(0, minsize = frame_width)
map_frame.rowconfigure(1, weight = 1)
# map_frame.grid_propagate(False)
itinerary_frame.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = tk.N + tk.W)
itinerary_frame.columnconfigure(0, pad = 0, minsize = frame_width, weight = 1)
itinerary_frame.rowconfigure(1, minsize = int(0.75 * frame_height))
review_frame.grid(row = 0, column = 2, padx = 5, pady = 5, sticky = tk.N + tk.W + tk.E)
review_frame.columnconfigure(0, minsize = frame_width)
for i in xrange(1, review_frame.grid_size()[1]):
	review_frame.rowconfigure(i, weight = 1)



image_label.grid(row = 0, column = 0, sticky = tk.W + tk.E)
map_frame_button.grid(row = 1, column = 0)
map_frame_hidden_button.grid(row = 2, column = 0)
map_frame_hidden_button.grid_remove()


itinerary_frame_list.grid(row = 0, column = 0, sticky = tk.W + tk.E + tk.N + tk.S, padx = 0, pady = 0, ipadx = 0, ipady = 0)
itinerary_yscrollbar.grid(row = 0, column = 1, sticky = tk.E + tk.N + tk.S, padx = 0, pady = 0, ipadx = 0, ipady = 0)


review_frame_review_text.grid(row = 0, column = 0, sticky = tk.W + tk.E)
review_text_yscrollbar.grid(row = 0, column = 1, sticky = tk.E + tk.N + tk.S, padx = 0, pady = 0, ipadx = 0, ipady = 0)
review_text_xscrollbar.grid(row = 1, column = 0, sticky = tk.N + tk.W + tk.E, padx = 0, pady = 0, ipadx = 0, ipady = 0)


master.mainloop()
# master.destroy()	# explicitly destroys the main window when the event loop is terminated; needed for some development envrionments