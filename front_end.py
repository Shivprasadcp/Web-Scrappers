import tkinter as tk
from tkinter import ttk
import Amazon
import Flipkart
import IMDB
import Myntra
import TripAdvisor
from selenium import webdriver


def submit():
    text = textbox.get()
    option = dropdown.get()
    if option == 'Amazon':
        obj =Amazon.Amazon()
        z = obj.extract(text)
        print(z)
        z.to_csv('Amazon.csv', index=False)
        

    elif option == 'Flipkart':
        obj =Flipkart.Flipkart()
        z = obj.extract(text)
        print(z)
        z.to_csv('Flipkart.csv', index=False)

    elif option =='Myntra':
        obj =Myntra.Myntra()
        z = obj.extract(text)
        print(z)
        z.to_csv('Myntra.csv', index=False)

    elif option =='IMDB':
        obj =IMDB.Imdb()
        z = obj.extract(text)
        print(z)
        z.to_csv('IMDB.csv', index=False)

    else:
        obj =TripAdvisor.TripAdvisor()
        z = obj.extract(text)
        print(z)
        z.to_csv('TripAdvisor.csv', index=False)


    window.destroy()

window = tk.Tk()
window.title("Automated Webscraper")
window.configure(bg="#212A3E")

# Create a label for the dropdown and pack it into the window
dropdown_label = tk.Label(text="Choose the Website:", font=("Helvetica", 16), bg="#B0A4A4")
dropdown_label.pack(pady=5, padx=10)

# Create a list of options for the dropdown
options = ["Amazon", "Flipkart", "Myntra","IMDB","Trip Advisor"]

# Create the dropdown and pack it into the window
dropdown = ttk.Combobox(values=options, width=25, font=("Helvetica", 12), style="TCombobox", background="#fff")
dropdown.pack(pady=(5, 20), padx=10)

# Create a label and pack it into the window
label = tk.Label(text="Enter the URL:", font=("Helvetica", 16), bg="#B0A4A4")
label.pack(pady=(20, 5), padx=10)

# Create a textbox and pack it into the window
textbox = tk.Entry(width=50, font=("Helvetica", 12), borderwidth=3, relief="sunken", bg="#fff", fg="#000")
textbox.pack(pady=5, padx=10)

# Create a submit button and pack it into the window
submit_button = tk.Button(text="Submit", font=("Helvetica", 16), command=submit, borderwidth=3, relief="raised", bg="#4CAF50", fg="#fff")
submit_button.pack(pady=10, padx=10)

window.mainloop()
