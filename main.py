import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pockie_ninja_automation import *
import sys
import threading
from PyQt5.QtWidgets import QApplication
    

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Pockie Ninja Bot")
        self.master.geometry("300x350")
        self.master.resizable(False, False)
        self.grid(row=0, column=0, sticky="NESW")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()
        self.bots = []
        self.threads = []
        self.bot = False
        center(self.master)


    def create_widgets(self):
        self.username_label = ttk.Label(self, text="Username")
        self.username_label.grid()
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid()

        self.password_label = ttk.Label(self, text="Password")
        self.password_label.grid()
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid()


        ## SET DUNGEON LEVEL AS A DROPDOWN MENU
        # Dropdown menu options
        options = ["11", "16"]
        self.dungeon_lvl_label = ttk.Label(self, text="Dungeon Level")
        self.dungeon_lvl_label.grid()

        dungeon_lvl_str_var = tk.StringVar()
        dungeon_lvl_str_var.set(options[0])
        self.dungeon_lvl_option_menu = tk.OptionMenu(self , dungeon_lvl_str_var , *options)
        self.dungeon_lvl_option_menu.grid(pady=10)

        ## ADD A CHECKBOX IF YOU WANT TO RUN THE BOT IN HEADLESS MODE
        self.headless_var = tk.IntVar()
        self.headless_checkbox = ttk.Checkbutton(self, text="Headless (No Browser)", variable=self.headless_var)
        self.headless_checkbox.grid(pady=10)

        self.start_button = ttk.Button(self, text="Start", command=self.on_start_button_click)
        self.start_button.grid(pady=15)
        
        self.stop_button = ttk.Button(self, text="Stop", command=self.stop_bot)
        self.stop_button.grid(pady=15)


    def on_start_button_click(self):
        new_thread = threading.Thread(target=self.start_bot, daemon=True)
        self.threads.append(new_thread)
        new_thread.start()


    def start_bot(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        dungeon_lvl = self.dungeon_lvl_option_menu.cget("text")
        headless = self.headless_var.get()

        if headless == 1:
            headless = True
        else:
            headless = False

        if username == "" or password == "" or dungeon_lvl == "":
            messagebox.showwarning("Warning", "Please fill all the fields")
        else:
            messagebox.showinfo("Info", "Starting Bot!")
            bot = PockieNinjaFarmBot(int(dungeon_lvl), username, password, headless=headless)
            self.bots.append(bot)
            bot.main_loop()
            
    
    def stop_bot(self):
        if self.bots:
            messagebox.showinfo("Info", "Stopping Bot(s)!")
            for bot in self.bots:
                bot.quit()
            self.bots = []
        else:
            messagebox.showwarning("Warning", "No Bot is not running!")


def center(toplevel):
    toplevel.update_idletasks()

    # Tkinter way to find the screen resolution
    # screen_width = toplevel.winfo_screenwidth()
    # screen_height = toplevel.winfo_screenheight()

    # PyQt way to find the screen resolution
    app = QApplication([])
    screen_width = app.desktop().screenGeometry().width()
    screen_height = app.desktop().screenGeometry().height()
    app.quit()

    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2

    toplevel.geometry("+%d+%d" % (x, y))


def rebuild():
    root = tk.Tk()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    app = Application(master=root)

    ## STYLE USING TKINTER TTK
    style = ttk.Style()
    style.theme_use("vista")
    style.configure("TButton", padding=6, relief="flat", background="#ccc")
    
    app.mainloop()


if __name__ == "__main__":
    rebuild()