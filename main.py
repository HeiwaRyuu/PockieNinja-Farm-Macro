import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pockie_ninja_automation import *
import sys
import threading
from src import *

VALHALLA_FARM_WINDOW_SIZE="320x200"
STANDARD_AREA_FARM_WINDOW_SIZE ="340x200"
MAIN_MENU_WINDOW_SIZE="200x150"
STANDARD_PADDING_X=15
STANDARD_PADDING_Y=3


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
        self.create_widgets()
        center(self.master)


    def create_widgets(self):
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.valhalla_farm_button = ttk.Button(self.master, text="Valhalla Farm", command=self.on_valhalla_farm_button_click)
        self.regular_area_button = ttk.Button(self.master, text="Regular Area Farm", command=self.on_regular_area_button_click)

        self.valhalla_farm_button.grid(row=0, column=0, pady=25)
        self.regular_area_button.grid(row=1, column=0)


    def on_valhalla_farm_button_click(self):
        self.master.destroy()
        root = tk.Tk()
        app = ValhallaFarm(master=root)
        ## STYLE USING TKINTER TTK
        set_style()
        
        app.mainloop()


    def on_regular_area_button_click(self):
        self.master.destroy()
        root = tk.Tk()
        app = StandardAreaFarm(master=root)
        ## STYLE USING TKINTER TTK
        set_style()
        
        app.mainloop()


