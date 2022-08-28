import json
import time
import pytesseract
import cv2

from enums.walk_type import WalkType
from enums.ball_type import BallType
from enums.potion_type import PotionType
from enums.skill_type import SkillType
from enums.item_type import ItemType
from helper.keyboard import Keyboard
from helper.mouse import Mouse
from helper.globalvalues import GlobalValues
from helper.screenshot import Screenshot
from helper.imagepath import ImagePath
from helper.settings import Settings
from helper.objectdetection import ObjectDetection
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
from PIL import Image


# Class For Helper Operations
class HelperUtil:

    @staticmethod
    def load_pokemon_names():
        json_file = open('json/pokemon_names.json', 'r')
        GlobalValues.pokemon_names = json.loads(json_file.read())

    @staticmethod
    def load_settings():
        json_file = open('json/settings.json', 'r')
        json_settings = json.loads(json_file.read())
        Settings.path_of_tesseract = json_settings["path_of_tesseract"]
        Settings.walk_type = WalkType(json_settings["walk_type"])
        Settings.skill_to_use = SkillType(json_settings["skill_to_use"])
        Settings.walk_speed = json_settings["walk_speed"]
        Settings.pokeball_to_use = BallType(json_settings["pokeball_to_use"])
        Settings.pokemons_to_catch = json_settings["pokemons_to_catch"]
        Settings.potion_to_use = PotionType(json_settings["potion_to_use"])

    @staticmethod
    def save_settings():
        json_data = {
            "path_of_tesseract": Settings.path_of_tesseract,
            "walk_type": Settings.walk_type.value,
            "skill_to_use": Settings.skill_to_use.value,
            "walk_speed": Settings.walk_speed,
            "pokeball_to_use": Settings.pokeball_to_use.value,
            "pokemons_to_catch": Settings.pokemons_to_catch,
            "potion_to_use": Settings.potion_to_use.value
        }
        json_object = json.dumps(json_data, indent=4)
        with open("json/settings.json", "w") as outfile:
            outfile.write(json_object)

    @staticmethod
    def set_buttons_locations(loc):
        GlobalValues.button_loc_1 = loc
        GlobalValues.button_loc_2 = [loc[0] + GlobalValues.buttons_width_diff, loc[1]]
        GlobalValues.button_loc_3 = [loc[0], loc[1] + GlobalValues.buttons_height_diff]
        GlobalValues.button_loc_4 = [loc[0] + GlobalValues.buttons_width_diff,
                                     loc[1] + GlobalValues.buttons_height_diff]
        GlobalValues.pokemon_name_loc_x = loc[0] + GlobalValues.pokemon_name_distance_x
        GlobalValues.pokemon_name_loc_y = loc[1] + GlobalValues.pokemon_name_distance_y
        GlobalValues.pokemon_hp_loc_x = loc[0] + GlobalValues.pokemon_hp_distance_x
        GlobalValues.pokemon_hp_loc_y = loc[1] + GlobalValues.pokemon_hp_distance_y
        GlobalValues.button_loc_bag_right = [loc[0] + GlobalValues.bag_right_distance_x, loc[1]]
        GlobalValues.button_loc_bag_left = [loc[0], loc[1]]
        GlobalValues.button_loc_bag_use_item = [loc[0] + GlobalValues.bag_use_item_distance_x, loc[1]]

    @staticmethod
    def get_pokemon_list():
        arr = []
        for i in range(1, GlobalValues.pokemon_count + 1):
            pokemon_name = GlobalValues.pokemon_names[str(i)]["name"]
            arr.append(pokemon_name)
        return arr

    @staticmethod
    def refresh_pokemon_encounters(pokemon_name):
        first_turn = ObjectDetection.find_object(ImagePath.first_turn)
        if first_turn is not None:
            if pokemon_name in GlobalValues.pokemon_encounters:
                GlobalValues.pokemon_encounters[pokemon_name] += 1
            else:
                GlobalValues.pokemon_encounters[pokemon_name] = 1

    @staticmethod
    def get_pokemon_encounters_data():
        data = []
        for key in GlobalValues.pokemon_encounters.keys():
            data.append([key, GlobalValues.pokemon_encounters[key]])
        return data

    @staticmethod
    def run():
        if WalkType(Settings.walk_type) == WalkType.UpDown:
            key_1 = GlobalValues.key_up
            key_2 = GlobalValues.key_down
        else:
            key_1 = GlobalValues.key_right
            key_2 = GlobalValues.key_left
        in_battle = ObjectDetection.find_object(ImagePath.fight_button)
        while in_battle is None:
            Keyboard.hold(key_1, Settings.walk_speed)
            Keyboard.hold(key_2, Settings.walk_speed)
            in_battle = ObjectDetection.find_object(ImagePath.fight_button)
        if GlobalValues.button_loc_1 is None:
            object_loc = ObjectDetection.find_object(ImagePath.fight_button)
            if object_loc is not None:
                HelperUtil.set_buttons_locations(object_loc)
        time.sleep(0.1)

    @staticmethod
    def get_pokemon_info():
        screenshot = Screenshot.get_screenshot_image()
        x = GlobalValues.pokemon_name_loc_x
        y = GlobalValues.pokemon_name_loc_y
        h = GlobalValues.pokemon_name_rec_height
        w = GlobalValues.pokemon_name_rec_width
        if screenshot is None:
            Screenshot.take_screenshot()
            screenshot = Screenshot.get_screenshot_image()
        rect = screenshot[y:y + h, x:x + w]
        cv2.imwrite(ImagePath.pokemon_name, rect)

        image = Image.open(ImagePath.pokemon_name)
        # Get the size of the image
        width, height = image.size

        # Process every pixel
        for x in range(width):
            for y in range(height):
                current_color = image.getpixel((x, y))
                if current_color[0] < 170 or current_color[1] < 170 or current_color[2] < 170:
                    image.putpixel((x, y), (0, 0, 0, 255))

        pytesseract.pytesseract.tesseract_cmd = Settings.path_of_tesseract
        text = pytesseract.image_to_string(image, lang="eng")
        text_split = text.split(" ")
        pokemon_name = text_split[len(text_split) - 1]
        pokemon_name = pokemon_name.strip('\n')
        for i in range(1, GlobalValues.pokemon_count + 1):
            pokemon_id = str(GlobalValues.pokemon_names[str(i)]["id"])
            pokemon_name_json = GlobalValues.pokemon_names[str(i)]["name"]
            if pokemon_name_json == pokemon_name:
                image = QtGui.QImage("Pokedex/" + pokemon_id + ".png")
                HelperUtil.refresh_pokemon_encounters(pokemon_name)
                return [pokemon_name, QPixmap.fromImage(image), pokemon_id]
        return None

    @staticmethod
    def get_encountered_pokemon():
        if GlobalValues.button_loc_1 is None:
            object_loc = ObjectDetection.find_object(ImagePath.fight_button)
            if object_loc is not None:
                HelperUtil.set_buttons_locations(object_loc)
        return HelperUtil.get_pokemon_info()

    @staticmethod
    def use_skill():
        skill_type = Settings.skill_to_use
        if skill_type == SkillType.Skill1:
            keys = GlobalValues.skill1_keys
        elif skill_type == SkillType.Skill2:
            keys = GlobalValues.skill2_keys
        elif skill_type == SkillType.Skill3:
            keys = GlobalValues.skill3_keys
        elif skill_type == SkillType.Skill4:
            keys = GlobalValues.skill4_keys
        else:
            keys = GlobalValues.skillrun_keys
        for key in keys:
            Keyboard.press(key)
            time.sleep(0.05)

    @staticmethod
    def is_pokemon_found():
        return int(GlobalValues.encountered_pokemon_id) in Settings.pokemons_to_catch

    @staticmethod
    def use_item(item_type):
        # Max Size Of Bag
        max_item_count = 7

        # Control For Bug (If there is no pokeball in the bag)
        is_item_image_found = False

        # Open Bag
        Mouse.click(GlobalValues.button_loc_2)
        time.sleep(0.1)

        # Find Which Pokeball to use
        counter = 0
        while counter <= max_item_count:
            if item_type == ItemType.PokeBall:
                if Settings.pokeball_to_use == BallType.PokeBall:
                    object_loc = ObjectDetection.find_object(ImagePath.poke_ball)
                elif Settings.pokeball_to_use == BallType.GreatBall:
                    object_loc = ObjectDetection.find_object(ImagePath.great_ball)
                elif Settings.pokeball_to_use == BallType.UltraBall:
                    object_loc = ObjectDetection.find_object(ImagePath.ultra_ball)
            elif item_type == ItemType.Potion:
                if Settings.potion_to_use == PotionType.Potion:
                    object_loc = ObjectDetection.find_object(ImagePath.potion)
                elif Settings.potion_to_use == PotionType.SuperPotion:
                    object_loc = ObjectDetection.find_object(ImagePath.super_potion)
                elif Settings.potion_to_use == PotionType.HyperPotion:
                    object_loc = ObjectDetection.find_object(ImagePath.hyper_potion)

            if object_loc is not None and GlobalValues.button_loc_1[0] < object_loc[0] < GlobalValues.button_loc_2[0]:
                is_item_image_found = True
                break
            else:
                Mouse.click(GlobalValues.button_loc_bag_right)
                time.sleep(0.5)
            counter += 1

        if is_item_image_found:
            # Click Multiple Because of Unknown Bug
            for i in range(1, 5):
                Mouse.click(GlobalValues.button_loc_bag_use_item)
                time.sleep(0.1)
        else:
            # 5 = Back Shortcut
            Keyboard.press("5")

        return is_item_image_found

    @staticmethod
    def use_pokeball():
        is_pokemon_found = HelperUtil.is_pokemon_found()
        is_pokeball_used = False
        if is_pokemon_found:
            is_pokeball_used = HelperUtil.use_item(ItemType.PokeBall)
        return is_pokeball_used

    @staticmethod
    def use_potion_if_pokemon_health_less_than_35_percent():
        Screenshot.take_screenshot()
        screenshot = Screenshot.get_screenshot_image()
        x = GlobalValues.pokemon_hp_loc_x
        y = GlobalValues.pokemon_hp_loc_y
        h = GlobalValues.pokemon_hp_rec_height
        w = GlobalValues.pokemon_hp_rec_width
        rect = screenshot[y:y + h, x:x + w]
        cv2.imwrite(ImagePath.hp_rectangle, rect)

        obj_loc = ObjectDetection.find_object_on_rectangle(ImagePath.hp35, ImagePath.hp_rectangle)
        if obj_loc is None and Settings.potion_to_use is not PotionType.DontUse:
            return HelperUtil.use_item(ItemType.Potion)
        return False

