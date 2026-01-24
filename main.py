#!/bin/python
import math, sys, os, json
from functools import cmp_to_key
from PIL import Image, ImageDraw



# The path to the data folder.
FDATA = "data"

# Available conversion scope keys recognized as the command line arguments.
CONVERSION_SCOPE_KEYS = {
	"--sprites": "sprites",
	"--maps": "maps",
	"--levels": "levels",
	"--fonts": "fonts",
	"--particles": "particles",
	"--sounds": "sounds",
	"--music": "music",
	"--ui": "ui",
	"--uiscriptlet": "uiscriptlet",
	"--powerups": "powerups",
	"--layers": "layers",
	"--shooter": "shooter",
	"--spheres": "spheres",
	"--locale": "locale",
	"--highscores": "highscores"
}

# A list of folders in the `<FDATA>/maps` folder.
# All directories which match the name will be converted to the case in this reference list.
# Filled in `convert()`.
MAP_NAMES = []

# Maps keyboard shortcuts from the MumboJumbo engine to LOVE2D.
KEYS = {
	"KEY_ENTER": "return",
	"KEY_ESCAPE": "escape",
	"KEY_SPACE": "space",
	"KEY_BACKSPACE": "backspace"
}



#
#  UTILITY
#

###  Converts case LIKE THIS to case LikeThis.
def convert_pascal(line):
	return "".join(word[0].upper() + word[1:].lower() for word in line.split(" "))

### Fixes paths for unix-like systems. This includes backslashes and different directory name casing.
def fix_path(path):
	if path[0] == "\"" and path[-1] == "\"":
		# Unquote the string.
		path = path[1:-1].replace("\\\\", "\\")
	path = path.replace("\\", "/")
	path = path.replace("data/", FDATA + "/")
	if FDATA + "/maps" in path:
		components = path.split("/")
		components_lower = [component.lower() for component in components]
		for name in MAP_NAMES:
			if name.lower() in components_lower:
				components[components_lower.index(name.lower())] = name
		path = "/".join(components)

	return path

###  Takes a file from a given path and returns its contents as a list of lines.
def get_contents(path):
	path = fix_path(path) # MacOS hack
	file = open(path, "r")
	contents = file.read()
	file.close()
	if contents[0] == "\ufeff": # Remove BOM
		contents = contents[1:]
	return contents.split("\n")

###  Takes a file from a given path and returns its contents as a binary string.
def get_binary_contents(path):
	path = fix_path(path) # MacOS hack
	file = open(path, "rb")
	contents = file.read()
	file.close()
	return contents

###  Stores given data in JSON format in a given file.
def store_contents(path, contents):
	make_dir(path)
	file = open(path, "w")
	file.write(json.dumps(contents, indent = 4))
	file.close()

###  Takes a list of lines and processes it, creating a new list of lines.
###  The returned list has all leading and trailing whitespace, empty and commented out lines removed.
###  The lines are also split into a list of words.
def preprocess_contents(contents):
	lines = []
	for line in contents:
		line = line.strip()
		# Ignore empty lines.
		if line == "":
			continue
		words = line.split(" ")
		# Remove empty words.
		while "" in words:
			words.remove("")
		# Ignore comments.
		if not words[0].startswith("//"):
			lines.append(words)
	return lines

###  Creates a folder with a given path if it doesn't exist yet.
def make_dir(path):
	# Cut off the file part.
	if "." in path.split("/")[-1]:
		path = "/".join(path.split("/")[:-1])
	if not os.path.exists(path):
		os.makedirs(path)

###  Returns True if a given file exists.
def file_exists(path):
	try:
		open(path, "r")
	except:
		return False
	return True

###  Changes e.g. "data\bitmaps\powerups\wild_pal.jpg" to "images/powerups/wild_pal.png".
def resolve_path_image2(path):
	return fix_path(path).replace(FDATA + "/bitmaps", "images")[:-4] + ".png"

###  Changes e.g. "data\sprites\game\shooter.spr" to "images/game/shooter.png".
def resolve_path_image(path):
	return fix_path(path).replace(FDATA + "/sprites", "images").replace(FDATA + "/", "")[:-4] + ".png"

###  Changes e.g. "data\sprites\game\shooter.spr" to "sprites/game/shooter.json".
def resolve_path_sprite(path):
	return fix_path(path).replace(FDATA + "/", "")[:-4] + ".json"

###  Changes e.g. "data\maps\UraeusNefertari\map.ui" to "maps/UraeusNefertari/config.json".
def resolve_path_map(path):
	return fix_path(path).replace(FDATA + "/maps", "maps").replace("map.ui", "config.json")

###  Changes e.g. "data\fonts\score4.font" to "fonts/score4.json".
def resolve_path_font(path):
	return fix_path(path).replace(FDATA + "/fonts", "fonts")[:-5] + ".json"

###  Changes e.g. "data\psys\powerup_stop.psys" to "particles/powerup_stop.json".
def resolve_path_particle(path):
	return fix_path(path).replace(FDATA + "/psys", "particles")[:-5] + ".json"

###  Changes e.g. "data\sound\collapse_1.ogg" to "sounds/collapse_1.ogg".
def resolve_path_sound(path):
	return fix_path(path).replace(FDATA + "/sound", "sounds")

###  Changes e.g. "data\music\menu.ogg" to "music/menu.ogg".
def resolve_path_music(path):
	return fix_path(path).replace(FDATA + "/music", "music")

###  Changes e.g. "data\uiscript\banner_paused.ui" to "ui/banner_paused.json".
def resolve_path_ui(path):
	return fix_path(path).replace(FDATA + "/uiscript", "ui")[:-3] + ".json"

###  If both values are identical, return that value. If not, return a random value generator, eg. "randomi(1, 3)"
def collapse_random_base(a, b, is_float):
	if a == b:
		return a
	else:
		return ("randomf" if is_float else "randomi") + "(" + str(a) + ", " + str(b) + ")"

###  If both values are identical, return that value. If not, return a random value generator expression, eg. "${randomi(1, 3)}"
def collapse_random_number(a, b, is_float):
	if a == b:
		return a
	else:
		return "${" + collapse_random_base(a, b, is_float) + "}"

###  If both vectors are identical, return it, eg. {"x": 1, "y": 3}. If not, return a random value generator expression, eg. "${vec2(randomf(0, 1), randomf(-1, 1))}"
def collapse_random_vector(ax, ay, bx, by, is_float):
	if ax == bx and ay == by:
		return {"x": ax, "y": ay}
	else:
		return "${vec2(" + str(collapse_random_base(ax, bx, is_float)) + ", " + str(collapse_random_base(ay, by, is_float)) + ")}"

###  Gets a UI child by name. This cannot go outside of a single file.
def get_ui_child(ui_data, child_name):
	for child in ui_data["children"]:
		if type(child) is dict and child["name"] == child_name:
			return child



#
#  ACTUAL PROCEDURES
#

#
#  Takes images "img" (*.jpg) and "alpha" (*.tga) and returns a combined *.png file.
#

def combine_alpha(img, alpha = None):
	combine = alpha != None

	px = img.load()
	if combine:
		px_alpha = alpha.convert(mode = "L").load()

	result = Image.new("RGBA" if combine else "RGB", img.size)
	px_result = result.load()

	for i in range(img.size[0]):
		for j in range(img.size[1]):
			px_result[i, j] = (px[i, j][0], px[i, j][1], px[i, j][2], px_alpha[i, j]) if combine else (px[i, j][0], px[i, j][1], px[i, j][2])

	return result

#
#  As above, but with paths instead to save typing. WARNING: extensions are required!
#

def combine_alpha_path(img_path, alpha_path, result_path):
	make_dir(result_path)

	try:
		img = Image.open(fix_path(img_path))
	except:
		print("Unknown image: " + fix_path(img_path))
		return False

	try:
		alpha = Image.open(fix_path(alpha_path))
	except:
		alpha = None
	combine_alpha(img, alpha).save(result_path)

	return True

#
#  As above, but these are read from a *.spr file. Also generates a sprite file.
#