class ValhallaFarm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Pockie Ninja Bot - Valhalla Farm")
        self.master.geometry(VALHALLA_FARM_WINDOW_SIZE)
        self.master.resizable(False, False)
        self.create_widgets()
        self.bots = []
        self.threads = []
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
        self.username_label = ttk.Label(self.master, text="Username:")
        self.username_entry = ttk.Entry(self.master)
        self.password_label = ttk.Label(self.master, text="Password:")
        self.password_entry = ttk.Entry(self.master, show="*")
        ## SET DUNGEON LEVEL AS A OPTION MENU
        self.dungeon_level_options = [VALHALLA_LVL_11, VALHALLA_LVL_16]
        self.dungeon_lvl_label = ttk.Label(self.master, text="Dungeon Level:")
        self.dungeon_lvl_str_var = tk.StringVar()
        self.dungeon_lvl_str_var.set(self.dungeon_level_options[0])
        self.dungeon_lvl_option_menu = tk.OptionMenu(self.master, self.dungeon_lvl_str_var , *self.dungeon_level_options, command=self.update_difficulties)
        ## DIFFICULTY OPTION MENU
        self.difficulty_options = [SOLO_VALHALLA_DIFFICULTY]
        self.difficulty_option_label = ttk.Label(self.master, text="Choose difficulty:")
        self.difficulty_str_var = tk.StringVar()
        self.difficulty_str_var.set(self.difficulty_options[0])
        self.difficulty_option_menu = tk.OptionMenu(self.master, self.difficulty_str_var , *self.difficulty_options)
        ## ADD A CHECKBOX IF YOU WANT TO RUN THE BOT IN HEADLESS MODE
        self.headless_var = tk.IntVar()
        self.headless_label = ttk.Label(self.master, text="Headless (No Browser):")
        self.headless_checkbox = ttk.Checkbutton(self.master, variable=self.headless_var)
        self.start_button = ttk.Button(self.master, text="Start", command=self.on_start_button_click)
        self.back_to_main_menu_button = ttk.Button(self.master, text="Back to Main Menu", command=self.back_to_main_menu)

        self.username_label.grid(row=0, column=0, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.username_entry.grid(row=0, column=1, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.password_label.grid(row=1, column=0, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.password_entry.grid(row=1, column=1, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.dungeon_lvl_label.grid(row=2, column=0, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.dungeon_lvl_option_menu.grid(row=2, column=1, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.difficulty_option_label.grid(row=3, column=0, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.difficulty_option_menu.grid(row=3, column=1, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.headless_label.grid(row=4, column=0, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.headless_checkbox.grid(row=4, column=1, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.start_button.grid(row=5, column=0, pady=STANDARD_PADDING_Y)
        self.back_to_main_menu_button.grid(row=5, column=1, pady=STANDARD_PADDING_Y)


    def back_to_main_menu(self):
        self.master.destroy()
        root = tk.Tk()
        app = MainMenu(master=root)
        set_style()
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
        area_names = [SMELTING_MOUNTAINS_AREA_NAME, EVENTIDE_BARRENS_AREA_NAME, CROSSROADS_AREA_NAME]
        return area_names

    def populate_mob_names(self):
        options = [SUNFLOWER_NAME, BEE_NAME, SUSHI_NAME, SCARLET_NAME, WARRIOR_OF_DARKNESS_NAME] # , DEMON_BRUTE_NAME
        return options
    
    def update_mob_names(self, *args):
        # Reset var and delete all old options
        self.mob_name_str_var.set('')
        self.mob_name_option_menu['menu'].delete(0, 'end')
        area_name = self.area_name_option_menu.cget("text")
        if area_name == SMELTING_MOUNTAINS_AREA_NAME:
            options = [SUNFLOWER_NAME, BEE_NAME, SUSHI_NAME, SCARLET_NAME, WARRIOR_OF_DARKNESS_NAME] # , DEMON_BRUTE_NAME
        elif area_name == EVENTIDE_BARRENS_AREA_NAME:
            options = [POTATO_NAME, MONKEY_NAME, MEAL_NAME, KAPPA_NAME, BULLHEAD_NAME] # , PLAGUE_DEMON_NAME
        elif area_name == CROSSROADS_AREA_NAME:
            options = [TREE_ENT_NAME, MAN_EATER_NAME, LONGFEATHER_DEMON_NAME, CHEVALIER_DEMON_NAME, SHADOW_BAT_NAME,] # SOULENDER_NAME
        # Insert list of new options (tk._setit hooks them up to var)
        for option in options:
            self.mob_name_option_menu['menu'].add_command(label=option, command=tk._setit(self.mob_name_str_var, option))
        self.mob_name_str_var.set(options[0])

    def create_widgets(self):
        self.username_label = ttk.Label(self, text="Username")
        self.username_entry = ttk.Entry(self)
        self.password_label = ttk.Label(self, text="Password")
        self.password_entry = ttk.Entry(self, show="*")
        ## AREA NAMES DROPDOWN MENU
        area_options = self.populate_area_names()
        self.area_option_label = ttk.Label(self, text="Choose Area")
        self.area_name_str_var = tk.StringVar()
        self.area_name_str_var.set(area_options[0])
        self.area_name_option_menu = tk.OptionMenu(self , self.area_name_str_var , *area_options, command=self.update_mob_names)
        ## MOB NAMES DROPDOWN MENU
        mobs_options = self.populate_mob_names()
        self.mob_option_label = ttk.Label(self, text="Choose Mob")
        self.mob_name_str_var = tk.StringVar()
        self.mob_name_str_var.set(mobs_options[0])
        self.mob_name_option_menu = tk.OptionMenu(self , self.mob_name_str_var , *mobs_options)
        ## ADD A CHECKBOX IF YOU WANT TO RUN THE BOT IN HEADLESS MODE
        self.headless_var = tk.IntVar()
        self.headless_label = ttk.Label(self, text="Headless (No Browser):")
        self.headless_checkbox = ttk.Checkbutton(self, variable=self.headless_var)
        self.start_button = ttk.Button(self, text="Start", command=self.on_start_button_click)
        self.back_to_main_menu_button = ttk.Button(self, text="Back to Main Menu", command=self.back_to_main_menu)

        self.username_label.grid(row=0, column=0, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.username_entry.grid(row=0, column=1, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.password_label.grid(row=1, column=0, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.password_entry.grid(row=1, column=1, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.area_option_label.grid(row=2, column=0, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.area_name_option_menu.grid(row=2, column=1, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.mob_option_label.grid(row=3, column=0, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.mob_name_option_menu.grid(row=3, column=1, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.headless_label.grid(row=4, column=0, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.headless_checkbox.grid(row=4, column=1, sticky="w", padx=STANDARD_PADDING_X, pady=STANDARD_PADDING_Y)
        self.start_button.grid(row=5, column=0, pady=STANDARD_PADDING_Y)
        self.back_to_main_menu_button.grid(row=5, column=1, pady=STANDARD_PADDING_Y)

    def back_to_main_menu(self):
        self.master.destroy()
        root = tk.Tk()
        app = MainMenu(master=root)
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

def center(toplevel):
    toplevel.update_idletasks()
    # Tkinter way to find the screen resolution
    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2
    toplevel.geometry("+%d+%d" % (x, y))

def rebuild():
    root = tk.Tk()
    app = MainMenu(master=root)
    set_style()
    app.mainloop()

if __name__ == "__main__":
    rebuild()