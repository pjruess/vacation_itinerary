import sys
from datetime import datetime
if sys.version_info[0] < 3:
	import Tkinter as tk
else:
	import tkinter as tk
from PIL import Image, ImageTk
import read_google as gapi


master = tk.Tk()
master.title('Optimal Itinerary')
master.resizable(0, 0)	# cannot resize the master window in x or y direction

# Works only if there is a single display; otherwise sums the value from each display
screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()
screen_width_factor = 0.93
screen_height_factor = 0.8
usable_screen_width = screen_width_factor * screen_width
usable_screen_height = screen_height_factor * screen_height
screen_size_ratio = 9.0 / 16.0
number_frame = 3	# number of frames
frame_width = int( (usable_screen_width - ( number_frame + 1) * 5 - 8) / number_frame)
frame_height = int(usable_screen_height)

master.minsize(frame_width + (5 * (number_frame + 1)) + 5, int(screen_size_ratio * frame_width))
master.maxsize(screen_width, screen_height)
master.geometry("%dx%d%+d%+d" % (screen_width, screen_height, 0, 0))		# "%dx%d%+d%+d" % (width, height, xoffset, yoffset)


# Inputs

font_content = 'Calibri 12'
font_head = ('Cambria', 24, 'bold')
# font_head = 'Cambria 20 bold'
input_map = 'ToRudys.png'

myurl = gapi.build_url_text_search(query = 'top restaurants in Austin, TX')
myresponse = gapi.GetResponse(myurl)
myresults = gapi.GetResults(myresponse)
input_country = 'US'
input_city = 'Austin'
input_state = 'TX'
input_itinerary = []

if len(myresults) > 0:
	for result in myresults:
		# print '{0}: {1}'.format(result['name'], result['address'])
		input_itinerary.append(result['name'])
	# printing the details of the top result
	
else:
	print 'No results available!'

review_content = ''
reviews_required = 3


def AddLabelFrame(parentwidget, text, height = frame_height, width = frame_width, relief = tk.SUNKEN, font = font_head):
	return tk.LabelFrame(parentwidget, text = text,  height = height, width = width, relief = relief, bd = 2, font = font, labelanchor = tk.N + tk.W , padx = 1, pady = 1)


# Create 3 frames -- map frame, Itinerary frame, reviews frame
map_frame = AddLabelFrame(master, text = 'Map')
itinerary_frame = AddLabelFrame(master, text = 'Schedule')
review_frame = AddLabelFrame(master, text = 'Reviews')


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
image = Image.open(input_map)
width, height = image.size
map_ratio = float(height) / width
map_width = frame_width
map_height = int((map_width * height) / width)

if width > (2.2 * frame_width):
	width = int(2.2 * frame_width)
	height = int(2.2 * frame_width * map_ratio)
	image = image.resize((width, height), Image.ANTIALIAS)

resized_image = image.resize((map_width, map_height), Image.ANTIALIAS)

route_map = ImageTk.PhotoImage(image)
resized_route_map = ImageTk.PhotoImage(resized_image)
image_label = tk.Label(map_frame, image = route_map, relief = tk.SUNKEN)
resized_image_label = tk.Label(map_frame, image = resized_route_map, relief = tk.SUNKEN)
image_label.image = route_map
resized_image_label.image = resized_route_map

# Add button to remove everything save the map
def ZoomMap():
	itinerary_frame_list.config(height = int(min(height /16.0, usable_screen_height / 16.0)))
	if width > (2 * frame_width):
		itinerary_frame.grid_remove()
	review_frame.grid_remove()
	map_frame_zoom_button.grid_remove()
	resized_image_label.grid_remove()
	map_frame_restore_button.grid()
	image_label.grid()

def RestoreMap():
	itinerary_frame_list.config(height = int(map_height / 16.0))
	map_frame_restore_button.grid_remove()
	image_label.grid_remove()
	if width > (2 * frame_width):
		itinerary_frame.grid()
	review_frame.grid()
	map_frame_zoom_button.grid()
	resized_image_label.grid()
	

