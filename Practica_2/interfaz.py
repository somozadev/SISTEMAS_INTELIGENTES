import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3



# Creating tkinter window
window = tk.Tk()
window.title('Mi Recomendador')
window.geometry('730x700')


# label text for title
ttk.Label(window, text = "RECOMENDACIONES",
        background = 'green', font = ("Times New Roman", 15, UNDERLINE)).grid(column = 0, row = 1, 
        padx =10, pady = 10)


# label usuario
ttk.Label(window, text = "Selecciona un usuario: ",
		font = ("Times New Roman", 15)).grid(column = 0,
		row = 2, padx =10, pady = 10)

# Combobox IDusuario
n = tk.StringVar()
idchoosen = ttk.Combobox(window, width = 10, textvariable = n)


# label items del ranking 
ttk.Label(window, text = "Items del ranking: ",
		font = ("Times New Roman", 15)).grid(column = 0,
		row = 3, padx =20, pady = 10)

# input ranking 
e1 = ttk.Entry(window, width = 5)
e1.grid(row = 3, column = 1)

# label umbral de similitud 
ttk.Label(window, text = "Unbral de similitud: ",
		font = ("Times New Roman", 15)).grid(column = 2,
		row = 3, padx =20, pady = 20)


# input similitud 
e2 = ttk.Entry(window, width = 5)
e2.grid(row = 3, column = 3)


# button recomendar 
tk.Button(window, text='Recomendar').grid(row=2, column=4, sticky=tk.W, pady=4)

# label ranking
ttk.Label(window, text = "Ranking: ",
		font = ("Times New Roman", 15)).grid(column = 2,
		row = 4, padx =10, pady = 30)


# label usuario2
ttk.Label(window, text = "Selecciona un usuario: ",
		font = ("Times New Roman", 15)).grid(column = 0,
		row = 5, padx =10, pady = 10)

# Combobox IDusuario2
n = tk.StringVar()
id2choosen = ttk.Combobox(window, width = 10, textvariable = n)


# Label Selecciona Pelicula
ttk.Label(window, text = "Selecciona una pelicu: ",
		font = ("Times New Roman", 15)).grid(column = 0,
		row = 6, padx =10, pady = 10)

# Combobox Pelicula
n = tk.StringVar()
peliculachoosen = ttk.Combobox(window, width = 10, textvariable = n)

# button predecir 
tk.Button(window, text='Predecir').grid(row=5, column=4)


# List ID usuarios combobox
idchoosen['values'] = ()

idchoosen.grid(column = 1, row = 2)
idchoosen.current()


# List ID2 usuarios combobox
id2choosen['values'] = ()

id2choosen.grid(column = 1, row = 5)
id2choosen.current()


# List ID2 usuarios combobox
peliculachoosen['values'] = ()

peliculachoosen.grid(column = 1, row = 6)
peliculachoosen.current()



window.mainloop()












