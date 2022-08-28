from enums.ball_type import BallType
from enums.walk_type import WalkType
from enums.skill_type import SkillType
from enums.potion_type import PotionType


# Settings class For User Settings -> Json
class Settings:
    path_of_tesseract = ""
    walk_type = WalkType.UpDown
    pokeball_to_use = BallType.PokeBall
    skill_to_use = SkillType.Skill1
    pokemons_to_catch = []
    walk_speed = 0.44
    potion_to_use = PotionType.Potion
