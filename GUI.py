import json
import requests
import functools
import webbrowser
import googlemaps
import geocoder
import folium
import numpy as np
from RTreeOperations import *
from tkinter import *
from tkinter import ttk
import tkinter.font as font
from PIL import ImageTk, Image
import functools


def center_window(root, w=300, h=200):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


def Mainpage():  # first page
    global Menu
    center_window(Menu, 747, 442)
    load = Image.open(  # rendering image on the first window
        "Images/CoverPage.png")
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render
    img.place(x=0, y=0)
    Nextbutton = ImageTk.PhotoImage(
        Image.open("Images/nextresize.png"))  # Next button
    Next = Button(Menu, image=Nextbutton, bd=0, bg="#ffffff",
                  width=170, height=50, activebackground="#ffffff", command=lambda: Menupage(Next)).place(x=570, y=20)
    Menu.mainloop()


def Menupage(buttons):

    global Menu
    # rendering image for menupage on the same window
    Menu.configure(bg="white")
    background = Image.open(
        "Images/MenuPage.png")
    img = PhotoImage(file="Images/MenuPage.png")
    render = Label(image=img)
    render.image = img
    render.place(x=-2, y=0)  # 71c498

    # buttons for different types
    button = Button(Menu, text="General Store", compound=TOP, bd=0,
                    bg='#1b82ab', command=lambda: SelectionPage("General Store"), activebackground='#1b82ab', fg="white")
    Grocery = PhotoImage(file="Images\ResizeGeneral Store.png")
    button.config(image=Grocery, highlightbackground="black")
    button.place(x=70, y=240)
    myFont = font.Font(family='Comic Sans MS', size=8)
    button['font'] = myFont

    button1 = Button(Menu, text="Pharmacy", compound=TOP,
                     bd=0,
                     bg='#1b82ab', command=lambda: SelectionPage("Pharmacy"), activebackground='#1b82ab', fg="white")
    Pharmacy = PhotoImage(file="Images/ResizePharmacy.png")
    button1.config(image=Pharmacy)
    button1.place(x=118, y=90)

    button2 = Button(Menu, text="Milk", compound=TOP, bd=0,
                     bg='#1b82ab', command=lambda: SelectionPage("Milk"), activebackground='#1b82ab', fg="white")
    Milk = PhotoImage(file="Images/ResizeMilk.png")
    button2.config(image=Milk)
    button2.place(x=240, y=10)

    button3 = Button(Menu, text="Vegetables", compound=TOP,
                     bd=0,
                     bg='#1b82ab', command=lambda: SelectionPage("Vegetables"), activebackground='#1b82ab', fg="white")
    Veg = PhotoImage(file="Images/ResizeVegetables.png")
    button3.config(image=Veg)
    button3.place(x=390, y=10)

    button4 = Button(Menu, text="Fruits", compound=TOP,
                     bd=0,
                     bg='#1b82ab', command=lambda: SelectionPage("Fruits"), activebackground='#1b82ab', fg="white")

    Fruit = PhotoImage(file="Images/ResizeFruits.png")
    button4.config(image=Fruit)
    button4.place(x=520, y=90)

    button5 = Button(Menu, text="Meat", compound=TOP, bd=0,
                     bg='#1b82ab', command=lambda: SelectionPage("Meat"), activebackground='#1b82ab', fg="white")
    Meat = PhotoImage(file="Images/ResizeMeat.png")
    button5.config(image=Meat)
    button5.place(x=550, y=240)

    Menu.mainloop()


def SelectionPage(entity):

    v = IntVar()
    n = StringVar()

    global Menu
    global Select
    global Tree
    Select = Toplevel(Menu)  # new window for selection page
    Select.title("Selection")
    Select.configure(bg="#f1f3a6")
    center_window(Select, 747, 442)

    SearchLabel = Label(Select, text="Area :", bg="#f1f3a6",  # by area label
                        fg="black", font="Verdana 10 bold")
    SearchLabel.place(x=110, y=28, height=40, width=75)

    global AreaChoosen
    AreaChoosen = ttk.Combobox(Select, textvariable=n, state="readonly")

    AreaChoosen['values'] = tree.getAreas()
    AreaChoosen.place(x=196, y=38, height=20, width=190)
    AreaChoosen.current()
    AreaChoosen.bind("<<ComboboxSelected>>", callback)

    table = Frame(Select, width=522, height=315,
                  background="#f1f3a6", bd=3, relief=SOLID)
    table.place(x=113, y=85)

    global forcall
    forcall = entity
    data(Select, entity)
    Select.mainloop()


