from engine import LoadImages
from unit.player_unit import PlayerUnit
import unit

class GladiatorUnit(PlayerUnit):

	def __init__(self, unit_roster, xpos, ypos, name, number, dir, **keywords):
		super().__init__(unit_roster, xpos, ypos, name, number, dir, **keywords)
		self.anim_standing = LoadImages(dir, ["stand2_Frame_0.png", "stand2_Frame_1.png", "stand2_Frame_2.png"]).sequence
		self.anim_atk_stab = LoadImages(dir, ["stabOF_Frame_0.png","stabOF_Frame_1.png","stabOF_Frame_2.png"]).sequence
		self.anim_atk_slash = LoadImages(dir, ["swingT1_Frame_0.png","swingT1_Frame_1.png","swingT1_Frame_2.png"]).sequence
		self.anim_walking = LoadImages(dir, ["walk1_Frame_0.png","walk1_Frame_1.png","walk1_Frame_2.png","walk1_Frame_3.png"]).sequence

unit.unit_types["GladiatorUnit"] = GladiatorUnit