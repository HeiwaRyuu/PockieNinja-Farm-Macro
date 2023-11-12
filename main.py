import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pockie_ninja_automation import *
import sys
import threading
from PyQt5.QtWidgets import QApplication
from src import *

STANDARD_WINDOW_SIZE="300x475"
STANDARD_AREA_FARM_WINDOW_SIZE ="300x475"
MAIN_MENU_WINDOW_SIZE="200x150"


def set_style():
    style = ttk.Style()
    style.theme_use("vista")
    style.configure("TButton", padding=6, relief="flat", background="#ccc")


## CREATE A MAIN MENU WHERE IT CAN GO TO VALHALLA FARM OR REGULAR AREA FARM
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

        self.regular_area_button = ttk.Button(self, text="Regular Area Farm", command=self.on_regular_area_button_click)
        self.regular_area_button.grid(pady=25)


    def on_valhalla_farm_button_click(self):
        self.master.destroy()
        root = tk.Tk()
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        app = ValhallaFarm(master=root)

        ## STYLE USING TKINTER TTK
        set_style()
        
        app.mainloop()


    def on_regular_area_button_click(self):
        self.master.destroy()
        root = tk.Tk()
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        app = StandardAreaFarm(master=root)

        ## STYLE USING TKINTER TTK
        set_style()
        
        app.mainloop()


class ValhallaFarm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Pockie Ninja Bot - Valhalla Farm")
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

    
    def update_difficulties(self, *args):
        # Reset var and delete all old options
        self.difficulty_str_var.set('')
        self.difficulty_option_menu['menu'].delete(0, 'end')

        if self.dungeon_lvl_option_menu.cget("text") == VALHALLA_LVL_11:
            difficulty_options = [SOLO_VALHALLA_DIFFICULTY]
        else:
            difficulty_options = [NORMAL_VALHALLA_DIFFICULTY, SOLO_VALHALLA_DIFFICULTY]

        # Insert list of new options (tk._setit hooks them up to var)
        for option in difficulty_options:
            self.difficulty_option_menu['menu'].add_command(label=option, command=tk._setit(self.difficulty_str_var, option))
        self.difficulty_str_var.set(difficulty_options[0])


    def create_widgets(self):
        self.username_label = ttk.Label(self, text="Username")
        self.username_label.grid()
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid()

        self.password_label = ttk.Label(self, text="Password")
        self.password_label.grid()
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid()


        ## SET DUNGEON LEVEL AS A OPTION MENU
        self.dungeon_level_options = [VALHALLA_LVL_11, VALHALLA_LVL_16]
        self.dungeon_lvl_label = ttk.Label(self, text="Dungeon Level")
        self.dungeon_lvl_label.grid()

        self.dungeon_lvl_str_var = tk.StringVar()
        self.dungeon_lvl_str_var.set(self.dungeon_level_options[0])
        self.dungeon_lvl_option_menu = tk.OptionMenu(self , self.dungeon_lvl_str_var , *self.dungeon_level_options, command=self.update_difficulties)
        self.dungeon_lvl_option_menu.grid(pady=10)


        ## DIFFICULTY OPTION MENU
        self.difficulty_options = [SOLO_VALHALLA_DIFFICULTY]
        self.difficulty_option_label = ttk.Label(self, text="Choose difficulty")
        self.difficulty_option_label.grid()

        self.difficulty_str_var = tk.StringVar()
        self.difficulty_str_var.set(self.difficulty_options[0])
        self.difficulty_option_menu = tk.OptionMenu(self , self.difficulty_str_var , *self.difficulty_options)
        self.difficulty_option_menu.grid(pady=10)


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
        difficulty = self.difficulty_option_menu.cget("text")
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
            check_exit_success = self.create_and_run_bot(username, password, dungeon_lvl, difficulty, headless)
            while not check_exit_success:
                check_exit_success = self.create_and_run_bot(username, password, dungeon_lvl, difficulty, headless)
    

    def create_and_run_bot(self, username, password, dungeon_lvl, difficulty, headless):
        bot = PockieNinjaValhallaBot(username, password, int(dungeon_lvl), difficulty, headless=headless)
        self.bots.append(bot)
        check_exit_success = bot.main_loop()
        return check_exit_success
    
    
    def stop_bot(self):
        if self.bots:
            messagebox.showinfo("Info", "Stopping Bot(s)!")
            for bot in self.bots:
                bot.quit()
            self.bots = []
        else:
            messagebox.showwarning("Warning", "No Bot is not running!")