def callback(eventObject):
    for widgets in filter(lambda w: isinstance(w, Canvas), Select.winfo_children()):
        widgets.destroy()
    for widgets in filter(lambda w: isinstance(w, Scrollbar), Select.winfo_children()):
        widgets.destroy()

    data(Select, forcall)


def MapClick(i, latt, longi):
    global counter

    global my_map1
    my_map1 = folium.Map(location=[24.8607, 67.0011],
                         zoom_start=10)
    # my_map1 = folium.Map(location=[24.8607, 67.0011],
    #                  zoom_start=12)
    gmaps = googlemaps.Client(key='AIzaSyDtXUOF8QiIB___KLzmSlPZJhHjh81Wrvw')
    lat = gmaps.geolocate()["location"]["lat"]
    lng = gmaps.geolocate()["location"]["lng"]
    folium.Marker([round(lat, 2), round(lng, 2)],
                  popup='Source').add_to(my_map1)
    longi = float(i.Longitude)
    latt = float(i.Latitude)
    print(latt, longi)

    folium.Marker([latt, longi], popup=str(i.Name)).add_to(my_map1)
    coordinates = []
    coordinates.append([latt, longi])
    coordinates.append([round(lat, 2), round(lng, 2)])
    my_PolyLine = folium.PolyLine(locations=coordinates, weight=5)
    my_map1.add_child(my_PolyLine)
    my_map1.save("my_map.html")
    webbrowser.get(
        "C:/Users/aiman junaid/AppData/Local/Google/Chrome/Application/chrome.exe %s").open_new_tab('my_map.html')
    my_PolyLine.render()


def data(Select, entity):
    global counter
    global tree
    global my_map1

    canvas = Canvas(Select, height=300, width=510, bg="#f1f3a6", bd=0)
    frame = Frame(canvas, bg="#f1f3a6", bd=0)

    myscrollbar = Scrollbar(Select, orient="vertical",
                            command=canvas.yview)
    canvas.create_window((0, 0), window=frame, anchor='nw')

    x1 = 50
    y1 = 100
    j = 0

    ima1 = PhotoImage(file="Images/selection"+str(entity)+".png")

    if AreaChoosen.current() == - 1:
        result = tree.Search(
            entity, AreaChoosen['values'][AreaChoosen.current()], False)
        for i in result:

            if y1 > 340 and j == 5:
                y1 = 100
                x1 = x1 + 220
                j = 0

            data = Button(frame, width=500, height=42, bg="#f1f3a6", text=(i.getData() +
                                                                           "  " + " \n  8 AM - 5PM"),
                          anchor=W, justify=LEFT, compound=LEFT, bd=2, relief=RIDGE, command=lambda: MapClick(i, i.Latitude, i.Longitude))

            data.config(image=ima1, compound=LEFT)
            data.pack()
            y1 = y1 + 60
            j += 1

    else:
        result = tree.Search(
            entity, AreaChoosen['values'][AreaChoosen.current()], True)
        for i in result:

            if y1 > 340 and j == 5:
                y1 = 100
                x1 = x1 + 220
                j = 0

            data1 = Button(frame, width=500, height=42, bg="#f1f3a6", text=(i.getData() +
                                                                            "  " + " \n  8 AM - 5PM"),
                           anchor=W, justify=LEFT, compound=LEFT, bd=2, relief=RIDGE, command=lambda: MapClick(i, i.Latitude, i.Longitude))

            data1.config(image=ima1, compound=LEFT)

            data1.pack()
            y1 = y1 + 60
            j += 1

    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'),
                     yscrollcommand=myscrollbar.set)

    canvas.place(relx=0.5, rely=0.55, anchor=CENTER)
    myscrollbar.pack(fill='y', side='right')
    Select.mainloop()


tree = TreeOp("Data/Store Data.csv")

counter = 0

Menu = Tk()
Menu.title("Ehsaas")
Menu.configure(bg="#ffffff")
combostyle = ttk.Style()
combostyle.theme_create('combostyle', parent="classic",
                        settings={'TCombobox':
                                  {'configure':
                                   {
                                       'fieldbackground': 'white',
                                       "selectbackground": "white",
                                       "selectforeground": "black",
                                       'background': 'black',
                                       "highlightcolor": "red"
                                   }}}
                        )
combostyle.theme_use('combostyle')
Mainpage()
