from playwright.sync_api import sync_playwright
import time
from src import *



class PockieNinjaFarmBot:
    def __init__(self, dungeon_lvl, username, password, headless):
        self.dungeon_lvl = dungeon_lvl
        self.username = username
        self.password = password
        self.headless = headless
        self.flag_quit = False
        self.flag_first_time = True
        self.count_fight = 0
        self.fight_num = ""
        self.castle_menu = ""
        self.menu_mode = ""
        self.begin_btn = ""
        self.battle_select_instance = ""
        self.battle_icon = ""
    

    def main_loop(self):
        with sync_playwright() as self.p:
            self.browser = self.p.chromium.launch(headless=self.headless)
            print("OPENED BROWSER")
            
            ## CREATING A NEW PAGE
            self.page = self.browser.new_page()

            ## ENTERING WEBSITE
            self.page.goto("https://pockieninja.online/")
            print("OPENED LINK")

            ## RELOG
            self.relog()
        
            while(not self.flag_quit):

                ## SET DUNGEON INFO
                self.set_dungeon_info()

                ## CLOSING THE FIGHT PAGE IF IT IS OPEN
                self.close_fight_page()

                ## CLOSING CHAT, SETTINGS AND FRIENDS LIST
                self.close_interface()

                time.sleep(2)

                self.cancel_first_fight()
                self.count_fight += 1
                
                for i in range(0, self.fight_num-1):
                    print("CANCELING SUBSEQUENT FIGHTS...")
                    print("ITERATION NUMBER: ", i+1, " OUT OF ", self.fight_num-1, " FIGHTS")
                    if self.dungeon_lvl == 11:
                        ## OPENING THE FIGHT PAGE
                        self.cancel_subsequent_fights(nth_element=self.count_fight)
                        self.count_fight += 1
                    elif self.dungeon_lvl == 16:
                        if self.count_fight < 5:
                            ## OPENING THE FIGHT PAGE
                            self.cancel_subsequent_fights(nth_element=self.count_fight)
                            self.count_fight += 1
                        else:
                            self.battle_select_instance = VALHALLA_CAMP_PANTHEON_ENTRANCE_BATTLE_INSTANCE_SRC
                            ## OPENING THE FIGHT PAGE
                            self.cancel_subsequent_fights(nth_element=self.count_fight-(self.fight_num/2))
                            self.count_fight += 1
                print("ALL FIGHTS DONE!")
                

                if self.count_fight==self.fight_num:
                    ## CLICK ON THE CARD GET REWARD AND RESTART MACRO
                    self.click_card()
                    self.count_fight = 0
                    ## RELOAD
                    self.page.reload()
                    ## RELOG
                    self.relog()
                    print("RESTARTING MACRO...")
        
        print("QUITTING...")


    def relog(self):
        ## OPENING THE LOGIN SCREEN
        self.page.click("div[class='start-button']")
        ## ACCOUNT CREDENTIALS
        self.page.type(f"input[id='username']", self.username)
        self.page.type("input[id='password']", self.password)
        ## LOGIN INTO ACCOUNT
        self.page.get_by_text("Submit").click()
        print(f"LOGGED INTO ACCOUNT {self.username}!")
        self.page.get_by_text("Test Server").click()
        print("ENTERED SERVER!")


    def set_dungeon_info(self):
        if self.dungeon_lvl == 11:
            self.fight_num = DECADENT_NEST_FIGHT_NUM
            self.castle_menu = DECADENT_NEST_CASTLE_MENU_SRC
            self.menu_mode = DECADENT_NEST_NORMAL_MODE_SRC
            self.begin_btn = BEGIN_BTN_SRC
            self.battle_select_instance = DECADENT_NEST_BATTLE_INSTANCE_SRC
            self.battle_icon = DECADENT_NEST_BATTLE_ICON_SRC
        elif self.dungeon_lvl == 16:
            self.fight_num = VALLHALLA_CAMP_FIGHT_NUM
            self.castle_menu = VALHALLA_CAMP_CASTLE_MENU_SRC
            self.menu_mode = VALHALLA_CAMP_NORMAL_MODE_SRC
            self.begin_btn = BEGIN_BTN_SRC
            self.battle_select_instance = VALHALLA_CAMP_CAMP_OUTPOST_BATTLE_INSTANCE_SRC
            self.battle_icon = VALHALLA_CAMP_BATTLE_ICON_SRC


    def close_fight_page(self):
        print("CLOSING FIGHT PAGE (OBS: IT WAS OPEN BEFORE FROM PREVIOUS SESSION)")
        time.sleep(2)
        if self.page.get_by_text("Abandon").count() > 0:
            self.page.get_by_text("Abandon").click()
            time.sleep(2)
            if self.page.get_by_text("Leave").count() > 0:
                self.page.get_by_text("Leave").click()

    
    def close_interface(self):
        print("CLOSING INTERFACE (CHAT, SETTINGS AND FRIENDS LIST)...")
        if self.flag_first_time:
            ## CLOSING CHAT
            self.page.click(f"img[{CHAT_MINIMIZE_BUTTON}]")

            ## CLOSING SETTINGS
            self.page.click(f"img[{SETTINGS_CLOSE_BUTTON}]")

            ## CLOSING FIRNEDS LIST
            self.page.click(f"img[{FRIENDS_LIST_MINIZE_BTN}]")

            self.flag_first_time = False
        
        print("INTERFACES CLOSED!")

    
    def open_valhalla(self):
        castle = self.page.locator(f"img[{self.castle_menu}]").bounding_box()
        j = 0
        for j in range(int(round(castle["y"], 0)), int(round(castle["y"]+castle["height"]/2)), 2):
            self.page.mouse.move(castle["x"] + castle["width"]/2, j)
            
        self.page.mouse.click(castle["x"] + castle["width"]/2, j)

    
    def cancel_first_fight(self):
        print("CANCELLING FIRST FIGHT...")
        ## CLICKING INTO VALLHALLA DECANDENT NEST LVL. 11 --> I HAVE TO BRUSH THE WHOLE AREA TO FIND THE IMAGE (HOVER OVER IT)
        self.open_valhalla()

        ## CLICKING NORMAL MODE
        self.page.locator(f"img[{self.menu_mode}]").nth(-1).click()

        ## CLICKING BEGIN
        self.page.click(f"img[{self.begin_btn}]")

        ## SELECTING INSTANCE
        self.page.click(f"img[{self.battle_select_instance}]")

        ## ENTERING BATTLE
        self.page.click(f"img[{self.battle_icon}]")

        ## REFRESH PAGE
        self.page.reload()

        ## RELOG
        self.relog()


    def cancel_subsequent_fights(self, nth_element):
        ## SELECTING INSTANCE
        self.page.click(f"img[{self.battle_select_instance}]")

        ## ENTERING BATTLE
        nth_instance = self.page.locator(f"img[{self.battle_icon}]")
        nth_instance.nth(nth_element).click()

        ## REFRESH PAGE
        self.page.reload()

        ## RELOG
        self.relog()

    
    def click_card(self):
        print("CLICKING ON THE CARD...")
        card_element = self.page.locator(f"img[{CARD_IMG_SRC}]")
        card_element.nth(-1).click()
        time.sleep(2)
        self.page.get_by_text("Collect").click()
        print("CARDS COLLECTED!")


    def quit(self):
        self.flag_quit = True


if __name__ == "__main__":
    bot = PockieNinjaFarmBot(dungeon_lvl=11, username='clib_haze', password='limaolima1', headless=False)
    bot.main_loop()
