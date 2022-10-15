from tkinter import *
import json
import subprocess
# import os


def root_window():
    root = Tk()
    root.title('Boxing Combo Journal')
    root.iconbitmap("boxing_gloves.ico")
    root.attributes('-topmost', 1)
    window_width = 600
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    def screen_default():
        create_combo.place(relx=0.5, rely=0.3, anchor=CENTER)
        view_combo.place(relx=0.5, rely=0.6, anchor=CENTER)

    def screen1(c):
        create_combo.place(relx=0.5, rely=0.3, anchor=CENTER)
        view_combo.place(relx=0.5, rely=0.6, anchor=CENTER)
        c.clear()
        msg = 'process'
        file = open("pipe2.txt", "w")
        file.write(msg)
        file.close()
        instructions.config(text='Click a button to add its corresponding action to your combo:')
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
        del_all.place_forget()
        instructions.place_forget()

    def screen2():
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
        instructions.place(relx=0.5, rely=0.02, anchor=N)

    def screen3():
        create_combo.place_forget()
        view_combo.place_forget()
        back.place(relx=0.0, rely=0.0, anchor=NW)
        del_all.place(relx=0.88, rely=0.875, anchor=N)
        output = open("display.txt", "r")
        output = output.read()
        combo_list.place(relx=0.5, rely=0.02, anchor=N)
        combo_list.config(text=output)

    def build_combo(c, x):
        new = 'New combo: '
        c.append(x)
        for action in c:
            new += ' ' + str(action)
        instructions.config(text=new)

    def delete_action(c):
        if len(c) > 0:
            c.pop()
            new = 'New combo: '
            for action in c:
                new += ' ' + str(action)
            instructions.config(text=new)

    def delete_all():
        open('database.json', 'w').close()
        open("display.txt", "w").close()
        combo_list.config(text='')
        msg = '-1'
        file = open("pipe2.txt", "w")
        file.write(msg)
        file.close()

    def save_combo(c):
        if len(c) > 0:
            instructions.config(text='Combo saved!')
            data = {1: c}
            json_s = json.dumps(data)
            json_f = open("pipe.json", "w")
            json_f.write(json_s)
            json_f.close()
            c.clear()

    combo = []
    instructions = Label(root, text='Click a button to add its corresponding action to your combo:')
    combo_list = Label(root, text='')
    create_combo = Button(root, text="CREATE NEW COMBO", padx=45, pady=45, command=screen2, bg="chartreuse4")
    view_combo = Button(root, text="VIEW COMBOS", padx=63, pady=48, command=lambda: screen3(), fg="white", bg="blueviolet")
    jab = Button(root, text="Jab", padx=20, pady=10, command=lambda: build_combo(combo, 1), fg="white", bg="black")
    cross = Button(root, text="Cross", padx=15, pady=10, command=lambda: build_combo(combo, 2), fg="white", bg="black")
    left_hook = Button(root, text="Hook(L)", padx=15, pady=10, command=lambda: build_combo(combo, 3), fg="white", bg="black")
    right_hook = Button(root, text="Hook(R)", padx=10, pady=10, command=lambda: build_combo(combo, 4), fg="white", bg="black")
    left_uppercut = Button(root, text="Uppercut(L)", padx=10, pady=10, command=lambda: build_combo(combo, 5), fg="white", bg="black")
    right_uppercut = Button(root, text="Uppercut(R)", padx=5, pady=10, command=lambda: build_combo(combo, 6), fg="white", bg="black")
    pivot_left = Button(root, text="Pivot(L)", padx=20, pady=10, command=lambda: build_combo(combo, 'PL'), fg="white", bg="black")
    pivot_right = Button(root, text="Pivot(R)", padx=15, pady=10, command=lambda: build_combo(combo, 'PR'), fg="white", bg="black")
    custom_action = StringVar()
    custom_action.set("Custom action...")
    custom = Entry(root, width=20, borderwidth=5, textvariable=custom_action)
    custom_button = Button(root, text="Add", padx=5, command=lambda: build_combo(combo, custom.get()), fg="white", bg="black")
    save = Button(root, text="Save combo", padx=55, pady=15, command=lambda: save_combo(combo), bg="lime")
    delete = Button(root, text="Undo addition", command=lambda: delete_action(combo), padx=15, pady=5, bg='red')
    del_all = Button(root, text="Delete all combos", command=lambda: delete_all(), padx=15, pady=5, bg='red')
    back = Button(root, text="Back", padx=20, pady=5, command=lambda: screen1(combo))

    screen_default()
    root.mainloop()


# os.system("start /b ComboDB.py")
subprocess.Popen("python ComboProcessing.py &", close_fds=True)
subprocess.Popen("python ComboDB.py &", close_fds=True)
root_window()
open('database.json', 'w').close()