class StandardAreaFarm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Pockie Ninja Bot - Mob Farm")
        self.master.geometry(STANDARD_AREA_FARM_WINDOW_SIZE)
        self.master.resizable(False, False)
        self.grid(row=0, column=0, sticky="NESW")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()
        self.bots = []
        self.threads = []
        self.bot = False
        center(self.master)


    def populate_area_names(self):
        area_names = [SMELTING_MOUNTAINS_AREA_NAME, EVENTIDE_BARRENS_AREA_NAME]
        return area_names


    def populate_mob_names(self):
        options = [SUNFLOWER_NAME, BEE_NAME, SUSHI_NAME, SCARLET_NAME, WARRIOR_OF_DARKNESS_NAME]
        return options
    
    
    def update_mob_names(self, *args):
        # Reset var and delete all old options
        self.mob_name_str_var.set('')
        self.mob_name_option_menu['menu'].delete(0, 'end')

        area_name = self.area_name_option_menu.cget("text")

        if area_name == SMELTING_MOUNTAINS_AREA_NAME:
            options = [SUNFLOWER_NAME, BEE_NAME, SUSHI_NAME, SCARLET_NAME, WARRIOR_OF_DARKNESS_NAME]
        elif area_name == EVENTIDE_BARRENS_AREA_NAME:
            options = [POTATO_NAME, MONKEY_NAME, MEAL_NAME, KAPPA_NAME, BULLHEAD_NAME]

        # Insert list of new options (tk._setit hooks them up to var)
        for option in options:
            self.mob_name_option_menu['menu'].add_command(label=option, command=tk._setit(self.mob_name_str_var, option))
        self.mob_name_str_var.set(options[0])


    def create_widgets(self):
        self.username_label = ttk.Label(self, text="Username")
        self.username_label.grid()
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid()

        self.password_label = ttk.Label(self, text="Password")
        self.password_label.grid()
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid()


        ## AREA NAMES DROPDOWN MENU
        area_options = self.populate_area_names()
        self.area_option_label = ttk.Label(self, text="Choose Area")
        self.area_option_label.grid()

        self.area_name_str_var = tk.StringVar()
        self.area_name_str_var.set(area_options[0])
        self.area_name_option_menu = tk.OptionMenu(self , self.area_name_str_var , *area_options, command=self.update_mob_names)
        self.area_name_option_menu.grid(pady=10)


        ## MOB NAMES DROPDOWN MENU
        mobs_options = self.populate_mob_names()
        self.mob_option_label = ttk.Label(self, text="Choose Mob")
        self.mob_option_label.grid()

        self.mob_name_str_var = tk.StringVar()
        self.mob_name_str_var.set(mobs_options[0])
        self.mob_name_option_menu = tk.OptionMenu(self , self.mob_name_str_var , *mobs_options)
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
        area_name = self.area_name_option_menu.cget("text")
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
            check_exit_success = self.create_and_run_bot(username, password, area_name, mob_name, headless)
            while not check_exit_success:
                check_exit_success = self.create_and_run_bot(username, password, area_name, mob_name, headless)


    def create_and_run_bot(self, username, password, area_name, mob_name, headless):
        bot = PockieNinjaStandardAreaFarm(username, password, area_name, mob_name, headless=headless)
        self.bots.append(bot)
        check_exit_success = bot.main_loop()
        return check_exit_success

    
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