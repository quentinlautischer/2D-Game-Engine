from animation import LoadImages
from unit.base_unit import BaseUnit
from unit.base_enemy_unit import BaseEnemyUnit
from animation import Animation
import unit
from ai import AI

class GoblinUnit(BaseEnemyUnit):

	def __init__(self, unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords):
		
		super().__init__(unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords)
		self.anim_standing = LoadImages(dirr, ["stand1_Frame_0.png", "stand1_Frame_1.png", "stand1_Frame_2.png"]).sequence
		self.anim_atk1 = LoadImages(dirr, ["stabOF_Frame_0.png","stabOF_Frame_1.png","stabOF_Frame_2.png"]).sequence
		self.anim_atk2 = LoadImages(dirr, ["swingO1_Frame_0.png","swingO1_Frame_1.png","swingO1_Frame_2.png","swingO1_Frame_2.png"]).sequence
		self.anim_warn1 = LoadImages(dirr, ["swingO1_Frame_0.png","swingO1_Frame_1.png","swingO1_Frame_0.png","swingO1_Frame_1.png"]).sequence 
		self.anim_walking = LoadImages(dirr, ["walk1_Frame_0.png","walk1_Frame_1.png","walk1_Frame_2.png","walk1_Frame_3.png"]).sequence
		self.slash_effect = LoadImages("images/", ["sword_effect.png","sword_effect.png","sword_effect.png"]).sequence
		self.stab_effect = LoadImages("images/", ["stab_effect.png","stab_effect.png","stab_effect.png"]).sequence
		self.anim_death = LoadImages(dirr, ["rope_Frame_0.png"], 90).sequence
		self.attacks_dict = {"one": {"energy": 0, "dmg": 20, "x_range": 60, "y_range": 40},
						"two": {"energy": 0, "dmg": 50, "x_range": 40, "y_range": 40},
						"DOOM": {"energy": 0, "dmg": 100, "x_range": 50, "y_range": 50}}

unit.unit_types["GoblinUnit"] = GoblinUnit