from engine import LoadImages
from unit.player_unit import PlayerUnit
import unit

class SpellWeaverUnit(PlayerUnit):

	def __init__(self, unit_roster, xpos, ypos, name, number, dir, **keywords):
		super().__init__(unit_roster, xpos, ypos, name, number, dir, **keywords)
		self.anim_standing = LoadImages(dir, ["stand1_Frame_0.png", "stand1_Frame_1.png", "stand1_Frame_2.png"]).sequence
		self.anim_atk_stab = LoadImages(dir, ["stabO1_Frame_0.png","shootF_Frame_0.png","shootF_Frame_1.png","shootF_Frame_2.png"]).sequence
		self.anim_atk_slash = LoadImages(dir, ["swingO3_Frame_0.png","swingO3_Frame_1.png","swingO3_Frame_2.png"]).sequence
		self.anim_walking = LoadImages(dir, ["walk1_Frame_0.png","walk1_Frame_1.png","walk1_Frame_2.png","walk1_Frame_3.png"]).sequence

unit.unit_types["SpellWeaverUnit"] = SpellWeaverUnit