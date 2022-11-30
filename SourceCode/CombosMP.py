from tkinter import *
from PIL import ImageTk, Image
import json
from multiprocessing import *
from time import sleep
from random import shuffle
import sys
import os


def path(relative_path):
    """ Get the absolute path to the resource for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def ui():
    """Function containing UI microservice; one of four processes. Creates and launches GUI window and sends data back
    and forth to other microservices via text and JSON files. Contains various functions for button actions."""

    def title_screen():
        """Displays title screen"""
        bg.pack()
        title.place(relx=0.5, rely=0.2, anchor=CENTER)
        description.place(relx=0.5, rely=0.3, anchor=CENTER)
        proceed.place(relx=0.5, rely=0.775, anchor=N)

    def navigation():
        """Displays navigation screen when first entering app"""
        title.place_forget()
        description.place_forget()
        proceed.place_forget()
        create_combo.place(relx=0.5, rely=0.35, anchor=CENTER)
        view_combo.place(relx=0.5, rely=0.65, anchor=CENTER)

    def screen1(c):
        """Displays navigation screen"""
        create_combo.place(relx=0.5, rely=0.35, anchor=CENTER)
        view_combo.place(relx=0.5, rely=0.65, anchor=CENTER)
        c.clear()
        msg = 'process'
        file = open(path("pipe2.txt"), "w")  # Sends execution command to processing microservice
        file.write(msg)
        file.close()
        back.place_forget()
        combo_list.place_forget()
        jab.place_forget()
        cross.place_forget()
        left_hook.place_forget()
        right_hook.place_forget()
        left_uppercut.place_forget()
        right_uppercut.place_forget()
        pivot_left.place_forget()
        pivot_right.place_forget()
        custom.place_forget()
        custom_button.place_forget()
        save.place_forget()
        delete.place_forget()
        shuff.place_forget()
        del_all.place_forget()
        instructions.place_forget()

    def screen2():
        """Displays combo builder screen"""
        create_combo.place_forget()
        view_combo.place_forget()
        back.place(relx=0.0, rely=0.0, anchor=NW)
        jab.place(relx=0.42, rely=0.125, anchor=N)
        cross.place(relx=0.58, rely=0.125, anchor=N)
        left_hook.place(relx=0.42, rely=0.25, anchor=N)
        right_hook.place(relx=0.58, rely=0.25, anchor=N)
        left_uppercut.place(relx=0.42, rely=0.375, anchor=N)
        right_uppercut.place(relx=0.58, rely=0.375, anchor=N)
        pivot_left.place(relx=0.42, rely=0.5, anchor=N)
        pivot_right.place(relx=0.58, rely=0.5, anchor=N)
        custom.place(relx=0.46, rely=0.65, anchor=N)
        custom_button.place(relx=0.61, rely=0.65, anchor=N)
        save.place(relx=0.5, rely=0.8, anchor=N)
        delete.place(relx=0.88, rely=0.825, anchor=N)
        shuff.place(relx=0.88, rely=0.7, anchor=N)
        instructions.place(relx=0.5, rely=0.02, anchor=N)
        file = open(path("pipe3.txt"), "w")  # Prepares pipe3 for communication with shuffle microservice
        file.write('e')
        file.close()

    def screen3():
        """Displays view combos screen"""
        create_combo.place_forget()
        view_combo.place_forget()
        back.place(relx=0.0, rely=0.0, anchor=NW)
        del_all.place(relx=0.88, rely=0.875, anchor=N)
        output = open(path("display.txt"), "r")  # Pulls data appropriately processed by processing microservice
        output = output.read()
        combo_list.place(relx=0.5, rely=0.02, anchor=N)
        combo_list.config(text=output)

    def build_combo(c, x):
        """Appends action from corresponding user input to temporary combo data structure"""
        new = 'New combo: '
        c.append(x)
        for action in c:
            new += ' ' + str(action)
        instructions.config(text=new)  # Displays combo as it is being built

    def delete_action(c):
        """Pops most recent input from temporary combo data structure"""
        if len(c) > 0:
            c.pop()
            new = 'New combo: '
            for action in c:
                new += ' ' + str(action)
            instructions.config(text=new)  # Updates combo being built

    def delete_all():
        """Clears saved data and wipes view combos display"""
        open(path('database.json'), 'w').close()
        open(path("display.txt"), "w").close()
        combo_list.config(text='')
        msg = '-1'
        file = open(path("pipe2.txt"), "w")  # Sends command to delete combos data structure in database microservice
        file.write(msg)
        file.close()

    def save_combo(c):
        """Packages current combo and sends it to database microservice"""
        if len(c) > 0:
            instructions.config(text='Combo saved! Access your saved combos from the main menu.')
            data = {1: c}
            json_s = json.dumps(data)
            json_f = open(path("pipe.json"), "w")
            json_f.write(json_s)
            json_f.close()
            c.clear()

    def shuffle_combo(c):
        """Shuffles combo being built. Communicates with shuffle microservice via pipe3."""
        if len(c) > 0:
            f = open(path("pipe3.txt"), "r")
            command = f.readline().rstrip()
            f.close()
            if command == 'e':
                with open(path('pipe3.txt'), 'w') as w_file:  # Send combo to shuffle microservice
                    w_file.write('f\n')
                    w_file.writelines(f'{i}\n' for i in c)
                while True:  # Listens for response from shuffle microservice
                    sleep(0.05)
                    f = open(path("pipe3.txt"), "r")
                    command = f.readline().rstrip()
                    f.close()
                    if command == 'r':
                        break
                with open(path('pipe3.txt'), 'r') as r_file:
                    lst = [line.rstrip() for line in r_file]
                lst.remove('r')
                if lst:
                    for i in range(0, len(c)):  # Writes shuffled combo back into temporary combo data structure
                        c[i] = lst[i]
                else:
                    shuffle_combo(c)
                new = 'New combo: '
                for action in c:
                    new += ' ' + str(action)
                instructions.config(text=new)  # Updates combo being built display
                f = open(path("pipe3.txt"), "w")
                f.write('e')
                f.close()

    root = Tk()
    root.title('Boxing Combo Journal')
    root.iconbitmap(path("boxing_gloves.ico"))
    img = ImageTk.PhotoImage(Image.open(path("background.jpg")))
    bg = Label(image=img)
    root.attributes('-topmost', 1)
    window_width = 600
    window_height = 367
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.resizable(False, False)  # Prevents resizing of GUI window
    combo = []  # Initializes combo data structure to temporarily storing combos
    title = Label(root, text='Boxing Combo Builder', background='white', font=("Times New Roman", 25))
    description = Label(root, background='white',
                        text='Build and record combinations of boxing moves')
    instructions = Label(root, background='white', text='Click on an action to add it to your combo:')
    combo_list = Label(root, background='white', text='')
    create_combo = Button(root, text="CREATE NEW COMBO", padx=45, pady=45, command=screen2, bg="chartreuse4")
    view_combo = Button(root, text="VIEW COMBOS", padx=63, pady=48, command=lambda: screen3(), fg="white",
                        bg="blueviolet")
    jab = Button(root, text="Jab", padx=20, pady=10, command=lambda: build_combo(combo, 1), fg="white", bg="black")
    cross = Button(root, text="Cross", padx=15, pady=10, command=lambda: build_combo(combo, 2), fg="white", bg="black")
    left_hook = Button(root, text="Hook(L)", padx=15, pady=10, command=lambda: build_combo(combo, 3), fg="white",
                       bg="black")
    right_hook = Button(root, text="Hook(R)", padx=10, pady=10, command=lambda: build_combo(combo, 4), fg="white",
                        bg="black")
    left_uppercut = Button(root, text="Uppercut(L)", padx=10, pady=10, command=lambda: build_combo(combo, 5),
                           fg="white", bg="black")
    right_uppercut = Button(root, text="Uppercut(R)", padx=5, pady=10, command=lambda: build_combo(combo, 6),
                            fg="white", bg="black")
    pivot_left = Button(root, text="Pivot(L)", padx=20, pady=10, command=lambda: build_combo(combo, 'PL'), fg="white",
                        bg="black")
    pivot_right = Button(root, text="Pivot(R)", padx=15, pady=10, command=lambda: build_combo(combo, 'PR'), fg="white",
                         bg="black")
    custom_action = StringVar()
    custom_action.set("Custom action...")
    custom = Entry(root, width=20, borderwidth=5, textvariable=custom_action)
    custom_button = Button(root, text="Add", padx=5, command=lambda: build_combo(combo, custom.get()), fg="white",
                           bg="black")
    save = Button(root, text="Save combo", padx=55, pady=15, command=lambda: save_combo(combo), bg="deepskyblue2")
    delete = Button(root, text="Undo addition", command=lambda: delete_action(combo), padx=15, pady=5, bg='orange')
    shuff = Button(root, text="Shuffle", command=lambda: shuffle_combo(combo), padx=15, pady=5, bg='pink3')
    del_all = Button(root, text="Delete all combos", command=lambda: delete_all(), padx=15, pady=5, bg='orange')
    back = Button(root, text="Back", padx=20, pady=5, command=lambda: screen1(combo), bg='yellow')
    proceed = Button(root, text="Click here to begin", padx=30, pady=15, command=lambda: navigation(), bg="maroon4")

    title_screen()
    root.mainloop()  # Launches GUI loop


def database():
    """Function containing database microservice; one of four microservices. Processes and stores data sent from UI
    microservice"""

    def db_helper(cs, c):  # Adds combo to temporary database data structure
        cs["Combo " + str(len(cs) + 1)] = c

    combo_db = {}  # Initializes temporary database data structure
    while True:
        file_object = open(path("pipe.json"), "r")
        json_content = file_object.read()
        file_object.close()
        msg = open(path("pipe2.txt"), "r")
        if msg.read() == '-1':  # Clears temporary database data structure
            combo_db = {}
            msg.close()
            open(path('pipe2.txt'), 'w').close()
        if json_content:
            combo = json.loads(json_content)
            db_helper(combo_db, combo['1'])
            open(path('pipe.json'), 'w').close()
            json_s = json.dumps(combo_db)
            json_f = open(path("database.json"), "w")  # Writes into database file
            json_f.write(json_s)
            json_f.close()


def formatting():
    """Function containing formatting microservice; one of four microservices. Formats data from database for
    display in UI."""
    while True:
        msg = open(path("pipe2.txt"), "r")
        if msg.read() == 'process':
            f = open(path("database.json"), "r")
            combos = f.read()
            f.close()
            if combos:
                c = json.loads(combos)
                output = ''
                for key in c:
                    combs = ''
                    for act in c[key]:
                        combs += str(act) + ', '
                    combs = combs[:-2]
                    output += key + ': ' + combs + '\n'
                file = open(path("display.txt"), "w")
                file.write(output)
                file.close()
                open(path('pipe2.txt'), 'w').close()


def shuffles():
    """Function containing formatting microservice; one of four microservices. Formats data from database for
    display in UI."""
    while True:
        while True:  # Listens for appropriate command and data from UI microservice
            sleep(0.05)
            f = open(path("pipe3.txt"), "r")
            command = f.readline().rstrip()
            f.close()
            if command == 'f':
                break
        with open(path('pipe3.txt'), 'r') as r_file:
            r_file.readline().rstrip()
            lst = [line.rstrip() for line in r_file]
            shuffle(lst)
        with open(path('pipe3.txt'), 'w') as w_file:
            w_file.write('r\n')
            w_file.writelines(f'{i}\n' for i in lst)


if __name__ == '__main__':
    freeze_support()  # Allows multiprocessing module to work with .exe compiler
    p1 = Process(target=database)
    p1.start()
    p2 = Process(target=formatting)
    p2.start()
    p3 = Process(target=shuffles)
    p3.start()
    ui()
    p1.terminate()
    p2.terminate()
    p3.terminate()
