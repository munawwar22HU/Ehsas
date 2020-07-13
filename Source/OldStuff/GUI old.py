from RTreeOperations import *
from tkinter import *
from tkinter import ttk
import tkinter.font as font
from PIL import ImageTk, Image
import xlrd


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
    Grocery = PhotoImage(file="Images/ResizeGeneral Store.png")
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

    Fruit = PhotoImage(file="Images/resizeFruits.png")
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
    global tree
    Select = Toplevel(Menu)  # new window for selection page
    Select.title("Selection")
    Select.configure(bg="#f1f3a6")
    center_window(Select, 747, 442)

    SearchLabel = Label(Select, text="Area :", bg="#f1f3a6",  # by area label
                        fg="black", font="Verdana 10 bold")
    SearchLabel.place(x=24, y=28, height=40, width=75)

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

    global AreaChoosen
    AreaChoosen = ttk.Combobox(Select, textvariable=n, state="readonly")

   
    AreaChoosen['values'] = tree.getAreas()
    AreaChoosen.place(x=110, y=38, height=20, width=190)
    AreaChoosen.current()
    AreaChoosen.bind("<<ComboboxSelected>>", callback)


    NearMe = Radiobutton(Select, text="Near Me", variable=v, value=2, bg="#f1f3a6",
                         fg="black")
    NearMe.place(x=350, y=38, width=90, height=20)

    table = Frame(Select, width=690, height=340,
                  background="#f1f3a6", bd=3, relief=SOLID)
    table.place(x=30, y=80)

    global forcall
    forcall = entity
    data(Select, entity)
    Select.mainloop()

def callback(eventObject):
    for butons in filter(lambda w: isinstance(w, Button), Select.winfo_children()):
        butons.destroy()
    data(Select, forcall)




def data(Select, entity):
    print(entity)
    print(AreaChoosen['values'][AreaChoosen.current()])




Menu = Tk()
Menu.title("Ehsaas")
Menu.configure(bg="#ffffff")
tree = TreeOp("Data/Store Data.csv")
Mainpage()


# data1 = Button(Select, width=200, height=40, bg="#f1f3a6", text=" Awami Markaz \n Imtiaz \n 8 AM - 5PM",
#                anchor=W, justify=LEFT, compound=LEFT, bd=2, relief=RIDGE)
# data1.config(image=Veg, compound=LEFT)
# data1.place(x=50, y=100)

# data2 = Button(Select, width=200, height=40, bg="#f1f3a6", text=" Bahadurabad \n Imtiaz \n 8 AM - 5PM",
#                anchor=W, justify=LEFT, compound=LEFT, bd=2, relief=RIDGE)
# data2.config(image=Veg, compound=LEFT)
# data2.place(x=50, y=160)

# data3 = Button(Select, width=200, height=40, bg="#f1f3a6", text=" Baloch Colony \n Bin Ahmed \n 8 AM - 5PM",
#                anchor=W, justify=LEFT, compound=LEFT, bd=2, relief=RIDGE)
# data3.config(image=Veg, compound=LEFT)
# data3.place(x=50, y=220)

# data4 = Button(Select, width=200, height=40, bg="#f1f3a6", text=" Clifton \n Shop n Save \n 8 AM - 5PM",
#                anchor=W, justify=LEFT, compound=LEFT, bd=2, relief=RIDGE)
# data4.config(image=Veg, compound=LEFT)
# data4.place(x=50, y=280)

# data5 = Button(Select, width=200, height=50, bg="#f1f3a6", text=" Defence \n General store and Pharmacies \n near KFC Rahat \n 8 AM - 5PM",
#                anchor=W, justify=LEFT, compound=LEFT, bd=2, relief=RIDGE)
# data5.config(image=Veg, compound=LEFT)
# data5.place(x=50, y=340)

# data6 = Button(Select, width=200, height=40, bg="#f1f3a6", text=" Defence \n Imtiaz \n 8 AM - 5PM",
#                anchor=W, justify=LEFT, compound=LEFT, bd=2, relief=RIDGE)
# data6.config(image=Veg, compound=LEFT)
# data6.place(x=270, y=100)

# data7 = Button(Select, width=200, height=40, bg="#f1f3a6", text=" Gulshan-e-Iqbal \n Imtiaz \n 8 AM - 5PM",
#                anchor=W, justify=LEFT, compound=LEFT, bd=2, relief=RIDGE)
# data7.config(image=Veg, compound=LEFT)
# data7.place(x=270, y=160)

# data8 = Button(Select, width=200, height=40, bg="#f1f3a6", text=" Nazimabad \n Imtiaz \n 8 AM - 5PM",
#                anchor=W, justify=LEFT, compound=LEFT, bd=2, relief=RIDGE)
# data8.config(image=Veg, compound=LEFT)
# data8.place(x=270, y=220)

# data9 = Button(Select, width=200, height=40, bg="#f1f3a6", text=" Orangi Town \n Bilal General Store \n 8 AM - 5PM",
#                anchor=W, justify=LEFT, compound=LEFT, bd=2, relief=RIDGE)
# data9.config(image=Veg, compound=LEFT)
# data9.place(x=270, y=280)

# data10 = Button(Select, width=200, height=40, bg="#f1f3a6", text=" Safoora Chowrangi \n Al Jadeed \n 8 AM - 5PM",
#                 anchor=W, justify=LEFT, compound=LEFT, bd=2, relief=RIDGE)
# data10.config(image=Veg, compound=LEFT)
# data10.place(x=270, y=340)

# data11 = Button(Select, width=200, height=40, bg="#f1f3a6", text=" Safoora Chowrangi \n Bin Hashim \n 8 AM - 5PM",
#                 anchor=W, justify=LEFT, compound=LEFT, bd=2, relief=RIDGE)
# data11.config(image=Veg, compound=LEFT)
# data11.place(x=490, y=100)

# data12 = Button(Select, width=200, height=40, bg="#f1f3a6", text=" Safoora Chowrangi \n Muslim SuperMarket \n 8 AM - 5PM",
#                 anchor=W, justify=LEFT, compound=LEFT, bd=2, relief=RIDGE)
# data12.config(image=Veg, compound=LEFT)
# data12.place(x=490, y=160)
