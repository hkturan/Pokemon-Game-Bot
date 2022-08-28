import sys
import time

from PyQt5 import QtGui, QtWidgets, uic, QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPixmap
from helper.aligndelegate import AlignDelegate
from helper.imagepath import ImagePath
from helper.globalvalues import GlobalValues
from helper.helperutil import HelperUtil
from helper.settings import Settings
from helper.tablemodel import TableModel
from helper.worker import Worker
from enums.ball_type import BallType
from enums.potion_type import PotionType
from enums.skill_type import SkillType
from enums.walk_type import WalkType


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method

        # Buttons
        self.btn_start = None
        self.btn_stop = None
        self.btn_delete_list = None

        # List Widgets
        self.list_pokemons_to_catch = None
        self.list_pokemons_to_catch_selected = None

        # Labels
        self.label_encountered_pokemon = None
        self.label_image_encountered_pokemon = None
        self.label_image_icon = None
        self.img_pokeball = None
        self.img_greatball = None
        self.img_ultraball = None
        self.img_potion = None
        self.img_superpotion = None
        self.img_hyperpotion = None
        self.img_updown = None
        self.img_leftright = None
        self.label_walk_speed = None
        self.img_search = None

        # Sliders
        self.slider_walk_speed = None

        # Radio Buttons
        self.rb_skill1 = None
        self.rb_skill2 = None
        self.rb_skill3 = None
        self.rb_skill4 = None
        self.rb_skillrun = None
        self.rb_pokeball = None
        self.rb_greatball = None
        self.rb_ultraball = None
        self.rb_potion = None
        self.rb_superpotion = None
        self.rb_hyperpotion = None
        self.rb_potiondontuse = None
        self.rb_walk_leftright = None
        self.rb_walk_updown = None

        # Tables
        self.table_encountered_pokemons = None

        # Line Edits
        self.txt_search = None

        self.setup_form()

    def setup_form(self):
        # Load the .ui file
        uic.loadUi('ui/main.ui', self)

        # --- Form Components
        # Buttons
        self.btn_start = self.findChild(QtWidgets.QPushButton, 'btnStart')
        self.btn_stop = self.findChild(QtWidgets.QPushButton, 'btnStop')
        self.btn_delete_list = self.findChild(QtWidgets.QPushButton, 'btnDeleteList')

        # List Widgets
        self.list_pokemons_to_catch = self.findChild(QtWidgets.QListWidget, 'listPokemonsToCatch')
        self.list_pokemons_to_catch_selected = self.findChild(QtWidgets.QListWidget, 'listPokemonsToCatchSelected')

        # Labels
        self.label_encountered_pokemon = self.findChild(QtWidgets.QLabel, 'lblEncounteredPokemon')
        self.label_image_encountered_pokemon = self.findChild(QtWidgets.QLabel, 'lblImageEncounteredPokemon')
        self.label_image_icon = self.findChild(QtWidgets.QLabel, 'lblImageIcon')
        self.img_pokeball = self.findChild(QtWidgets.QLabel, 'imgPokeball')
        self.img_greatball = self.findChild(QtWidgets.QLabel, 'imgGreatball')
        self.img_ultraball = self.findChild(QtWidgets.QLabel, 'imgUltraball')
        self.img_potion = self.findChild(QtWidgets.QLabel, 'imgPotion')
        self.img_superpotion = self.findChild(QtWidgets.QLabel, 'imgSuperPotion')
        self.img_hyperpotion = self.findChild(QtWidgets.QLabel, 'imgHyperPotion')
        self.img_updown = self.findChild(QtWidgets.QLabel, 'imgUpDown')
        self.img_leftright = self.findChild(QtWidgets.QLabel, 'imgLeftRight')
        self.label_walk_speed = self.findChild(QtWidgets.QLabel, 'labelWalkSpeed')
        self.img_search = self.findChild(QtWidgets.QLabel, 'lblImageSearch')

        # Sliders
        self.slider_walk_speed = self.findChild(QtWidgets.QSlider, 'sliderWalkSpeed')

        # Radio Buttons
        self.rb_skill1 = self.findChild(QtWidgets.QRadioButton, 'rbSkill1')
        self.rb_skill2 = self.findChild(QtWidgets.QRadioButton, 'rbSkill2')
        self.rb_skill3 = self.findChild(QtWidgets.QRadioButton, 'rbSkill3')
        self.rb_skill4 = self.findChild(QtWidgets.QRadioButton, 'rbSkill4')
        self.rb_skillrun = self.findChild(QtWidgets.QRadioButton, 'rbSkillRun')
        self.rb_pokeball = self.findChild(QtWidgets.QRadioButton, 'rbPokeball')
        self.rb_greatball = self.findChild(QtWidgets.QRadioButton, 'rbGreatball')
        self.rb_ultraball = self.findChild(QtWidgets.QRadioButton, 'rbUltraball')
        self.rb_potion = self.findChild(QtWidgets.QRadioButton, 'rbPotion')
        self.rb_superpotion = self.findChild(QtWidgets.QRadioButton, 'rbSuperPotion')
        self.rb_hyperpotion = self.findChild(QtWidgets.QRadioButton, 'rbHyperPotion')
        self.rb_potiondontuse = self.findChild(QtWidgets.QRadioButton, 'rbPotionDontUse')
        self.rb_walk_leftright = self.findChild(QtWidgets.QRadioButton, 'rbWalkTypeLeftRight')
        self.rb_walk_updown = self.findChild(QtWidgets.QRadioButton, 'rbWalkTypeUpDown')

        # Tables
        self.table_encountered_pokemons = self.findChild(QtWidgets.QTableView, 'tableEncounteredPokemons')

        # Line Edits
        self.txt_search = self.findChild(QtWidgets.QLineEdit, 'txtSearch')

        # Table Settings
        header = self.table_encountered_pokemons.horizontalHeader()
        self.table_encountered_pokemons.setColumnWidth(0, 120)
        self.table_encountered_pokemons.setColumnWidth(1, 61)
        delegate = AlignDelegate(self.table_encountered_pokemons)
        self.table_encountered_pokemons.setItemDelegateForColumn(1, delegate)
        afont = QtGui.QFont()
        afont.setFamily("Arial Black")
        afont.setPointSize(9)
        header.setFont(afont)

        # Form Component Defaults
        self.list_pokemons_to_catch.setSelectionMode(QtWidgets.QListWidget.MultiSelection)
        self.slider_walk_speed.setMaximum(100)
        self.slider_walk_speed.setMinimum(0)
        self.img_pokeball.setPixmap(QPixmap.fromImage(QtGui.QImage(ImagePath.design_poke_ball)))
        self.img_greatball.setPixmap(QPixmap.fromImage(QtGui.QImage(ImagePath.design_great_ball)))
        self.img_ultraball.setPixmap(QPixmap.fromImage(QtGui.QImage(ImagePath.design_ultra_ball)))
        self.img_potion.setPixmap(QPixmap.fromImage(QtGui.QImage(ImagePath.design_potion)))
        self.img_superpotion.setPixmap(QPixmap.fromImage(QtGui.QImage(ImagePath.design_superpotion)))
        self.img_hyperpotion.setPixmap(QPixmap.fromImage(QtGui.QImage(ImagePath.design_hyperpotion)))
        self.img_leftright.setPixmap(QPixmap.fromImage(QtGui.QImage(ImagePath.design_walktype_leftright)))
        self.img_updown.setPixmap(QPixmap.fromImage(QtGui.QImage(ImagePath.design_walktype_updown)))
        self.label_image_encountered_pokemon.setPixmap(QPixmap.fromImage(QtGui.QImage(ImagePath.pokemon_default)))
        self.label_image_icon.setPixmap(QPixmap.fromImage(QtGui.QImage(ImagePath.icon)))
        self.img_search.setPixmap(QPixmap.fromImage(QtGui.QImage(ImagePath.search)))
        self.label_image_encountered_pokemon.setVisible(False)
        self.label_encountered_pokemon.setVisible(False)
        self.btn_start.setIcon(QtGui.QIcon(QtGui.QPixmap(ImagePath.start)))
        self.btn_stop.setIcon(QtGui.QIcon(QtGui.QPixmap(ImagePath.stop)))
        self.btn_delete_list.setIcon(QtGui.QIcon(QtGui.QPixmap(ImagePath.delete)))

        # Form Component Event Connects
        self.slider_walk_speed.valueChanged.connect(self.value_changed_slider_walk_speed)
        self.btn_start.clicked.connect(self.run)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_delete_list.clicked.connect(self.delete_selected_pokemons_list)
        self.txt_search.textChanged.connect(self.search_pokemon)
        self.list_pokemons_to_catch.itemClicked.connect(self.list_pokemons_clicked)

        # Load Settings and Pokemon Names From Json File, then Add to List
        HelperUtil.load_settings()
        HelperUtil.load_pokemon_names()
        self.list_pokemons_to_catch.addItems(HelperUtil.get_pokemon_list())

        # Load Settings - Form
        self.load_settings()

        # Show the GUI
        self.show()

    def delete_selected_pokemons_list(self):
        self.list_pokemons_to_catch.clearSelection()
        self.list_pokemons_to_catch_selected.clear()

    def list_pokemons_clicked(self, item):
        items = self.list_pokemons_to_catch_selected.findItems(item.text(), QtCore.Qt.MatchExactly)
        if len(items) > 0:
            row = self.list_pokemons_to_catch_selected.row(items[0])
            self.list_pokemons_to_catch_selected.takeItem(row)
        else:
            self.list_pokemons_to_catch_selected.addItem(item.text())

    def search_pokemon(self, text):
        model = self.list_pokemons_to_catch.model()
        match = model.match(
            model.index(0, self.list_pokemons_to_catch.modelColumn()),
            QtCore.Qt.DisplayRole,
            text,
            hits=1,
            flags=QtCore.Qt.MatchContains)
        if match:
            self.list_pokemons_to_catch.setCurrentIndex(match[0])
            self.list_pokemons_to_catch.item(match[0].row()).setSelected(False)

    def start(self):
        if not self.worker.started:
            self.worker.started = True

    def stop(self):
        if self.worker.started:
            self.worker.started = False

    def reportProgress(self):
        self.show_encountered_pokemon()
        data = HelperUtil.get_pokemon_encounters_data()
        self.model = TableModel(data)
        self.table_encountered_pokemons.setModel(self.model)
        self.table_encountered_pokemons.setColumnWidth(0, 160)
        self.table_encountered_pokemons.setColumnWidth(1, 61)

    def run(self):
        self.label_image_encountered_pokemon.setVisible(True)
        self.label_encountered_pokemon.setVisible(True)
        self.label_image_icon.setVisible(False)
        time.sleep(0.2)
        Settings.pokemons_to_catch = []
        for selectedItem in self.list_pokemons_to_catch.selectedIndexes():
            Settings.pokemons_to_catch.append(selectedItem.row() + 1)

        # Save Settings
        self.save_settings()

        # Create a QThread object
        self.thread = QThread()
        # Create a worker object
        self.worker = Worker()
        # Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        # Start the thread
        self.start()
        self.thread.start()

    def show_encountered_pokemon(self):
        self.label_encountered_pokemon.setText(GlobalValues.encountered_pokemon)
        self.label_image_encountered_pokemon.setPixmap(GlobalValues.encountered_pokemon_image)

    def load_settings(self):
        # Walk Speed
        self.slider_walk_speed.setValue(int(Settings.walk_speed * 100))
        self.value_changed_slider_walk_speed()

        # Walk Type
        walk_type = Settings.walk_type
        if walk_type == WalkType.UpDown:
            self.rb_walk_updown.setChecked(True)
        elif walk_type == WalkType.LeftRight:
            self.rb_walk_leftright.setChecked(True)

        # Skill
        skill_type = Settings.skill_to_use
        if skill_type == SkillType.Skill1:
            self.rb_skill1.setChecked(True)
        elif skill_type == SkillType.Skill2:
            self.rb_skill2.setChecked(True)
        elif skill_type == SkillType.Skill3:
            self.rb_skill3.setChecked(True)
        elif skill_type == SkillType.Skill4:
            self.rb_skill4.setChecked(True)
        elif skill_type == SkillType.SkillRun:
            self.rb_skillrun.setChecked(True)

        # Pokeball
        enum_pokeball = Settings.pokeball_to_use
        if enum_pokeball == BallType.PokeBall:
            self.rb_pokeball.setChecked(True)
        elif enum_pokeball == BallType.GreatBall:
            self.rb_greatball.setChecked(True)
        elif enum_pokeball == BallType.UltraBall:
            self.rb_ultraball.setChecked(True)

        # Potion
        enum_potion = PotionType(Settings.potion_to_use)
        if enum_potion == PotionType.Potion:
            self.rb_potion.setChecked(True)
        elif enum_potion == PotionType.SuperPotion:
            self.rb_superpotion.setChecked(True)
        elif enum_potion == PotionType.HyperPotion:
            self.rb_hyperpotion.setChecked(True)
        elif enum_potion == PotionType.DontUse:
            self.rb_potiondontuse.setChecked(True)

        # Pokemons to Catch
        for pokemon_id in Settings.pokemons_to_catch:
            self.list_pokemons_to_catch.item(pokemon_id - 1).setSelected(True)
            self.list_pokemons_clicked(self.list_pokemons_to_catch.item(pokemon_id - 1))

    def save_settings(self):
        # Walk Speed
        Settings.walk_speed = self.slider_walk_speed.value() / 100

        # Walk Type
        if self.rb_walk_updown.isChecked():
            Settings.walk_type = WalkType.UpDown
        elif self.rb_walk_leftright.isChecked():
            Settings.walk_type = WalkType.LeftRight

        # Skill
        if self.rb_skill1.isChecked():
            Settings.skill_to_use = SkillType.Skill1
        elif self.rb_skill2.isChecked():
            Settings.skill_to_use = SkillType.Skill2
        elif self.rb_skill3.isChecked():
            Settings.skill_to_use = SkillType.Skill3
        elif self.rb_skill4.isChecked():
            Settings.skill_to_use = SkillType.Skill4
        elif self.rb_skillrun.isChecked():
            Settings.skill_to_use = SkillType.SkillRun

        # Pokeball
        if self.rb_pokeball.isChecked():
            Settings.pokeball_to_use = BallType.PokeBall
        elif self.rb_greatball.isChecked():
            Settings.pokeball_to_use = BallType.GreatBall
        elif self.rb_ultraball.isChecked():
            Settings.pokeball_to_use = BallType.UltraBall

        # Potion
        if self.rb_potion.isChecked():
            Settings.potion_to_use = PotionType.Potion
        elif self.rb_superpotion.isChecked():
            Settings.potion_to_use = PotionType.SuperPotion
        elif self.rb_hyperpotion.isChecked():
            Settings.potion_to_use = PotionType.HyperPotion
        elif self.rb_potiondontuse.isChecked():
            Settings.potion_to_use = PotionType.DontUse

        # Pokemons to Catch
        Settings.pokemons_to_catch = []
        for selectedItem in self.list_pokemons_to_catch.selectedIndexes():
            Settings.pokemons_to_catch.append((selectedItem.row() + 1))

        # Save All
        HelperUtil.save_settings()

    # Walk Speed Slider Value Change Event
    def value_changed_slider_walk_speed(self):
        self.label_walk_speed.setText(str(self.slider_walk_speed.value() / 100))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
