import sys
if sys.version_info[0] < 3:
	import Tkinter as tk
else:
	import tkinter as tk


master = tk.Tk()

review_frame = tk.Frame(master, bd = 2, relief = tk.SUNKEN)
review_frame.grid_rowconfigure(0, weight = 1)	# configure row index of a grid
review_frame.grid_columnconfigure(0, weight = 1)

# vertical scrollbar
# vscrollbar = tk.Scrollbar(master)
# vscrollbar.pack(side = tk.RIGHT, fill = tk.Y)
vscrollbar = tk.Scrollbar(review_frame)
vscrollbar.grid(row = 0, column = 1, sticky = tk.N + tk.S)

# # horizontal scrollbar
# hscrollbar = tk.Scrollbar(master, orient = tk.HORIZONTAL)
# hscrollbar.pack(side = tk.BOTTOM, fill = tk.X)

# wrap: WORD, CHAR, NONE
# review_text = tk.Text(master, wrap = tk.WORD, yscrollcommand = vscrollbar.set)
# review_text.pack()
# # Alternatively for wrap = NONE
# review_text = tk.Text(master, wrap = tk.NONE, xscrollcommand = hscrollbar.set, yscrollcommand = vscrollbar.set)
# review_text.pack()
review_text = tk.Text(review_frame, wrap = tk.NONE, bd = 0, yscrollcommand = vscrollbar.set)
review_text.grid(row = 0, column = 0, sticky = tk.N+tk.S+tk.E+tk.W)

review_text.insert(tk.END, 'Hello World!\nYeah')
# hscrollbar.config(command = review_text.xview)
vscrollbar.config(command = review_text.yview)
review_frame.pack()

tk.mainloop()