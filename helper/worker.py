from PyQt5.QtCore import pyqtSignal, QObject
from helper.globalvalues import GlobalValues
from helper.helperutil import HelperUtil
from helper.imagepath import ImagePath


def set_encountered_pokemon_info():
    pokemon_info = HelperUtil.get_encountered_pokemon()
    GlobalValues.encountered_pokemon_image = ImagePath.pokemon_default
    GlobalValues.encountered_pokemon = "Unknown"
    GlobalValues.encountered_pokemon_id = -1
    if pokemon_info is not None:
        GlobalValues.encountered_pokemon = pokemon_info[0]
        GlobalValues.encountered_pokemon_image = pokemon_info[1]
        GlobalValues.encountered_pokemon_id = pokemon_info[2]


def take_battle():
    is_potion_used = HelperUtil.use_potion_if_pokemon_health_less_than_35_percent()
    if not is_potion_used:
        is_pokeball_used = HelperUtil.use_pokeball()
        if not is_pokeball_used:
            HelperUtil.use_skill()


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal()
    started = False

    def run(self):
        while self.started:
            # Run until you find a pokemon
            HelperUtil.run()
            # Set Encountered Pokemon Info : Pokemon Name, ID and Image
            set_encountered_pokemon_info()
            # Emit Event and Set Form Processes
            self.progress.emit()
            # Take Battle (Catch Pokemon, Kill Pokemon or Run From Battle)
            take_battle()
        # End of Program
        self.finished.emit()