map_frame_zoom_button = tk.Button(map_frame, text = 'Zoom', font = '16', command = ZoomMap)
map_frame_restore_button = tk.Button(map_frame, text = 'Restore', font = '16', command = RestoreMap)



# Add elements to itinerary_frame
itinerary_list = tk.StringVar()
# height: number of lines, activestyle: 'underline', 'dotbox', 'none'
itinerary_frame_list = tk.Listbox(itinerary_frame, bd = 0, font = font_content, height = int(map_height / 16.0), activestyle = 'dotbox', exportselection = 1, listvariable = itinerary_list, selectmode = tk.BROWSE, state = tk.NORMAL)
# Add scrollbars
itinerary_yscrollbar = tk.Scrollbar(itinerary_frame)
# attach list box to scrollbar
itinerary_frame_list.config(yscrollcommand = itinerary_yscrollbar.set)
itinerary_yscrollbar.config(command = itinerary_frame_list.yview)

# for i in range(60):
# 	itinerary_frame_list.insert(tk.END, u'09:00\u201309:30 Hotel {}'.format(i+1))

for e in input_itinerary:
	itinerary_frame_list.insert(tk.END, u'09:00\u201309:30 {}'.format(e))

itinerary_frame_list.selection_set(0)
# print itinerary_list.get()
# itinerary_list.set('A B')


def GetReviews(event):
	# delete previous reviews
	review_frame_review_text.config(state = tk.NORMAL)	# enable editing of text
	review_frame_review_text.delete('1.0', tk.END)

	# provideint 'Getting reviews for place in the list at ({0}, {1})'.format(event.x, event.y)
	items = map(int, itinerary_frame_list.curselection())
	item = itinerary_frame_list.get(int(items[0]))
	item = item[12:]

	placename =  '{0}, {1}, {2}, {3}'.format(item, input_city, input_state, input_country)
	myurl = gapi.build_url_text_search(query = placename)
	myresponse = gapi.GetResponse(myurl)
	myresults = gapi.GetResults(myresponse)
	if len(myresults) > 0:
		myurl = gapi.build_url_place_details(placeid = myresults[0]['place_id'])
		myresponse = gapi.GetResponse(myurl)
		# myresults = gapi.GetPlaceDetails(myresponse, review_count = reviews_required)
		myresults = myresponse
		review_content = '\nReview(s) for {}:\n'.format(placename)

		if myresponse['status'] == 'OK':
			result = myresponse['result']
			if 'name' in result:
				review_content += '{}\n'.format(result['name'].encode('utf-8'))
			if 'rating' in result:
				review_content += 'Rating: {}\n'.format(result['rating'])
			if 'reviews' in result:
				for i in xrange(0, min(reviews_required, len(result['reviews']))):
					# review_content += result['reviews'].replace('\t', '')
					if ('author_name' in result['reviews'][i]) and ('text' in result['reviews'][i]) and ('time' in result['reviews'][i]):
						review_detail = result['reviews'][i]
						review_detail_name = review_detail['author_name'].encode('utf-8')
						review_detail_comment = review_detail['text'].encode('utf-8')
						review_detail_time = datetime.fromtimestamp(review_detail['time']).strftime('%c')
						review_content += '{0}: {1}\nSubmitted on: {2}\n\n'.format(review_detail_name, review_detail_comment, review_detail_time)	
	else:
		review_content = 'Reviews not available! TRY AGAIN!\n'

	review_frame_review_text.insert(tk.END, review_content)
	review_frame_review_text.config(state = tk.DISABLED)	# disable editing of text


itinerary_frame_list.bind('<ButtonRelease-1>', GetReviews)

# print itinerary_frame_list.get(0, 2)
# itinerary_frame_list.selection_clear(0, tk.END)
# itinerary_frame_list.activate(3)
# itinerary_list.set('Hello Brother')
# itinerary_frame_list.insert(6, 'Hello Brother')



# 

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


