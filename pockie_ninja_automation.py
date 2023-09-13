from playwright.sync_api import sync_playwright
import time
import os
from dotenv import load_dotenv
from src import *


def relog(page):
    ## OPENING THE LOGIN SCREEN
    page.click("div[class='start-button']")
    ## ACCOUNT CREDENTIALS
    print("ENTERING ACCOUNT CREDENTIALS...")
    page.type(f"input[id='username']", f"{os.getenv('USER')}")
    page.type("input[id='password']", f"{os.getenv('PASSWORD')}")
    ## LOGIN INTO ACCOUNT
    page.get_by_text("Submit").click()
    print("LOGGED INTO ACCOUNT!")
    ## LOGIN INTO SERVER
    print("LOGGING INTO SERVER...")
    page.get_by_text("Test Server").click()
    print("LOGGED INTO SERVER!")


def close_interface(page, flag_first_time):
    print("CLOSING INTERFACE (CHAT, SETTINGS AND FRIENDS LIST)...")
    if flag_first_time:
        ## CLOSING CHAT
        page.click(f"img[{CHAT_MINIMIZE_BUTTON}]")

        ## CLOSING SETTINGS
        page.click(f"img[{SETTINGS_CLOSE_BUTTON}]")

        ## CLOSING FIRNEDS LIST
        page.click(f"img[{FRIENDS_LIST_MINIZE_BTN}]")

        flag_first_time = False
    
    print("INTERFACES CLOSED!")
    return flag_first_time


def open_valhalla(page, castle_menu):
    castle = page.locator(f"img[{castle_menu}]").bounding_box()
    j = 0
    for j in range(int(round(castle["y"], 0)), int(round(castle["y"]+castle["height"]/2)), 2):
        page.mouse.move(castle["x"] + castle["width"]/2, j)
        
    page.mouse.click(castle["x"] + castle["width"]/2, j)


def cancel_first_fight(page, castle_menu, menu_mode, begin_btn, battle_select_instance, battle_icon):
    print("CANCELLING FIRST FIGHT...")
    ## CLICKING INTO VALLHALLA DECANDENT NEST LVL. 11 --> I HAVE TO BRUSH THE WHOLE AREA TO FIND THE IMAGE (HOVER OVER IT)
    open_valhalla(page, castle_menu)

    ## CLICKING NORMAL MODE
    page.locator(f"img[{menu_mode}]").nth(-1).click()

    ## CLICKING BEGIN
    page.click(f"img[{begin_btn}]")

    ## SELECTING INSTANCE
    page.click(f"img[{battle_select_instance}]")

    ## ENTERING BATTLE
    page.click(f"img[{battle_icon}]")

    ## REFRESH PAGE
    page.reload()

    ## RELOG
    relog(page)



def cancel_subsequent_fights(page, nth_element, battle_select_instance, battle_icon):
    ## SELECTING INSTANCE
    page.click(f"img[{battle_select_instance}]")

    ## ENTERING BATTLE
    nth_instance = page.locator(f"img[{battle_icon}]")
    nth_instance.nth(nth_element).click()

    ## REFRESH PAGE
    page.reload()

    ## RELOG
    relog(page)


def click_card(page):
    print("CLICKING ON THE CARD...")
    card_element = page.locator(f"img[{CARD_IMG_SRC}]")
    card_element.nth(-1).click()
    time.sleep(2)
    page.get_by_text("Collect").click()
    print("CARDS COLLECTED!")


def close_fight_page(page):
    print("CLOSING FIGHT PAGE (OBS: IT WAS OPEN BEFORE FROM PREVIOUS SESSION)")
    time.sleep(2)
    if page.get_by_text("Abandon").count() > 0:
        page.get_by_text("Abandon").click()
        time.sleep(2)
        if page.get_by_text("Leave").count() > 0:
            page.get_by_text("Leave").click()


def fetch_dungeon_info(dungeon_lvl):
    if dungeon_lvl == 11:
        fight_num = DECADENT_NEST_FIGHT_NUM
        castle_menu = DECADENT_NEST_CASTLE_MENU_SRC
        menu_mode = DECADENT_NEST_NORMAL_MODE_SRC
        begin_btn = BEGIN_BTN_SRC
        battle_select_instance = DECADENT_NEST_BATTLE_INSTANCE_SRC
        battle_icon = DECADENT_NEST_BATTLE_ICON_SRC
    elif dungeon_lvl == 16:
        fight_num = VALLHALLA_CAMP_FIGHT_NUM
        castle_menu = VALHALLA_CAMP_CASTLE_MENU_SRC
        menu_mode = VALHALLA_CAMP_NORMAL_MODE_SRC
        begin_btn = BEGIN_BTN_SRC
        battle_select_instance = VALHALLA_CAMP_CAMP_OUTPOST_BATTLE_INSTANCE_SRC
        battle_icon = VALHALLA_CAMP_BATTLE_ICON_SRC

    return fight_num, castle_menu, menu_mode, begin_btn, battle_select_instance, battle_icon


def test_pockie_ninja(dungeon_lvl=11):
    ## LOADING ENVIRONMENT VARIABLES
    load_dotenv()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)## headless=False
        print("OPENED BROWSER")
        
        ## CREATING A NEW PAGE
        page = browser.new_page()

        ## ENTERING WEBSITE
        page.goto("https://pockieninja.online/")
        print("OPENED LINK")

        flag_first_time = True
        count_fight = 0

        ## RELOG
        relog(page)
        
        while(True):
            ## FETCH DUNGEON INFO
            fight_num, castle_menu, menu_mode, begin_btn, battle_select_instance, battle_icon = fetch_dungeon_info(dungeon_lvl)

            ## CLOSING THE FIGHT PAGE IF IT IS OPEN
            close_fight_page(page)

            ## CLOSING CHAT, SETTINGS AND FRIENDS LIST
            flag_first_time = close_interface(page, flag_first_time)

            time.sleep(2)

            cancel_first_fight(page, castle_menu, menu_mode, begin_btn, battle_select_instance, battle_icon)
            count_fight += 1
            
            for i in range(0, fight_num-1):
                print("CANCELING SUBSEQUENT FIGHTS...")
                print("ITERATION NUMBER: ", i+1, " OUT OF ", fight_num-1, " FIGHTS")
                if dungeon_lvl == 11:
                    ## OPENING THE FIGHT PAGE
                    cancel_subsequent_fights(page, nth_element=count_fight, battle_select_instance=battle_select_instance, battle_icon=battle_icon)
                    count_fight += 1
                elif dungeon_lvl == 16:
                    if count_fight < 5:
                        ## OPENING THE FIGHT PAGE
                        cancel_subsequent_fights(page, nth_element=count_fight, battle_select_instance=battle_select_instance, battle_icon=battle_icon)
                        count_fight += 1
                    else:
                        battle_select_instance = VALHALLA_CAMP_PANTHEON_ENTRANCE_BATTLE_INSTANCE_SRC
                        ## OPENING THE FIGHT PAGE
                        cancel_subsequent_fights(page, nth_element=count_fight-(fight_num/2), battle_select_instance=battle_select_instance, battle_icon=battle_icon)
                        count_fight += 1
            print("ALL FIGHTS DONE!")
            

            if count_fight==fight_num:
                ## CLICK ON THE CARD GET REWARD AND RESTART MACRO
                click_card(page)
                count_fight = 0
                ## RELOAD
                page.reload()
                ## RELOG
                relog(page)
                print("RESTARTING MACRO...")


if __name__ == "__main__":
    test_pockie_ninja(dungeon_lvl=16)