def combine_alpha_sprite(sprite_path, out_sprite_path, out_image_path):
	sprite_data = {
		"$schema": "",
		"image": "",
		"frameSize": {"x":1,"y":1},
		"states": [],
		"batched": False
	}

	contents = get_contents(sprite_path)
	result = combine_alpha_path(contents[0], contents[1], out_image_path)
	if not result:
		return

	sprite_data["$schema"] = "../" * len(out_image_path.split("/")) + "schemas/sprite.json"
	sprite_data["image"] = "/".join(out_image_path.split("/")[1:])
	sprite_data["frameSize"]["x"] = int(contents[2].split(" ")[0])
	sprite_data["frameSize"]["y"] = int(contents[2].split(" ")[1])
	for i in range(int(contents[3])):
		n = 4 + i * 2
		state = {"pos":{"x":0,"y":0},"frames":{"x":1,"y":1}}
		state["pos"]["x"] = int(contents[n + 1].split(" ")[0])
		state["pos"]["y"] = int(contents[n + 1].split(" ")[1])
		state["frames"]["x"] = int(contents[n])
		sprite_data["states"].append(state)

	# hacks for various sprites
	if sprite_path == FDATA + "/sprites/particles/speed_shot_beam.spr":
		sprite_data["states"][0]["frames"]["x"] = 1

	result_path = out_sprite_path
	store_contents(result_path, sprite_data)

#
#  Takes (path.obj) file contents and returns a list of vertices in {x:, y:} form.
#

def convert_path(contents):
	vertices = []
	vertex_order = []

	for words in preprocess_contents(contents):
		if words[0] == "v":
			vertices.append({"x":float(words[1]),"y":-float(words[2]),"hidden":False})
		if words[0] == "f":
			for i in range(len(words) - 1):
				vertex_order.append(int(words[i + 1]))

	result = []
	for vertex_id in vertex_order:
		result.append(vertices[vertex_id - 1])

	result.reverse()

	return {"nodes": result}

#
#  Takes (level_x_y.lvl) file contents and returns level data.
#

def convert_level(contents):
	level_data = {
		"$schema": "../../../schemas/level.json",
		"map": "",
		"sequence": "level_sequences/adventure.json",
		"music": "music_tracks/level_music.json",
		"dangerMusic": "music_tracks/danger_music.json",
		"dangerSound": "sound_events/warning.json",
		"warmupLoopSound": "sound_events/spheres_roll.json",
		"failSound": "sound_events/foul.json",
		"failLoopSound": "sound_events/spheres_roll.json",
		"colorGeneratorNormal": "color_generators/default.json",
		"colorGeneratorDanger": "color_generators/danger.json",
		"matchEffect": "sphere_effects/match.json",
		"objectives": [
			{
				"type": "destroyedSpheres",
				"target": 0
			}
		],
		"variables": {},
		"pathsBehavior": [
			{
				"trainRules": {
					"type": "random",
					"colors": [],
					"colorStreak": 0,
					"forceDifferentColor": True,
					"length": 0
				},
				"spawnDistance": 0,
				"dangerDistance": 0.75,
				"speeds": []
			},
			{
				"trainRules": {
					"type": "random",
					"colors": [],
					"colorStreak": 0,
					"forceDifferentColor": True,
					"length": 0
				},
				"spawnDistance": 0,
				"dangerDistance": 0.75,
				"speeds": []
			}
		]
	}

	viseMaxSpeed = 0
	viseMidMaxSpeed = 0
	viseMidMinSpeed = 0
	viseMinSpeed = 0
	viseSpeedMaxBzLerp = [0, 0]
	viseSpeedMidBzLerp = [0, 0]
	viseSpeedMinBzLerp = [0, 0]
	midStartDistance1 = 0
	midStartDistance2 = 0
	midEndDistance1 = 0
	midEndDistance2 = 0

	for words in preprocess_contents(contents):
		if words[0] == "mapFile":
			level_data["map"] = convert_pascal(" ".join(words[2:])[1:-1]).replace("'", "")
		if words[0].startswith("spawnColor_") and words[2] == "true":
			level_data["pathsBehavior"][0]["trainRules"]["colors"].append(int(words[0][11:]))
			level_data["pathsBehavior"][1]["trainRules"]["colors"].append(int(words[0][11:]))
		if words[0].startswith("powerup_") and words[2] == "true":
			level_data["variables"]["spawn_" + words[0][8:]] = True
		if words[0].startswith("reward_") and words[2] == "true":
			level_data["variables"]["spawn_" + words[0][7:]] = True
		if words[0] == "spawnStreak":
			level_data["pathsBehavior"][0]["trainRules"]["colorStreak"] = 0.5 #min(int(words[2]) / 300, 0.5)
			level_data["pathsBehavior"][1]["trainRules"]["colorStreak"] = 0.5 #min(int(words[2]) / 300, 0.5)
		if words[0] == "winCondition":
			level_data["objectives"][0]["target"] = int(words[2])
		if words[0] == "viseGroupCount":
			level_data["pathsBehavior"][0]["trainRules"]["length"] = int(words[2])
			level_data["pathsBehavior"][1]["trainRules"]["length"] = int(words[2])
		if words[0] == "viseSpawnDistance_1":
			level_data["pathsBehavior"][0]["spawnDistance"] = float(words[2])
		if words[0] == "viseSpawnDistance_2":
			level_data["pathsBehavior"][1]["spawnDistance"] = float(words[2])
		if words[0] == "viseMaxSpeed":
			viseMaxSpeed = float(words[2])
		if words[0] == "viseMidMaxSpeed":
			viseMidMaxSpeed = float(words[2])
		if words[0] == "viseMidMinSpeed":
			viseMidMinSpeed = float(words[2])
		if words[0] == "viseMinSpeed":
			viseMinSpeed = float(words[2])
		if words[0] == "viseSpeedMaxBzLerp":
			viseSpeedMaxBzLerp = [float(words[2]), float(words[3])]
		if words[0] == "viseSpeedMidBzLerp":
			viseSpeedMidBzLerp = [float(words[2]), float(words[3])]
		if words[0] == "viseSpeedMinBzLerp":
			viseSpeedMinBzLerp = [float(words[2]), float(words[3])]
		if words[0] == "midStartDistance_1":
			midStartDistance1 = float(words[2])
		if words[0] == "midStartDistance_2":
			midStartDistance2 = float(words[2])
		if words[0] == "midEndDistance_1":
			midEndDistance1 = float(words[2])
		if words[0] == "midEndDistance_2":
			midEndDistance2 = float(words[2])

	level_data["pathsBehavior"][0]["speeds"].append({"distance":0,"speed":viseMaxSpeed,"transition":{"type":"bezier","point1":viseSpeedMaxBzLerp[0],"point2":viseSpeedMaxBzLerp[1]}})
	level_data["pathsBehavior"][0]["speeds"].append({"distance":midStartDistance1,"speed":viseMidMaxSpeed,"transition":{"type":"bezier","point1":viseSpeedMidBzLerp[0],"point2":viseSpeedMidBzLerp[1]}})
	level_data["pathsBehavior"][0]["speeds"].append({"distance":midEndDistance1,"speed":viseMidMinSpeed,"transition":{"type":"bezier","point1":viseSpeedMinBzLerp[0],"point2":viseSpeedMinBzLerp[1]}})
	level_data["pathsBehavior"][0]["speeds"].append({"distance":1,"speed":viseMinSpeed})

	level_data["pathsBehavior"][1]["speeds"].append({"distance":0,"speed":viseMaxSpeed,"transition":{"type":"bezier","point1":viseSpeedMaxBzLerp[0],"point2":viseSpeedMaxBzLerp[1]}})
	level_data["pathsBehavior"][1]["speeds"].append({"distance":midStartDistance2,"speed":viseMidMaxSpeed,"transition":{"type":"bezier","point1":viseSpeedMidBzLerp[0],"point2":viseSpeedMidBzLerp[1]}})
	level_data["pathsBehavior"][1]["speeds"].append({"distance":midEndDistance2,"speed":viseMidMinSpeed,"transition":{"type":"bezier","point1":viseSpeedMinBzLerp[0],"point2":viseSpeedMinBzLerp[1]}})
	level_data["pathsBehavior"][1]["speeds"].append({"distance":1,"speed":viseMinSpeed})

	# Fix the map name.
	for name in MAP_NAMES:
		if level_data["map"].lower() == name.lower():
			level_data["map"] = name
			break

	# Don't include the second path behavior if it's not included in the level file.
	if level_data["pathsBehavior"][1]["spawnDistance"] == 0:
		level_data["pathsBehavior"].pop()

	return level_data

#
#  Takes map.ui file contents and returns map data.
#