review_frame_review_text = tk.Text(review_frame, bd = 1, exportselection = 1, font = font_content, width = 45, wrap = tk.WORD, spacing1 = 3, spacing3 = 1)
# text = 'Sudesh\nRating: 4.3\nGood!\n\n' + 'Melissa\nRating: 4.0\nGood! friendly staff, beautiful interior and good food provide satisfaction and its central bar looks perfectly awesome in dim light. Going there is a good option if you want to spend some personal time with good food n drinks.\n\n' + 'Paul\nRating: 3.9\nExcellent!\n\n'

text = review_content
review_frame_review_text.insert(tk.END, text)
itinerary_frame_list.event_generate('<ButtonRelease-1>')
review_frame_review_text.config(state = tk.DISABLED)
# Add scrollbars
review_text_yscrollbar = tk.Scrollbar(review_frame)
# attach review text to scrollbars
review_frame_review_text.config(yscrollcommand = review_text_yscrollbar.set)
review_text_yscrollbar.config(command = review_frame_review_text.yview)


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
image_label.grid_remove()
resized_image_label.grid(row = 1, column = 0, sticky = tk.W + tk.E)
map_frame_zoom_button.grid(row = 2, column = 0)
map_frame_restore_button.grid(row = 3, column = 0)
map_frame_restore_button.grid_remove()


itinerary_frame_list.grid(row = 0, column = 0, sticky = tk.W + tk.E + tk.N + tk.S, padx = 0, pady = 0, ipadx = 0, ipady = 0)
itinerary_yscrollbar.grid(row = 0, column = 1, sticky = tk.E + tk.N + tk.S, padx = 0, pady = 0, ipadx = 0, ipady = 0)


review_frame_review_text.grid(row = 0, column = 0, sticky = tk.W + tk.E)
review_text_yscrollbar.grid(row = 0, column = 1, sticky = tk.E + tk.N + tk.S, padx = 0, pady = 0, ipadx = 0, ipady = 0)



countVar = tk.StringVar()
pos = '1.0'
# review_frame_review_text_last_line = review_frame_review_text.index('end')
# flag = True

# pos = review_frame_review_text.search('Submitted on:', pos, stopindex = 'end', count = countVar)
# if pos:
# 	review_frame_review_text.tag_add('time', pos, "{}+{}c".format(pos, countVar.get()))
# 	review_frame_review_text.tag_configure('time', font = font_content + ' bold')
# print pos

# print review_frame_review_text.index(pos + 'linestart')
# print review_frame_review_text_last_line
# if review_frame_review_text.index(pos + 'linestart') == review_frame_review_text_last_line:
# 	print False


while pos:
	pos = review_frame_review_text.search('Submitted on:', pos, stopindex = "end", count = countVar)
	if pos:
		review_frame_review_text.tag_add('bold', pos, "{}+{}c".format(pos, countVar.get()))
		pos = pos + '+1c'

pos = review_frame_review_text.search('Rating:', '1.0', stopindex = "end", count = countVar)
if pos:
	review_frame_review_text.tag_add('bold', pos, "{}+{}c".format(pos, countVar.get()))


review_frame_review_text.tag_configure('bold', font = font_content + ' bold')

	# if review_frame_review_text.index(pos + 'linestart') == review_frame_review_text_last_line:
	# 	flag = False


# pos = review_frame_review_text.search('Submitted on:', '1.0', stopindex="end", count=countVar)
# review_frame_review_text.tag_add('time', pos, "{}+{}c".format(pos, countVar.get()))
# review_frame_review_text.tag_configure('time', font = font_content + ' bold')
# pos = review_frame_review_text.search('Submitted on:', str(pos) + '+1c', stopindex="end", count=countVar)
# review_frame_review_text.tag_add('time', pos, "{}+{}c".format(pos, countVar.get()))
# review_frame_review_text.tag_configure('time', font = font_content + ' bold')
# print review_frame_review_text.index('end')

# pos = review_frame_review_text.search(':', '1.0', stopindex="end", count=countVar)
# print review_frame_review_text.index(pos + 'linestart')

master.mainloop()
# master.destroy()	# explicitly destroys the main window when the event loop is terminated; needed for some development envrionments