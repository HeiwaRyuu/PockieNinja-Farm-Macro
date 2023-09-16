import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pockie_ninja_automation import *
import sys
import threading
from PyQt5.QtWidgets import QApplication

STANDARD_WINDOW_SIZE="300x400"
MAIN_MENU_WINDOW_SIZE="200x150"


def set_style():
    style = ttk.Style()
    style.theme_use("vista")
    style.configure("TButton", padding=6, relief="flat", background="#ccc")


## CREATE A MAIN MENU WHERE IT CAN GO TO VALHALLA FARM OR SMELTING MOUNTAINS
class MainMenu(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Pockie Ninja Bot")
        self.master.geometry(MAIN_MENU_WINDOW_SIZE)
        self.master.resizable(False, False)
        self.grid(row=0, column=0, sticky="NESW")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()
        center(self.master)


    def create_widgets(self):
        self.valhalla_farm_button = ttk.Button(self, text="Valhalla Farm", command=self.on_valhalla_farm_button_click)
        self.valhalla_farm_button.grid(pady=10)

        self.smelting_mountains_button = ttk.Button(self, text="Smelting Mountains (lvl 1)", command=self.on_smelting_mountains_button_click)
        self.smelting_mountains_button.grid(pady=10)


    def on_valhalla_farm_button_click(self):
        self.master.destroy()
        root = tk.Tk()
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        app = ValhallaFarm(master=root)

        ## STYLE USING TKINTER TTK
        set_style()
        
        app.mainloop()


    def on_smelting_mountains_button_click(self):
        self.master.destroy()
        root = tk.Tk()
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        app = SmeltingMountains(master=root)

        ## STYLE USING TKINTER TTK
        set_style()
        
        app.mainloop()


class ValhallaFarm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Pockie Ninja Bot")
        self.master.geometry(STANDARD_WINDOW_SIZE)
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

        self.back_to_main_menu_button = ttk.Button(self, text="Back to Main Menu", command=self.back_to_main_menu)
        self.back_to_main_menu_button.grid(pady=15)


    def back_to_main_menu(self):
        self.master.destroy()
        root = tk.Tk()
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        app = MainMenu(master=root)

        ## STYLE USING TKINTER TTK
        style = ttk.Style()
        style.theme_use("vista")
        style.configure("TButton", padding=6, relief="flat", background="#ccc")
        
        app.mainloop()


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
            messagebox.showinfo("Info", "Checking Your Credentials...\nPlease wait for a moment!")
            check_credentials_bot = CheckLoginCredentials(username, password)
            is_invalid, case = check_credentials_bot.check_credentials()
            if is_invalid:
                if case == 'logedin':
                    messagebox.showwarning("Warning", "Invalid Credentials!\nThis account is already logged in!")
                if case == 'username':
                    messagebox.showwarning("Warning", "Invalid Credentials!\nUsername is incorrect!")
                if case == 'password':
                    messagebox.showwarning("Warning", "Invalid Credentials!\nPassword is incorrect!")
                return
            
            messagebox.showinfo("Info", "Valid Credentials!\nStarting Bot!")
            bot = PockieNinjaValhallaBot(username, password, int(dungeon_lvl), headless=headless)
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


class SmeltingMountains(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Pockie Ninja Bot")
        self.master.geometry(STANDARD_WINDOW_SIZE)
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
        options = ["Sunflower (lvl 2)", "Bee (lvl 4)", "Sushi (lvl 6)", "Scarlet (lvl 8)", "Warrior of Darkness (lvl 10)"]
        self.mob_option_label = ttk.Label(self, text="Choose Mob")
        self.mob_option_label.grid()

        mob_name_str_var = tk.StringVar()
        mob_name_str_var.set(options[0])
        self.mob_name_option_menu = tk.OptionMenu(self , mob_name_str_var , *options)
        self.mob_name_option_menu.grid(pady=10)

        ## ADD A CHECKBOX IF YOU WANT TO RUN THE BOT IN HEADLESS MODE
        self.headless_var = tk.IntVar()
        self.headless_checkbox = ttk.Checkbutton(self, text="Headless (No Browser)", variable=self.headless_var)
        self.headless_checkbox.grid(pady=10)

        self.start_button = ttk.Button(self, text="Start", command=self.on_start_button_click)
        self.start_button.grid(pady=15)
        
        self.stop_button = ttk.Button(self, text="Stop", command=self.stop_bot)
        self.stop_button.grid(pady=15)

        self.back_to_main_menu_button = ttk.Button(self, text="Back to Main Menu", command=self.back_to_main_menu)
        self.back_to_main_menu_button.grid(pady=15)


    def back_to_main_menu(self):
        self.master.destroy()
        root = tk.Tk()
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        app = MainMenu(master=root)

        ## STYLE USING TKINTER TTK
        set_style()
        
        app.mainloop()


    def on_start_button_click(self):
        new_thread = threading.Thread(target=self.start_bot, daemon=True)
        self.threads.append(new_thread)
        new_thread.start()


    def start_bot(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        mob_name = self.mob_name_option_menu.cget("text")
        headless = self.headless_var.get()

        if headless == 1:
            headless = True
        else:
            headless = False

        if username == "" or password == "" or mob_name == "":
            messagebox.showwarning("Warning", "Please fill all the fields")
        else:
            messagebox.showinfo("Info", "Checking Your Credentials...\nPlease wait for a moment!")
            check_credentials_bot = CheckLoginCredentials(username, password)
            is_invalid, case = check_credentials_bot.check_credentials()
            if is_invalid:
                if case == 'logedin':
                    messagebox.showwarning("Warning", "Invalid Credentials!\nThis account is already logged in!")
                if case == 'username':
                    messagebox.showwarning("Warning", "Invalid Credentials!\nUsername is incorrect!")
                if case == 'password':
                    messagebox.showwarning("Warning", "Invalid Credentials!\nPassword is incorrect!")
                return
            
            messagebox.showinfo("Info", "Valid Credentials!\nStarting Bot!")
            bot = PockieNinjaSmeltingMountainsBot(username, password, mob_name, headless=headless)
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
    app = MainMenu(master=root)

    ## STYLE USING TKINTER TTK
    style = ttk.Style()
    style.theme_use("vista")
    style.configure("TButton", padding=6, relief="flat", background="#ccc")
    
    app.mainloop()


if __name__ == "__main__":
    rebuild()