def convert_map(contents):
	map_data = {
		"$schema": "../../../../schemas/map.json",
		"name": "",
		"paths": [],
		"objects": []
	}

	particle_data = None

	for words in preprocess_contents(contents):
		if particle_data != None:
			if words[0] == "X":
				particle_data["x"] = int(words[2])
			if words[0] == "Y":
				particle_data["y"] = int(words[2])
			if words[0] == "Depth":
				particle_data["layer"] = words[2]
			if words[0] == "File":
				particle_data["particle"] = resolve_path_particle(words[2])
			if words[0] == "}":
				map_data["objects"].append(particle_data)
				particle_data = None
		if words[0] == "MapName":
			map_data["name"] = " ".join(words[2:])[1:-1]
		if words[0] == "Sprite":
			map_data["objects"].append({"type": "sprite", "x": 0, "y": 0, "sprite": resolve_path_sprite(words[2]), "layer": "GameBackground"})
		if words[0] == "Depth":
			map_data["objects"][0]["layer"] = words[2]
		if words[0] == "GLSprite":
			map_data["objects"].append({"type": "sprite", "x": int(words[2]), "y": int(words[3]), "sprite": resolve_path_sprite(words[5]), "layer": words[4]})
		if words[0] == "Path":
			map_data["paths"].append(convert_path(get_contents(fix_path(words[2]))))
		if words[0] == "Node":
			map_data["paths"][int(words[2])]["nodes"][int(words[3])]["hidden"] = True
		if words[0] == "Child" and words[3] == "uiParticleSystem":
			particle_data = {"type": "particle"}

	return map_data

#
#  Takes the given path to .font file and converts it to OpenSMCE format.
#

def convert_font(input_path, output_path):
	font_data = {
		"$schema":"../../../schemas/font.json",
		"type":"image",
		"image":"",
		"characters":{}
	}

	contents = get_contents(input_path)

	image_name = contents[0].replace("\\", "/").replace("data/bitmaps", "images")[:-4]
	combine_alpha_path(contents[0].replace("\\", "/"), contents[1].replace("\\", "/"), "output/" + image_name + ".png")
	font_data["image"] = image_name + ".png"

	for i in range((len(contents) - 4) // 2):
		char = contents[i * 2 + 4]
		params = contents[i * 2 + 5].split(" ")
		font_data["characters"][char] = {"offset":int(params[0]),"width":int(params[2])}

	store_contents(output_path, font_data)

# A list of UI widget types mapped to OpenSMCE widget types.
UI_WIDGET_TYPES = {
	"uiNonVisualWidget": "none",
	"uiAnimDialog": "none",
	"uiVisualWidget": "sprite",
	"uiStageMap": "sprite",
	"uiTextWidget": "text",
	"uiEntryWidget": "textInput",
	"uiButton": "spriteButton",
	"uiRadioButton": "spriteButton", # TODO: At some point, add radio button support to OpenSMCE.
	"uiToggleButton": "spriteButtonCheckbox",
	"uiSliderButton": "spriteButtonSlider",
	"uiProgressBar": "spriteProgress",
	"uiProgressBar_Giza": "spriteProgress",
	"uiParticleSystem": "particle"
}

#
#  Takes .ui file contents and returns UI script data.
#

def convert_ui(contents, full_name = None):
	ui_data = {
		"name": "",
		"type": "none",
		"pos": {"x": 0, "y": 0},
		"alpha": 1,
		"children": [],
		"sounds": {}
	}
	sub_anim_uis = {}

	child_scan = False
	child_scan_level = 0
	child_contents = []

	first_line = True

	button_layer = None # Hack for stagemap scriptlet layering

	for words in preprocess_contents(contents):
		if child_scan:
			# If we're at 0, we've encountered a Child and not a single curly brace yet.
			# Ignore everything that happens between the Child line and the first curly brace.
			if child_scan_level > 0:
				child_contents.append(" ".join(words))
			if words[0] == "{":
				child_scan_level += 1
			if words[0] == "}":
				child_scan_level -= 1 # protection for nested children
				if child_scan_level == 0:
					child_scan = False
					ui_data["children"].append(convert_ui(child_contents, full_name))
			continue
		
		if first_line:
			# First line is always NAME = TYPE. Extract relevant information.
			ui_data["name"] = words[0]
			if full_name == None:
				full_name = ui_data["name"]
			else:
				full_name += "." + ui_data["name"]

			if words[2] in UI_WIDGET_TYPES:
				ui_data["type"] = UI_WIDGET_TYPES[words[2]]
			else:
				print("!! Unknown UI widget type! " + words[2])
			first_line = False
			continue

		if words[0] == "X":
			ui_data["pos"]["x"] = int(words[2])
		if words[0] == "Y":
			ui_data["pos"]["y"] = int(words[2])
		if words[0] == "Flags":
			if words[2] == "WF_ROOT_COORDS":
				ui_data["inheritPos"] = False
		if words[0] == "AnimIn" and words[1] == "Sound":
			ui_data["sounds"]["in"] = "sound_events/" + words[3] + ".json"
		if words[0] == "AnimOut" and words[1] == "Sound":
			ui_data["sounds"]["out"] = "sound_events/" + words[3] + ".json"
		if words[0] == "Depth" and words[2] != "#Parent":
			ui_data["layer"] = words[2]
		if words[0] == "DepthButton":
			button_layer = words[2] # Used in conjunction with #Scriptlet
		if words[0] == "Text":
			ui_data["text"] = " ".join(words[2:])[1:-1].replace("\\n", "\n")
		if words[0] == "Sprite":
			ui_data["sprite"] = resolve_path_sprite(words[2])
		if words[0] == "Sprite2":
			ui_data["sprite"] = [ui_data["sprite"], resolve_path_sprite(words[2])]
		if words[0] == "Font":
			ui_data["font"] = resolve_path_font(words[2])
		if words[0] == "Cursor":
			ui_data["cursorSprite"] = resolve_path_sprite(words[2])
		if words[0] == "Justify":
			ui_data["align"] = {"LEFT":{"x":0,"y":0},"CENTER":{"x":0.5,"y":0},"RIGHT":{"x":1,"y":0}}[words[2]]
		if words[0] == "Smooth":
			ui_data["smooth"] = words[2] == "true"
		if words[0] == "MinX":
			ui_data["bounds"] = [int(words[2]), 0]
		if words[0] == "MaxX":
			ui_data["bounds"][1] = int(words[2])
		if words[0] == "Hotkey":
			ui_data["hotkey"] = KEYS[words[2]]
		if words[0] == "EntryWidth":
			ui_data["maxLength"] = int(words[2])
		if words[0] == "File":
			ui_data["path"] = resolve_path_particle(words[2])
		if words[0] == "Psys": # Strictly for the progress bar
			ui_data["children"].append({"name": "_Particle", "type": "particle", "path": resolve_path_particle(words[2])})
		if words[0] == "#Scriptlet":
			if words[1] == "data\\uiscript\\stage_select.uis":
				ui_data["children"].append({"name": "_Scriptlet", "type": "none", "layer": button_layer, "children": ["ui/stage_select.json"]})
			else:
				print("!! Unknown UI scriptlet! " + words[1])
		if words[0] == "Child":
			if len(words[1]) > 0 and words[1][0] == "#":
				# Include from another file.
				ui_data["children"].append(resolve_path_ui(words[1][1:]))
			else:
				child_scan = True
				child_scan_level = 0
				child_contents = [" ".join(words[1:])]



		if words[0] == "SubAnimIn":
			# Create an entry to hold animations.
			if not "animations" in ui_data:
				ui_data["animations"] = {"in": [], "out": []}
			# Get animation ID and add it to the list if there's no such animation yet.
			anim_id = int(words[1])
			if len(ui_data["animations"]["in"]) <= anim_id:
				ui_data["animations"]["in"].append({})
				ui_data["animations"]["out"].append({})
			# Get animation data.
			anim = ui_data["animations"]["in"][anim_id]
			anim_out = ui_data["animations"]["out"][anim_id]

			# Parse stuff.
			if words[2] == "Widget":
				sub_ui = ui_data
				sub_ui_nav = words[4].split(".")[1:]
				for nav in sub_ui_nav:
					sub_ui = get_ui_child(sub_ui, nav)
				sub_anim_uis[words[1]] = sub_ui
				anim["target"] = "/".join(sub_ui_nav)
				anim_out["target"] = "/".join(sub_ui_nav)
			if words[2] == "SpriteDepth":
				sub_anim_uis[words[1]]["layer"] = words[4]
			if words[2] == "Style":
				style_types = {
					"AlphaFade": "fade",
					"SpriteMask": "fade",
					"BezierLerp": "move"
				}
				if words[4] in style_types:
					style_type = style_types[words[4]]
				else:
					print("!! Unknown style type! " + words[4])
					style_type = "none"
				# Create a background child for animation if this is a mask.
				if words[4] == "SpriteMask":
					if not "children" in sub_anim_uis[words[1]]:
						sub_anim_uis[words[1]]["children"] = []
					sub_anim_uis[words[1]]["children"].append({"name": "_Mask", "type": "none", "children": ["ui/background.json"]})
					sub_anim_uis[words[1]] = get_ui_child(sub_anim_uis[words[1]], "_Mask")
					anim["target"] += "/_Mask"
					anim_out["target"] += "/_Mask"
				# Fill in animation info for the animated Widget.
				anim["type"] = style_type
			if words[2] == "Time":
				anim["time"] = int(words[4]) / 1000
			if words[2] == "Loc" and anim["type"] == "move":
				anim["endPos"] = {"x":int(words[4]),"y":int(words[5])}
				anim_out["startPos"] = {"x":int(words[4]),"y":int(words[5])}
			if words[2] == "AlphaStart" and anim["type"] == "fade":
				anim["startValue"] = int(words[4]) / 255
			if words[2] == "AlphaTarget" and anim["type"] == "fade":
				anim["endValue"] = int(words[4]) / 255
			if words[2] == "BezierControls":
				anim["transition"] = {"type": "bezier", "point1": float(words[4]), "point2": float(words[5])}
		if words[0] == "SubAnimOut":
			# Get animation ID.
			anim_id = int(words[1])
			# Get animation data.
			anim = ui_data["animations"]["out"][anim_id]
			anim_in = ui_data["animations"]["in"][anim_id]

			# Parse stuff.
			if words[2] == "Style":
				style_types = {
					"AlphaFade": "fade",
					"SpriteMask": "fade",
					"BezierLerp": "move"
				}
				if words[4] in style_types:
					style_type = style_types[words[4]]
				else:
					print("!! Unknown style type! " + words[4])
					style_type = "none"
				anim["type"] = style_type
			if words[2] == "Time":
				anim["time"] = int(words[4]) / 1000
			if words[2] == "Loc" and anim["type"] == "move":
				anim_in["startPos"] = {"x":int(words[4]),"y":int(words[5])}
				anim["endPos"] = {"x":int(words[4]),"y":int(words[5])}
			if words[2] == "AlphaStart" and anim["type"] == "fade":
				anim["startValue"] = int(words[4]) / 255
			if words[2] == "AlphaTarget" and anim["type"] == "fade":
				anim["endValue"] = int(words[4]) / 255
			if words[2] == "BezierControls":
				anim["transition"] = {"type": "bezier", "point1": float(words[4]), "point2": float(words[5])}
	
	# Text widgets are actually aligned to left by default if no JUSTIFY is specified.
	if ui_data["type"] == "text" and not "align" in ui_data:
		ui_data["align"] = {"x": 0, "y": 0}

	# Sometimes there are sprite widgets which don't actually have any sprite. Fix this here.
	if ui_data["type"] == "sprite" and not "sprite" in ui_data:
		ui_data["type"] = "none"

	# Hardcoded additions which don't make sense to be put elsewhere.
	if full_name == "Main.Menu":
		ui_data["type"] = "level"
		ui_data["path"] = "levels/level_0_0.json"
	if full_name == "Menu_Options.Frame.Slot_sfx.Slider_Effects":
		ui_data["releaseSound"] = "sound_events/catch_powerup_shot_speed.json"
	
	# Remove empty fields or fields with default values.
	if ui_data["type"] == "none":
		del ui_data["type"]
	if ui_data["pos"] == {"x": 0, "y": 0}:
		del ui_data["pos"]
	if ui_data["alpha"] == 1:
		del ui_data["alpha"]
	if ui_data["children"] == []:
		del ui_data["children"]
	if ui_data["sounds"] == {}:
		del ui_data["sounds"]
	if "text" in ui_data and ui_data["text"] == "":
		del ui_data["text"]

	return ui_data

#
#  Takes .uis file contents and returns UI script data for the stagemap, as well as saves an output/ui/stage_names.json file and a level_sets/adventure.json file.
#

def convert_ui_script(contents):
	ui_data = {
		"name": "Stage_Select",
		"children": [
			{"name": "StageButtons", "children": []},
			{"name": "LevelButtons", "children": []}
		]
	}
	level_set_data = {
		"$schema": "../../../schemas/level_set.json",
		"levelOrder": []
	}
	stage_names = []
	stage_lengths = []
	level = 1

	for words in preprocess_contents(contents):
		if words[0] == "LevelPsys":
			ui_data["children"].append({"name": "LevelPsys", "type": "particle", "path": resolve_path_particle(words[2])})
		if words[0] == "StagePsys":
			ui_data["children"].append({"name": "StageUnlockPsys", "type": "particle", "path": resolve_path_particle(words[2])})
		if words[0] == "StageCompletePsys":
			ui_data["children"].append({"name": "StageCompletePsys", "type": "particle", "pos": {"x": 400, "y": 300}, "path": resolve_path_particle(words[2])})
		if words[0] == "Stage":
			stage_buttons = get_ui_child(ui_data, "StageButtons")
			stage_buttons["children"].append({"name": words[1], "type": "spriteButton", "neverDisabled": True, "pos": {"x": int(words[3]), "y": int(words[4])}, "sprite": resolve_path_sprite(words[6])})
			if not words[-1].endswith("\""):
				stage_names.append(" ".join(words[7:-3])[1:-1])
				ui_data["children"].append({"name": "Set", "type": "sprite", "pos": {"x": int(words[-2]), "y": int(words[-1])}, "sprite": resolve_path_sprite(words[-3])})
			else:
				stage_names.append(" ".join(words[7:])[1:-1])
			stage_lengths.append(words[5])
		if words[0] == "Level":
			level_buttons = get_ui_child(ui_data, "LevelButtons")
			level_buttons["children"].append({"name": str(level), "type": "spriteButton", "neverDisabled": True, "pos": {"x": int(words[4]), "y": int(words[5])}, "sprite": "sprites/dialogs/button_level.json"})
			level += 1
			level_data = {"type": "level", "level": "levels/level_" + words[1] + "_" + words[2] + ".json", "name": words[1] + "-" + words[2]}
			if words[2] == "1":
				level_data["checkpoint"] = {"id": int(words[1])}
				if words[1] == "1":
					level_data["checkpoint"]["unlockedOnStart"] = True
			elif words[2] == stage_lengths[int(words[1]) - 1] and int(words[1]) < len(stage_lengths):
				level_data["unlockCheckpointsOnBeat"] = [int(words[1]) + 1]
			level_set_data["levelOrder"].append(level_data)
	
	store_contents("output/level_sets/adventure.json", level_set_data)
	store_contents("output/ui/stage_names.json", stage_names)
	
	return ui_data

#
#  Takes .psys file contents and returns particle spawner data.
#

def convert_psys(contents):
	particle_data = {
		"$schema": "../../../schemas/particle_effect.json",
		"emitters": []
	}

	spawner_name = None
	spawner_data = None
	spawner_flags = []

	lifespan_min = 0.0
	lifespan_max = 0.0
	spawn_radius_min_x = 0
	spawn_radius_min_y = 0
	spawn_radius_max_x = 0
	spawn_radius_max_y = 0
	start_vel_min_x = 0
	start_vel_min_y = 0
	start_vel_max_x = 0
	start_vel_max_y = 0
	dev_delay = 0
	dev_angle_min = 0
	dev_angle_max = 0
	emitter_vel_min_x = 0
	emitter_vel_min_y = 0
	emitter_vel_max_x = 0
	emitter_vel_max_y = 0

	for words in preprocess_contents(contents):
		if spawner_name == None:
			if words[0] == "Emitter":
				spawner_name = words[1]
				spawner_data = {
					#"name":spawner_name,
					"pos":{"x":0,"y":0},
					"speed":{"x":0,"y":0},
					"acceleration":{"x":0,"y":0},
					"lifespan":None,
					"spawnCount":1,
					"spawnMax":1,
					#"spawnDelay":None,
					"particleData":{
						"movement":{
							"type":"loose",
							"speed":{"x":0,"y":0},
							"acceleration":{"x":0,"y":0}
						},
						"spawnScale":{"x":0,"y":0},
						"lifespan":None,
						"sprite":"",
						"animationFrameCount":1,
						"animationSpeed":0,
						"animationLoop":False,
						"animationFrameRandom":False,
						"fadeTime":None,
						"fadeInPoint":0,
						"fadeOutPoint":1,
						"posRelative":False
					}
				}
			else:
				print("Unknown type: " + words[0])
			continue

		if words[0] == "}":
			spawner_data["particleData"]["lifespan"] = collapse_random_number(lifespan_min, lifespan_max, True)
			spawner_data["particleData"]["spawnScale"] = collapse_random_vector(spawn_radius_min_x, spawn_radius_min_y, spawn_radius_max_x, spawn_radius_max_y, True)
			spawner_data["particleData"]["movement"]["speed"] = collapse_random_vector(start_vel_min_x, start_vel_min_y, start_vel_max_x, start_vel_max_y, True)
			spawner_data["speed"] = collapse_random_vector(emitter_vel_min_x, emitter_vel_min_y, emitter_vel_max_x, emitter_vel_max_y, True)

			if "EF_LIFESPAN_INFINITE" in spawner_flags:
				if spawner_data["particleData"]["fadeInPoint"] != 0:
					spawner_data["particleData"]["fadeTime"] = spawner_data["particleData"]["lifespan"]
					spawner_data["particleData"]["fadeOutPoint"] = 1 # Fade out point on infinite lifespan particles must be ignored.
				spawner_data["particleData"]["lifespan"] = None
			if "EF_ELIFESPAN_INFINITE" in spawner_flags:
				spawner_data["lifespan"] = None
			if "EF_POS_RELATIVE" in spawner_flags:
				spawner_data["particleData"]["posRelative"] = True
			if "EF_VEL_POSRELATIVE" in spawner_flags:
				spawner_data["particleData"]["movement"]["type"] = "radius"
			if "EF_SPRITE_ANIM_LOOP" in spawner_flags:
				spawner_data["particleData"]["animationLoop"] = True
			if "EF_SPRITE_RANDOM_FRAME" in spawner_flags:
				spawner_data["particleData"]["animationFrameRandom"] = True
			if "EF_VEL_DEVIATION" in spawner_flags:
				spawner_data["particleData"]["directionDeviationTime"] = dev_delay
				spawner_data["particleData"]["directionDeviationSpeed"] = collapse_random_number(dev_angle_min, dev_angle_max, True)
			if "EF_VEL_ORBIT" in spawner_flags:
				spawner_data["particleData"]["posRelative"] = True
				spawner_data["particleData"]["movement"]["type"] = "circle"
				spawner_data["particleData"]["movement"]["speed"] = spawner_data["particleData"]["movement"]["speed"]["x"]
				spawner_data["particleData"]["movement"]["acceleration"] = spawner_data["particleData"]["movement"]["acceleration"]["x"]

			if spawner_data["particleData"]["lifespan"] == None:
				del spawner_data["particleData"]["lifespan"]
			if spawner_data["particleData"]["fadeTime"] == None:
				del spawner_data["particleData"]["fadeTime"]
			if spawner_data["particleData"]["fadeInPoint"] == 0:
				del spawner_data["particleData"]["fadeInPoint"]
			if spawner_data["particleData"]["fadeOutPoint"] == 1:
				del spawner_data["particleData"]["fadeOutPoint"]

			particle_data["emitters"].append(spawner_data)
			spawner_name = None
			continue

		if words[0] == "Flags":
			spawner_flags = " ".join(words[2:]).split(" | ")
		if words[0] == "StartParticles":
			spawner_data["spawnCount"] = int(words[2])
		if words[0] == "MaxParticles":
			spawner_data["spawnMax"] = int(words[2])
		if words[0] == "ParticleRate" and float(words[2]) > 0:
			spawner_data["spawnDelay"] = 1 / float(words[2])
		if words[0] == "Sprite":
			spawner_data["particleData"]["sprite"] = resolve_path_sprite(words[2])
			sprite_contents = get_contents(words[2])
			spawner_data["particleData"]["animationFrameCount"] = int(sprite_contents[4])
		if words[0] == "Palette":
			image_file = resolve_path_image2(words[2])
			color_palette_file = words[2].replace("\\", "/").replace("data/bitmaps", "color_palettes")
			spawner_data["particleData"]["colorPalette"] = color_palette_file[:-4] + ".json"
			# Create a new Color Palette alongside.
			generate_color_palette(words[2])
		if words[0] == "ColorRate":
			if "EF_USE_COLOR_RATE" in spawner_flags:
				spawner_data["particleData"]["colorPaletteSpeed"] = 1000 / float(words[2])
		if words[0] == "AnimRate":
			spawner_data["particleData"]["animationSpeed"] = 1000 / float(words[2])
		if words[0] == "FadeInEndTime":
			spawner_data["particleData"]["fadeInPoint"] = float(words[2])
		if words[0] == "FadeOutStartTime":
			spawner_data["particleData"]["fadeOutPoint"] = float(words[2])
		if words[0] == "LifespanMin":
			lifespan_min = float(words[2])
		if words[0] == "LifespanMax":
			lifespan_max = float(words[2])
		if words[0] == "PosX":
			spawner_data["pos"]["x"] = float(words[2])
		if words[0] == "PosY":
			spawner_data["pos"]["y"] = float(words[2])
		if words[0] == "SpawnRadiusMin":
			spawn_radius_min_x = float(words[2])
			spawn_radius_min_y = float(words[3])
		if words[0] == "SpawnRadiusMax":
			spawn_radius_max_x = float(words[2])
			spawn_radius_max_y = float(words[3])
		if words[0] == "StartVelMin":
			start_vel_min_x = float(words[2])
			start_vel_min_y = float(words[3])
		if words[0] == "StartVelMax":
			start_vel_max_x = float(words[2])
			start_vel_max_y = float(words[3])
		if words[0] == "Acc":
			spawner_data["particleData"]["movement"]["acceleration"]["x"] = float(words[2])
			spawner_data["particleData"]["movement"]["acceleration"]["y"] = float(words[3])
		if words[0] == "DevDelay":
			dev_delay = float(words[2])
		if words[0] == "DevAngle":
			dev_angle_min = float(words[2]) / 360 * math.pi * 2
			dev_angle_max = float(words[3]) / 360 * math.pi * 2
		if words[0] == "EmitterVelMin":
			emitter_vel_min_x = float(words[2])
			emitter_vel_min_y = float(words[3])
		if words[0] == "EmitterVelMax":
			emitter_vel_max_x = float(words[2])
			emitter_vel_max_y = float(words[3])
		if words[0] == "EmitterAcc":
			spawner_data["acceleration"]["x"] = float(words[2])
			spawner_data["acceleration"]["y"] = float(words[3])
		if words[0] == "EmitterLifespan":
			spawner_data["lifespan"] = collapse_random_number(float(words[2]), float(words[3]), True)

	return particle_data

#
#  Takes (sounds.sl3) file contents and generates sound events that can be saved.
#

def convert_sounds_from_sl3(contents):
	looping_sounds = ["bonus_scarab_move", "spheres_roll"]

	events = {}
	name = ""
	param_mode = False

	for words in preprocess_contents(contents):
		if words[0] == "{":
			param_mode = True
		elif words[0] == "}":
			param_mode = False
		else:
			if param_mode:
				event = events[name]
				if words[0] == "volume":
					event["volume"] = float(words[2])
				else:
					print("Unknown sound parameter: " + words[0] + " in sound event: " + name)
			else:
				name = words[0]

				event = {
					"$schema": "../../../schemas/sound_event.json",
					"sound": resolve_path_sound(words[3])
				}
				if name in looping_sounds:
					event["loop"] = True
				if name == "collapse_scarab":
					# collapse_scarab sound event also has a condition.
					event["sounds"] = [{"sound": event["sound"], "conditions": ["${[sphere.crushed|true]}"]}]
					del event["sound"]

				events[name] = event

	return events

#
#  Takes (music.sl3) file contents and generates music tracks that can be saved.
#

def convert_music_from_sl3(contents):
	tracks = {}
	playlists = {}
	name = ""
	param_mode = False
	current_track = None
	current_playlist = None

	for words in preprocess_contents(contents):
		if words[0] == "{":
			param_mode = True
			continue
		if words[0] == "}":
			# End of parameters. Save the current track/playlist and move on.
			if current_track != None:
				tracks[name] = current_track
				current_track = None
			if current_playlist != None:
				playlists[name] = current_playlist
				current_playlist = None
			param_mode = False
			continue
		if param_mode:
			if words[0] == "track":
				current_playlist["tracks"].append("music_tracks/" + words[2] + ".json")
		else:
			name = words[0]
			if words[2] == "stream":
				current_track = {"$schema": "../../../schemas/music_track.json", "audio": resolve_path_music(words[3])}
			if words[2] == "playlist":
				current_playlist = {"$schema": "../../../schemas/music_playlist.json", "tracks": []}

	return {"tracks": tracks, "playlists": playlists}

#
#  Takes the levels/powerups.txt file contents and SAVES to collectible_generators/vanilla_powerup.json as well as score_events/coin.json and score_events/gem_X.json.
#  Converts powerup weights and score values for gems and coins.
#

def convert_powerups(contents):
	# Maps powerup types to collectible entries.
	POWERUPS = {
		"reverse": {"type": "collectible", "collectible": "collectibles/reverse.json", "conditions": ["${[level.spawn_reverse]}"]},
		"slow": {"type": "collectible", "collectible": "collectibles/slow.json", "conditions": ["${[level.spawn_slow]}"]},
		"stop": {"type": "collectible", "collectible": "collectibles/stop.json", "conditions": ["${[level.spawn_stop]}"]},
		"speed_shot": {"type": "collectible", "collectible": "collectibles/speedshot.json", "conditions": ["${[level.spawn_shotspeed]}"]},
		"lightning": {"type": "collectible", "collectible": "collectibles/lightning.json", "conditions": ["${[level.spawn_lightning]}"]},
		"bomb": {"type": "collectible", "collectible": "collectibles/fireball.json", "conditions": ["${[level.spawn_bomb]}"]},
		"color_bomb": {"type": "collectibleGenerator", "generator": "collectible_generators/vanilla_powerup_colorbomb.json", "conditions": ["${[level.spawn_colorbomb]}"]},
		"wild": {"type": "collectible", "collectible": "collectibles/wild.json", "conditions": ["${[level.spawn_wild]}"]},
		"scorpion": {"type": "collectible", "collectible": "collectibles/scorpion.json", "conditions": ["${[level.spawn_scorpion]}"]}
	}

	generator_data = {
		"$schema": "../../../schemas/collectible_generator.json",
		"type": "randomPick",
		"pool": []
	}

	for words in preprocess_contents(contents):
		if words[0].startswith("spawn_"):
			generator_data["pool"].append({"entry": POWERUPS[words[0][6:]], "weight": int(words[2])})
		if words[0].startswith("scoring_"):
			event_data = {"$schema": "../../../schemas/score_event.json", "score": int(words[2]), "font": "fonts/score0.json"}
			store_contents("output/score_events/" + words[0][8:] + ".json", event_data)
	
	store_contents("output/collectible_generators/vanilla_powerup.json", generator_data)

#
#  Takes the uiscript/depths.txt file contents and returns the config/layers.json file contents.
#  Converts the layer list.
#

def convert_layers(contents):
	layer_data = {"$schema": "../../../schemas/config/layers.json", "layers": []}

	for words in preprocess_contents(contents):
		if words[0].startswith("\"") and words[0].endswith("\""):
			layer_data["layers"].append(words[0][1:-1])
	
	return layer_data

# Maps sphere IDs to next sphere sprites.
SHOOTER_NEXT_BALLS = {
	-3: "sprites/game/next_ball_lightning.json",
	-2: "sprites/game/next_ball_bomb.json",
	-1: "sprites/game/next_ball_wild.json",
	0: "sprites/game/next_ball_0.json",
	1: "sprites/game/next_ball_1.json",
	2: "sprites/game/next_ball_2.json",
	3: "sprites/game/next_ball_3.json",
	4: "sprites/game/next_ball_4.json",
	5: "sprites/game/next_ball_5.json",
	6: "sprites/game/next_ball_6.json",
	7: "sprites/game/next_ball_7.json"
}

#
#  Takes the uiscript/game.ui file contents, loads the sprites/game/next_ball_0.spr and sprites/game/shooter.spr files for width measurement, and returns the shooters/default.json file contents.
#

def convert_shooter(contents):
	# Measure shooter and next sphere width.
	shooter_sprite = preprocess_contents(get_contents(FDATA + "/sprites/game/shooter.spr"))
	next_sprite = preprocess_contents(get_contents(FDATA + "/sprites/game/next_ball_0.spr"))
	shooter_width = int(shooter_sprite[2][0])
	shooter_height = int(shooter_sprite[2][1])
	next_width = int(next_sprite[2][0])

	shooter_data = {
		"$schema": "../../../schemas/shooter.json",
		"movement": {"type": "linear", "xMin": 20, "xMax": 780, "y": 526, "angle": 0},
		"sprites": [
			{"sprite": "sprites/game/shooter.json", "layer": "GamePlayerBase", "offset": {"x": 0, "y": 0}, "anchor": {"x": 0.5, "y": 0}},
			{"sprite": "sprites/game/shooter_shadow.json", "layer": "GamePlayerBaseShadow", "offset": {"x": 4, "y": 4}, "anchor": {"x": 0.5, "y": 0}}
		],
		"spheres": [{"pos": {"x": 0, "y": 5}}],
		"speedShotBeam": {"sprite": "sprites/particles/speed_shot_beam.json", "fadeTime": 0.5, "renderingType": "cut", "colored": False},
		"sounds": {"sphereSwap": "sound_events/bullet_swap.json", "sphereFill": "sound_events/bullet_reload.json"},
		"speedShotParticle": "particles/speed_shot_beam.json",
		"shotSpeed": 1000,
		"shotCooldownFade": 0.1,
		"destroySphereOnFail": True,
		"hitboxSize": {"x": shooter_width, "y": shooter_height},
		"hitboxOffset": {"x": 0, "y": shooter_height // 2}
	}

	current_child = None
	next_sphere_offset = {"x": 0, "y": 0}

	for words in preprocess_contents(contents):
		if words[0] == "Child":
			current_child = words[1]
		if current_child == "PlayerBase":
			if words[0] == "Y":
				shooter_data["movement"]["y"] = int(words[2])
			if words[0] == "Depth":
				shooter_data["sprites"][0]["layer"] = words[2]
			if words[0] == "ShadowDepth":
				shooter_data["sprites"][1]["layer"] = words[2]
			if words[0] == "SpeedShotDepth":
				shooter_data["speedShotBeam"]["layer"] = words[2]
				shooter_data["speedShotParticleLayer"] = words[2]
			if words[0] == "BulletOffset":
				shooter_data["spheres"][0]["pos"]["y"] = int(float(words[2]))
			if words[0] == "NextBulletOffset":
				next_sphere_offset = {"x": int(words[2]) - (shooter_width - next_width) // 2, "y": int(words[3])}
	
	for next_ball in SHOOTER_NEXT_BALLS:
		sprite = {
			"sprite": SHOOTER_NEXT_BALLS[next_ball],
			"layer": shooter_data["sprites"][0]["layer"],
			"offset": next_sphere_offset,
			"anchor": {"x": 0.5, "y": 0},
			"conditions": ["${[shooter.nextColor] == " + str(next_ball) + "}"]
		}
		shooter_data["sprites"].append(sprite)

	return shooter_data

# Maps sphere IDs to sphere data.
SPHERES = {
	-3: {
		"sprite": "sprites/game/ball_lightning.json",
		"animationSpeed": 16,
		"rotate": False,
		"idleParticle": "particles/idle_ball_lightning.json",
		"destroyParticle": "particles/lightning_beam.json",
		"color": {"r": 0.7, "g": 0.8, "b": 1},
		"shotBehavior": {"type": "destroySpheres", "selector": "sphere_selectors/lightning.json", "scoreEvent": "score_events/lightning.json"},
		"shotEffects": [{"type": "setStreak", "streak": 0}],
		"shotSound": "sound_events/launch_lightning.json",
		"matches": [-1, 1, 2, 3, 4, 5, 6, 7]
	},
	-2: {
		"sprite": "sprites/game/ball_fire.json",
		"animationSpeed": 16,
		"rotate": False,
		"idleParticle": "particles/idle_ball_bomb.json",
		"destroyParticle": "particles/collapse_ball_bomb.json",
		"colorPalette": "color_palettes/powerups/fire_pal.json",
		"colorPaletteSpeed": 64,
		"shotSound": "sound_events/launch_fireball.json",
		"hitBehavior": {"type": "destroySpheres", "selector": "sphere_selectors/fireball.json", "scoreEvent": "score_events/fireball.json"},
		"hitSound": "sound_events/collapse_fireball.json",
		"matches": [-1, 1, 2, 3, 4, 5, 6, 7]
	},
	-1: {
		"sprite": "sprites/game/ball_wild.json",
		"animationSpeed": 16,
		"rotate": False,
		"idleParticle": "particles/idle_ball_wild.json",
		"destroyParticle": "particles/collapse_wild.json",
		"colorPalette": "color_palettes/powerups/wild_pal.json",
		"colorPaletteSpeed": 64,
		"shotSound": "sound_events/launch_wild.json",
		"matches": [-1, 1, 2, 3, 4, 5, 6, 7]
	},
	0: {
		"sprite": "sprites/game/vise.json",
		"animationSpeed": 28.57143,
		"destroyParticle": "particles/collapse_vise.json",
		"destroyCollectible": "collectible_generators/vanilla_scarab.json",
		"destroySound": "sound_events/collapse_scarab.json",
		"color": {"r": 1, "g": 1, "b": 1},
		"matches": []
	},
	1: {"color": {"r": 0, "g": 0, "b": 1}},
	2: {"color": {"r": 1, "g": 1, "b": 0}},
	3: {"color": {"r": 1, "g": 0, "b": 0}},
	4: {"color": {"r": 0, "g": 1, "b": 0}},
	5: {"color": {"r": 1, "g": 0, "b": 1}},
	6: {"color": {"r": 1, "g": 1, "b": 1}},
	7: {"color": {"r": 0, "g": 0, "b": 0}}
}

#
#  Takes the uiscript/game.ui file contents and uses it to generate sphere data.
#

def convert_spheres(contents):
	current_child = None
	shooter_layer = None
	shot_layer = None

	for words in preprocess_contents(contents):
		if words[0] == "Child":
			current_child = words[1]
		if current_child == "Bullet":
			# Both layers of interest are in objects named Bullet, but one is actually Playfield.PlayerBase.Bullet and the other one is Playfield.Bullet.
			if words[0] == "Depth":
				if shooter_layer == None:
					shooter_layer = words[2]
				else:
					shot_layer = words[2]
	
	for color in SPHERES:
		sphere = SPHERES[color]
		sphere_data = {
			"$schema": "../../../schemas/sphere.json",
			"sprites": [
				{
					"sprite": sphere["sprite"] if "sprite" in sphere else "sprites/game/ball_" + str(color) + ".json",
					"shooterLayer": shooter_layer,
					"shotLayer": shot_layer
				}
			]
		}
		if "animationSpeed" in sphere:
			sphere_data["sprites"][0]["animationSpeed"] = sphere["animationSpeed"]
		if "rotate" in sphere:
			sphere_data["sprites"][0]["rotate"] = sphere["rotate"]
		sphere_data["sprites"].append({"sprite": "sprites/game/ball_shadow.json", "layer": "GamePieceNShadow", "hiddenLayer": "GamePieceHShadow", "shooterLayer": "GamePieceNShadow", "shotLayer": "GamePieceNShadow", "offset": {"x": 4, "y": 4}})

		if "idleParticle" in sphere:
			sphere_data["idleParticle"] = sphere["idleParticle"]
		sphere_data["destroyParticle"] = sphere["destroyParticle"] if "destroyParticle" in sphere else "particles/collapse_ball_" + str(color) + ".json"
		if "destroyCollectible" in sphere:
			sphere_data["destroyCollectible"] = sphere["destroyCollectible"]
		if "destroySound" in sphere:
			sphere_data["destroySound"] = sphere["destroySound"]
		if "color" in sphere:
			sphere_data["color"] = sphere["color"]
		if "colorPalette" in sphere:
			sphere_data["colorPalette"] = sphere["colorPalette"]
		if "colorPaletteSpeed" in sphere:
			sphere_data["colorPaletteSpeed"] = sphere["colorPaletteSpeed"]
		if "shotBehavior" in sphere:
			sphere_data["shotBehavior"] = sphere["shotBehavior"]
		if "shotEffects" in sphere:
			sphere_data["shotEffects"] = sphere["shotEffects"]
		sphere_data["shotSound"] = sphere["shotSound"] if "shotSound" in sphere else "sound_events/launch_sphere.json"
		if "hitBehavior" in sphere:
			sphere_data["hitBehavior"] = sphere["hitBehavior"]
		sphere_data["hitSound"] = sphere["hitSound"] if "hitSound" in sphere else "sound_events/collide_spheres_shot.json"
		sphere_data["matches"] = sphere["matches"] if "matches" in sphere else [-1, color]

		store_contents("output/spheres/sphere_" + str(color) + ".json", sphere_data)

#
#  Takes the english/strings.utf8 file contents and returns the locale/english.json file contents.
#

def convert_locale(contents):
	locale_data = {
		"$schema": "../../../schemas/locale.json",
		"keys": {}
	}

	for words in preprocess_contents(contents):
		spl = " ".join(words).split("\" = \"")
		key = spl[0][1:].replace("\\n", "\n").replace("\\'", "'")
		value = spl[1][:-1].replace("\\n", "\n").replace("\\'", "'").replace("%d-%d", "%s")
		if key == "CHAIN X" or key == "COMBO X":
			value = "\n" + value + "%s"
		if key == "BONUS":
			value = "%s\n" + value
		locale_data["keys"][key] = value
	
	return locale_data

#
#  Takes the scores.dat file contents and returns the runtime.json file contents.
#

def convert_highscores(contents):
	runtime_data = {"highscores": {"entries": []}}

	# Parse the highscore file.
	cursor = 4 # Skip the header
	for i in range(10):
		entry = {"name": "", "level": "", "score": 0}
		# Ignore the index.
		cursor += 4
		# Parse player name.
		for i in range(13):
			if contents[cursor] > 0:
				entry["name"] += chr(contents[cursor])
			cursor += 4
		# Parse level and stage.
		level = contents[cursor] + (contents[cursor + 1] << 8)
		cursor += 2
		stage = contents[cursor] + (contents[cursor + 1] << 8)
		cursor += 2
		entry["level"] = str(stage) + "-" + str(level)
		# Skip unused chunk.
		cursor += 4
		# Parse score.
		for i in range(8):
			entry["score"] += contents[cursor] << i * 8
			cursor += 1
		runtime_data["highscores"]["entries"].append(entry)

	return runtime_data

#
#  Takes a path to the image and generates a Color Palette file pointing to it. Temporary function.
#  Example input: data\bitmaps\powerups\wild_pal.jpg
#

def generate_color_palette(image_path):
	# TODO: Remove this function in favor of loading color palettes in immediate mode.
	new_path = resolve_path_image2(image_path)
	color_palette_data = {
		"$schema": "../" * len(new_path.split("/")) + "schemas/color_palette.json",
		"image": new_path
	}

	# File hierarchy analogic to the image file.
	color_palette_path = new_path.replace("images", "color_palettes")
	store_contents("output/" + color_palette_path[:-4] + ".json", color_palette_data)

	# Convert the image itself, too.
	combine_alpha_path(fix_path(image_path), None, "output/" + new_path)



### Converts sprites and images.
### Input: data/**/*.spr + .tga and .jpg files specified inside
### Output: output/**/*.json + combined output/**/*.png
def convert_sprites(files):
	if files == []:
		for r, d, f in os.walk(FDATA):
			for file in f:
				if not file.endswith(".spr"):
					continue
				files.append(r + "/" + file)

	for file in files:
		print(file)
		combine_alpha_sprite(file, "output/" + resolve_path_sprite(file), "output/" + resolve_path_image(file))

### Converts map files.
### Input: data/maps/*/map.ui
### Output: output/maps/*/config.json
def convert_maps(files):
	if files == []:
		for r, d, f in os.walk(FDATA + "/maps"):
			for file in f:
				if not file.endswith("map.ui"):
					continue
				files.append(r + "/" + file)

	for file in files:
		print(file)
		store_contents("output/" + resolve_path_map(file), convert_map(get_contents(file)))

### Converts level files.
### Input: data/levels/*.lvl
### Output: output/levels/*.json
def convert_levels(files):
	if files == []:
		for r, d, f in os.walk(FDATA + "/levels"):
			for file in f:
				if not file.endswith(".lvl"):
					continue
				files.append(file)

	for file in files:
		print(file)
		store_contents("output/levels/" + file[:-4] + ".json", convert_level(get_contents(FDATA + "/levels/" + file)))

### Converts fonts.
### Input: data/fonts/*.font
### Output: output/fonts/*.json
def convert_fonts(files):
	if files == []:
		for r, d, f in os.walk(FDATA + "/fonts"):
			for file in f:
				if not file.endswith(".font"):
					continue
				files.append(file)

	for file in files:
		print(file)
		convert_font(FDATA + "/fonts/" + file, "output/fonts/" + file[:-5] + ".json")

### Converts particles.
### Input: data/psys/*.psys (minus progress.psys)
### Output: output/particles/*.json
def convert_particles(files):
	if files == []:
		for r, d, f in os.walk(FDATA + "/psys"):
			for file in f:
				if not file.endswith(".psys"):
					continue
				files.append(file)

	for file in files:
		print(file)
		store_contents("output/particles/" + file[:-5] + ".json", convert_psys(get_contents(FDATA + "/psys/" + file)))

### Converts sound events.
### Input: data/sound/sounds.sl3
### Output: output/sound_events/*.json
def convert_sounds(files):
	events = convert_sounds_from_sl3(get_contents(FDATA + "/sound/sounds.sl3"))

	for event_name in events:
		print(event_name)
		store_contents("output/sound_events/" + event_name + ".json", events[event_name])

### Converts music tracks and playlists.
### Input: data/music/music.sl3
### Output: output/music_tracks/*.json, output/music_playlists/*.json
def convert_music(files):
	data = convert_music_from_sl3(get_contents(FDATA + "/music/music.sl3"))

	for n in data["tracks"]:
		print(n)
		store_contents("output/music_tracks/" + n + ".json", data["tracks"][n])

	for n in data["playlists"]:
		print(n)
		store_contents("output/music_playlists/" + n + ".json", data["playlists"][n])

### Converts UI files.
### Input: data/uiscript/*.ui
### Output: output/ui/*.json
def convert_uis(files):
	if files == []:
		for r, d, f in os.walk(FDATA + "/uiscript"):
			for file in f:
				if not file.endswith(".ui"):
					continue
				files.append(file)

	for file in files:
		print(file)
		store_contents("output/ui/" + file[:-3] + ".json", convert_ui(get_contents(FDATA + "/uiscript/" + file)))

### Converts UI scriptlet.
### Input: data/uiscript/stage_select.uis
### Output: output/ui/stage_select.json
def convert_ui_scriptlet(files):
	store_contents("output/ui/stage_select.json", convert_ui_script(get_contents(FDATA + "/uiscript/stage_select.uis")))

### Converts powerup list.
### Input: data/levels/powerups.txt
### Output: output/collectible_generators/vanilla_powerup.json, output/score_events/gem_N.json, output/score_events/coin.json
def convert_powerups_file(files):
	convert_powerups(get_contents(FDATA + "/levels/powerups.txt"))

### Converts layer list.
### Input: data/uiscript/depths.txt
### Output: output/config/layers.json
def convert_layers_file(files):
	store_contents("output/config/layers.json", convert_layers(get_contents(FDATA + "/uiscript/depths.txt")))

### Converts layer list.
### Input: uiscript/game.ui, sprites/game/next_ball_0.spr, sprites/game/shooter.spr
### Output: shooters/default.json
def convert_shooter_file(files):
	store_contents("output/shooters/default.json", convert_shooter(get_contents(FDATA + "/uiscript/game.ui")))

### Converts sphere list.
### Input: uiscript/game.ui
### Output: spheres/sphere_*.json
def convert_sphere_files(files):
	convert_spheres(get_contents(FDATA + "/uiscript/game.ui"))

### Converts locale.
### Input: english/strings.utf8
### Output: locale/english.json
def convert_locale_file(files):
	store_contents("output/locale/english.json", convert_locale(get_contents(FDATA + "/strings.utf8")))

### Converts highscores.
### Input: scores.dat
### Output: runtime.json
def convert_highscores_file(files):
	store_contents("output/runtime.json", convert_highscores(get_binary_contents(FDATA + "/scores.dat")))

### Main conversion function.
def convert(conversion_scope):
	# Sample manual conversion functions:
	# combine_alpha_path("warning.jpg", "warning_alpha.tga", "warning.png")
	# combine_alpha_path("warning2.jpg", "", "warning_gem.png")
	# convert_map(FDATA + "/maps/Demo/map.ui", "output/maps/Demo/config.json")
	# store_contents("output/levels/level_0_0.json", convert_level(get_contents(FDATA + "/levels/level_0_0.lvl")))

	# Generate map names.
	for r, d, f in os.walk(FDATA + "/maps"):
		for directory in d:
			MAP_NAMES.append(directory)

	CONVERSION_FUNCTIONS = {
		"sprites": convert_sprites,
		"maps": convert_maps,
		"levels": convert_levels,
		"fonts": convert_fonts,
		"particles": convert_particles,
		"sounds": convert_sounds,
		"music": convert_music,
		"ui": convert_uis,
		"uiscriptlet": convert_ui_scriptlet,
		"powerups": convert_powerups_file,
		"layers": convert_layers_file,
		"shooter": convert_shooter_file,
		"spheres": convert_sphere_files,
		"locale": convert_locale_file,
		"highscores": convert_highscores_file
	}

	conversion_types = list(conversion_scope.keys())
	for i in range(len(conversion_types)):
		registry = conversion_types[i]
		files = conversion_scope[registry]
		print("==================================")
		print("Converting " + registry + " (" + str(i + 1) + "/" + str(len(conversion_types)) + ")...")
		CONVERSION_FUNCTIONS[registry](files)
		print("Done!")



### Converts a UI layout. (WIP)
def convert_ui_test(name):
	if name == "":
		convert_uis()
	else:
		output = convert_ui(get_contents(FDATA + "/uiscript/" + name + ".ui"))
		store_contents("output/ui/" + name + ".json", output)
		print("Converted!")



### Entry point of the application. Handles the commandline arguments.
def main():
	global FDATA

	if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == "--help"):
		print("Welcome to OpenSMCE Converter!")
		print("Supported games: Luxor, Luxor Amun Rising and mods for these games. Luxor 2 not supported!")
		print()
		print("Usage: main.py [arguments]")
		print()
		print("Possible arguments:")
		print("    --all - Converts all supported assets.")
		print("    --sprites - Converts sprites and images.")
		print("    --maps - Converts maps.")
		print("    --levels - Converts levels.")
		print("    --fonts - Converts fonts.")
		print("    --particles - Converts particles.")
		print("    --sounds - Converts sound events (sound/sounds.sl3).")
		print("    --music - Converts music tracks (music/music.sl3).")
		print("    --ui - Converts UI layouts.")
		print("    --uiscriptlet - Converts UI Scriptlet (uiscript/stage_select.uis).")
		print("    --powerups - Converts powerup spawning and scoring (levels/powerups.txt).")
		print("    --layers - Converts layer list (uiscript/depths.txt).")
		print("    --shooter - Converts the shooter (uiscript/game.ui, sprites/game/next_ball_0.spr, sprites/game/shooter.spr).")
		print("    --spheres - Converts the spheres (from uiscript/game.ui).")
		print("    --locale - Converts the locale (strings.utf8).")
		print("    --highscores - Converts the highscore list (scores.dat).")
		print()
		print("    After '--sprites', '--maps', '--levels', '--fonts', '--particles' or '--ui', you can give any number")
		print("     of paths to the relevant files to be converted. By default, all files will be converted.")
		print()
		print("    -d <folder> - Specify a different input folder, defaults to 'data'.")
		print()
		print("    --help - Prints this message.")
	else:
		conversion_scope = {}
		last_registry = None
		next_value = None
		for i in range(len(sys.argv) - 1):
			arg = sys.argv[i + 1]
			if next_value == None:
				if arg == "--all":
					for key in CONVERSION_SCOPE_KEYS:
						conversion_scope[CONVERSION_SCOPE_KEYS[key]] = []
				elif arg in CONVERSION_SCOPE_KEYS:
					registry = CONVERSION_SCOPE_KEYS[arg]
					if registry in conversion_scope:
						print("Error: key '" + arg + "' is invalid: duplicate or used with '--all'!")
						exit(1)
					else:
						conversion_scope[registry] = []
						last_registry = registry
				elif arg == "-d":
					next_value = arg
				elif last_registry != None:
					if not last_registry in ["sprites", "maps", "levels", "fonts", "particles", "ui"]:
						print("Error: The '" + last_registry + "' file type cannot be narrowed down!")
						exit(1)
					conversion_scope[last_registry].append(arg)
				else:
					print("Error: key '" + arg + "' unrecognized")
					exit(1)
			elif next_value == "-d":
				FDATA = arg
				next_value = None
		convert(conversion_scope)
		



main()