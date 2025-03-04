import math, sys, os, json
from PIL import Image, ImageDraw



# The paths to the data folder.
FDATA = "data"

# A list of stuff to convert. See `convert()` for available values.
CONVERSION_SCOPE = []



#
#  UTILITY
#

#
#  Converts case LIKE THIS to case LikeThis.
#

def convert_pascal(line):
	return "".join(word[0].upper() + word[1:].lower() for word in line.split(" "))

#
#  Removes all preceeding whitespaces from the given line.
#

def unindent(line):
	char = 0
	while char < len(line):
		if not line[char] in [" ", "\t"]:
			return line[char:]
		char += 1

#
# Fix paths for unixlike systems
#

def fix_path(path):
	path = path.replace("\\", "/")
	if FDATA + "/maps" in path:
		path = path.replace("InTheShadowofthePyramids","InTheShadowOfThePyramids") \
			.replace("InnerSanctumoftheTemple","InnerSanctumOfTheTemple") \
			.replace("flightofthesacredibis","FlightOfTheSacredIbis") \
			.replace("DescenttotheUnderworld","DescentToTheUnderworld") \
			.replace("inundationofthenile","InundationOfTheNile") \
			.replace("danceofthecrocodiles","DanceOfTheCrocodiles") \
			.replace("RasJourneytotheWest","RasJourneyToTheWest") \
			.replace("ThePillarofOsiris","ThePillarOfOsiris") \
			.replace("ScrollofThoth","ScrollOfThoth") \
			.replace("PooloftheLotusBlossom","PoolOfTheLotusBlossom") \
			\
			.replace("HalloftheApisBull","HallOfTheApisBull") \
			.replace("QueenofDenial","QueenOfDenial") \
			.replace("BastionoftheCatGoddess","BastionOfTheCatGoddess") \
			.replace("WeighingoftheHeart","WeighingOfTheHeart") \
			.replace("ReignoftheHereticKing","ReignOfTheHereticKing") \
			.replace("TheTreasureCityofRameses","TheTreasureCityOfRameses") \
			.replace("OpeningoftheMouthCeremony","OpeningOfTheMouthCeremony") \
			.replace("FestivalofJubilee","FestivalOfJubilee") \
			.replace("CrossingtheReedSea","CrossingTheReedSea") \
			.replace("TheStellaeofThutmosis","TheStellaeOfThutmosis") \
			.replace("ValleyoftheKings","ValleyOfTheKings") \
			.replace("EyeofHorus","EyeOfHorus") \
			.replace("InvasionoftheHyksos","InvasionOfTheHyksos") \
			.replace("demo2","Demo2") \
			.replace("narmerpalette","NarmerPalette")

	return path

#
#  Takes a file from a given path and returns its contents as a list of lines.
#

def get_contents(path):
	path = fix_path(path) # MacOS hack
	file = open(path, "r")
	contents = file.read()
	file.close()
	return contents.split("\n")

#
#  Stores given data in JSON format in a given file.
#

def store_contents(path, contents):
	file = open(path, "w")
	file.write(json.dumps(contents, indent = 4))
	file.close()

#
#  Attempts to create a folder with a given name if it doesn't exist yet.
#

def try_create_dir(path):
	try:
		os.makedirs(path)
	except:
		pass

#
#  Attempts to create a folder structure with a given name if it doesn't exist yet.
#

def try_create_dirs(path):
	total = ""
	try:
		for folder in path.split("/"):
			total += folder + "/"
			try_create_dir(total)
	except:
		pass

#
#  Returns True if a given file exists.
#

def file_exists(path):
	try:
		open(path, "r")
	except:
		return False
	return True


#
#  Changes i.e. "data\sprites\game\shooter.spr" to "images/game/shooter.png".
#

def resolve_path_image(path):
	return fix_path(path).replace(FDATA + "/sprites", "images")[:-4] + ".png"

#
#  Changes i.e. "data\sprites\game\shooter.spr" to "sprites/game/shooter.json".
#

def resolve_path_sprite(path):
	return fix_path(path).replace(FDATA + "/sprites", "sprites")[:-4] + ".json"

#
#  Changes i.e. "data\fonts\score4.font" to "fonts/score4.json".
#

def resolve_path_font(path):
	return fix_path(path).replace(FDATA + "/fonts", "fonts")[:-5] + ".json"

#
#  Changes i.e. "data\psys\powerup_stop.psys" to "particles/powerup_stop.json".
#

def resolve_path_particle(path):
	return fix_path(path).replace(FDATA + "/psys", "particles")[:-5] + ".json"

#
#  Changes i.e. "data\sound\collapse_1.ogg" to "sounds/collapse_1.ogg".
#

def resolve_path_sound(path):
	return fix_path(path).replace(FDATA + "/sound", "sounds")

#
#  Changes i.e. "data\music\menu.ogg" to "music/menu.ogg".
#

def resolve_path_music(path):
	return fix_path(path).replace(FDATA + "/music", "music")

#
#  If both values are identical, return that value. If not, return a random value generator dictionary, eg. {"type":"randomInt","min":1,"max":3}
#

def collapse_random_number(a, b, is_float):
	if a == b:
		return a
	else:
		return {"type":"randomFloat" if is_float else "randomInt","min":a,"max":b}

#
#  Changes i.e. "level_1_1" to "level_101".
#

def rename_level(name):
	try:
		words = name.split("_")
		a = int(words[1])
		b = int(words[2])
		return "level_" + str(a * 100 + b)
	except:
		return name



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
	output_path = "/".join(result_path.split("/")[:-1])
	if not os.path.exists(output_path):
		os.makedirs(output_path)

	try:
		img = Image.open(fix_path(img_path))
	except:
		print("Unknown image: " + img_path)
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
	output_path = "/".join(result_path.split("/")[:-1])
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	store_contents(result_path, sprite_data)

#
#  Takes (path.obj) file contents and returns a list of vertices in {x:, y:} form.
#

def convert_path(contents):
	vertices = []
	vertex_order = []

	for line in contents:
		words = line.split(" ")
		if words[0] == "v":
			vertices.append({"x":float(words[1]),"y":-float(words[2]),"hidden":False})
		if words[0] == "f":
			for i in range(len(words) - 1):
				vertex_order.append(int(words[i + 1]))

	result = []
	for vertex_id in vertex_order:
		result.append(vertices[vertex_id - 1])

	result.reverse()

	return result

#
#  Takes (level_x_y.lvl) file contents and returns level data.
#

def convert_level(contents):
	level_data = {
		"$schema": "../../../../schemas/config/level.json",
		"map": "",
		"sequence": "level_sequences/adventure.json",
		"music": "music_tracks/level_music.json",
		"dangerMusic": "music_tracks/danger_music.json",
		"colorGeneratorNormal": "default",
		"colorGeneratorDanger": "danger",
		"matchEffect": "match",
		"objectives": [
			{
				"type": "destroyedSpheres",
				"target": 0
			}
		],
		"pathsBehavior": [
			{
				"colorRules": {
					"type": "random",
					"colors": [],
					"colorStreak": 0,
					"forceDifferentColor": True
				},
				"spawnRules": {
					"type": "waves",
					"amount": 0
				},
				"spawnDistance": 0,
				"dangerDistance": 0.75,
				"speeds": []
			},
			{
				"colorRules": {
					"type": "random",
					"colors": [],
					"colorStreak": 0,
					"forceDifferentColor": True
				},
				"spawnRules": {
					"type": "waves",
					"amount": 0
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

	for line in contents:
		line = unindent(line)
		if line == None:
			continue
		words = line.split(" ")
		if words[0] == "mapFile":
			level_data["map"] = convert_pascal(" ".join(words[2:])[1:-1]).replace("'", "")
		if words[0][:11] == "spawnColor_" and words[2] == "true":
			level_data["pathsBehavior"][0]["colorRules"]["colors"].append(int(words[0][11:]))
			level_data["pathsBehavior"][1]["colorRules"]["colors"].append(int(words[0][11:]))
		if words[0] == "spawnStreak":
			level_data["pathsBehavior"][0]["colorRules"]["colorStreak"] = 0.45 #min(int(words[2]) / 300, 0.45)
			level_data["pathsBehavior"][1]["colorRules"]["colorStreak"] = 0.45 #min(int(words[2]) / 300, 0.45)
		if words[0] == "winCondition":
			level_data["objectives"][0]["target"] = int(words[2])
		if words[0] == "viseGroupCount":
			level_data["pathsBehavior"][0]["spawnRules"]["amount"] = int(words[2])
			level_data["pathsBehavior"][1]["spawnRules"]["amount"] = int(words[2])
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

	return level_data

#
#  Takes all files from given path and converts them to the Sphere Matcher Engine format. A slash after the path is important!
#

def convert_map(input_path, output_path):
	if not os.path.exists(output_path):
		os.makedirs(output_path)

	map_data = {
		"$schema":"../../../../schemas/map.json",
		"name":"",
		"paths":[],
		"sprites":[]
	}

	contents = get_contents(input_path + "map.ui")

	for line in contents:
		line = unindent(line)
		if line == None:
			continue
		words = line.split(" ")

		if words[0] == "MapName":
			map_data["name"] = " ".join(words[2:])[1:-1]

		if words[0] == "Sprite":
			is_global = input_path.replace("/", "\\").lower() != ("\\".join(words[2].split("\\")[:-1]) + "\\").lower()
			sprite_name = (words[2].replace("\\", "/").replace(FDATA + "/sprites", "sprites")[:-4]) if is_global else words[2].split("\\")[-1][:-4]
			if not is_global:
				combine_alpha_sprite(input_path + sprite_name + ".spr", output_path + sprite_name + ".json", output_path + sprite_name + ".png")
			sprite = {
				"x": 0,
				"y": 0,
				"path": ("" if is_global else ":") + sprite_name + ".json",
				"background": True
			}
			map_data["sprites"].append(sprite)

		if words[0] == "GLSprite":
			is_global = input_path.replace("/", "\\").lower() != ("\\".join(words[5].split("\\")[:-1]) + "\\").lower()
			background = words[4] == "GamePieceHShadow"
			foreground = words[4] == "MenuControls"
			sprite_name = (words[5].replace("\\", "/").replace(FDATA + "/sprites", "sprites")[:-4]) if is_global else words[5].split("\\")[-1][:-4]
			if not is_global:
				combine_alpha_sprite(input_path + sprite_name + ".spr", output_path + sprite_name + ".json", output_path + sprite_name + ".png")
			sprite = {
				"x": int(words[2]),
				"y": int(words[3]),
				"path": ("" if is_global else ":") + sprite_name + ".json",
				"background": background
			}
			if foreground:
				sprite["foreground"] = foreground
			map_data["sprites"].append(sprite)

		if words[0] == "Path":
			path = convert_path(get_contents(input_path + words[2].split("\\")[-1]))
			map_data["paths"].append(path)

		if words[0] == "Node":
			map_data["paths"][int(words[2])][int(words[3])]["hidden"] = True

	store_contents(output_path + "config.json", map_data)

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

	image_name = contents[0].replace("\\", "/").replace(FDATA + "/bitmaps", "images")[:-4]
	combine_alpha_path(contents[0].replace("\\", "/"), contents[1].replace("\\", "/"), "output/" + image_name + ".png")
	font_data["image"] = image_name + ".png"

	for i in range((len(contents) - 4) // 2):
		char = contents[i * 2 + 4]
		params = contents[i * 2 + 5].split(" ")
		font_data["characters"][char] = {"offset":int(params[0]),"width":int(params[2])}

	store_contents(output_path, font_data)

#
#  Takes .ui file contents and returns UI script data. Rule tables stored separately are used to automatically fill all things that are hardcoded in the original engine.
#

def convert_ui(contents, rule_table, name = "root"):
	ui_data = {"inheritShow":True,"inheritHide":True,"type":"none","pos":{"x":0,"y":0},"alpha":1,"children":{},"animations":{},"sounds":{}}
	sub_anim_uis = {}

	child_scan = False
	child_scan_level = 0
	child_name = ""
	child_type = "none"
	child_contents = []

	for line in contents:
		line = unindent(line)
		if line == None:
			continue

		if child_scan:
			child_contents.append(line)
			if line == "{":
				child_scan_level += 1
			if line == "}":
				child_scan_level -= 1 # protection for nested children
				if child_scan_level == 0:
					child_scan = False
					if child_name == "Background":
						ui_data["children"][child_name] = {"inheritShow":True,"inheritHide":True,"type":"none","pos":{"x":0,"y":0},"alpha":1,"children":{"Background":"ui/background.json"},"animations":{},"sounds":{}}
					else:
						full_child_name = name + "." + child_name
						print(full_child_name + ":")
						print("\n".join(child_contents))
						child_data = convert_ui(child_contents, rule_table, full_child_name)
						child_data["type"] = child_type
						ui_data["children"][child_name] = child_data
			continue

		words = line.split(" ")
		if words[0] == "//":
			continue # we don't want comments

		if words[0] == "X":
			ui_data["pos"]["x"] = int(words[2])
		if words[0] == "Y":
			ui_data["pos"]["y"] = int(words[2])
		if words[0] == "AnimIn" and words[1] == "Sound":
			ui_data["sounds"]["in_"] = "sounds/" + words[3] + ".ogg"
		if words[0] == "AnimOut" and words[1] == "Sound":
			ui_data["sounds"]["out"] = "sounds/" + words[3] + ".ogg"
		if words[0] == "Depth":
			ui_data["layer"] = words[2]
		if words[0] == "Text":
			ui_data["text"] = " ".join(words[2:])[1:-1]
		if words[0] == "Sprite":
			ui_data["sprite"] = resolve_path_sprite(words[2])
		if words[0] == "Sprite2":
			ui_data["sprite"] = [ui_data["sprite"], resolve_path_sprite(words[2])]
		if words[0] == "Font":
			ui_data["font"] = resolve_path_font(words[2])
		if words[0] == "Justify":
			ui_data["align"] = {"LEFT":{"x":0,"y":0},"CENTER":{"x":0.5,"y":0},"RIGHT":{"x":1,"y":0}}[words[2]]
		if words[0] == "Smooth":
			ui_data["smooth"] = words[2] == "True"
		if words[0] == "MinX":
			ui_data["bounds"] = [int(words[2]), 0]
		if words[0] == "MaxX":
			ui_data["bounds"][1] = int(words[2])
		if words[0] == "File":
			ui_data["path"] = resolve_path_particle(words[2])
		if words[0] == "Child":
			if len(words) < 4:
				continue
			child_types = {
				"uiNonVisualWidget":"none",
				"uiVisualWidget":"sprite",
				"uiTextWidget":"text",
				"uiButton":"spriteButton",
				"uiToggleButton":"spriteButtonCheckbox",
				"uiSliderButton":"spriteButtonSlider",
				"uiProgressBar":"spriteProgress",
				"uiProgressBar_Giza":"spriteProgress",
				"uiParticleSystem":"particle"
			}
			if words[3] in child_types:
				child_type = child_types[words[3]]
			else:
				print("Unknown UI widget type! " + words[3])
				child_type = "none"
			child_scan = True
			child_scan_level = 0
			child_name = words[1]
			child_contents = []



		if words[0] == "SubAnimIn":
			if words[2] == "Widget":
				sub_ui = ui_data
				sub_ui_nav = words[4].split(".")[1:]
				for nav in sub_ui_nav:
					sub_ui = sub_ui["children"][nav]
				sub_anim_uis[words[1]] = sub_ui
			if words[2] == "SpriteDepth":
				sub_anim_uis[words[1]]["layer"] = words[4]
			if words[2] == "Style":
				style_types = {"AlphaFade":"fade","SpriteMask":"fade","BezierLerp":"move"}
				if words[4] in style_types:
					style_type = style_types[words[4]]
				else:
					print("Unknown style type! " + words[4])
					style_type = "none"
				sub_anim_uis[words[1]]["animations"]["in_"] = {"type":style_type}
				sub_anim_uis[words[1]]["animations"]["out"] = {} # placeholder filled later
			if words[2] == "Time":
				sub_anim_uis[words[1]]["animations"]["in_"]["time"] = int(words[4]) / 1000
			if words[2] == "Loc" and sub_anim_uis[words[1]]["animations"]["in_"]["type"] == "move":
				sub_anim_uis[words[1]]["animations"]["in_"]["startPos"] = {"x":int(words[4]),"y":int(words[5])}
				sub_anim_uis[words[1]]["animations"]["out"]["endPos"] = {"x":int(words[4]),"y":int(words[5])}
			if words[2] == "AlphaStart" and sub_anim_uis[words[1]]["animations"]["in_"]["type"] == "fade":
				sub_anim_uis[words[1]]["animations"]["in_"]["startValue"] = int(words[4]) / 255
				sub_anim_uis[words[1]]["alpha"] = int(words[4]) / 255
			if words[2] == "AlphaTarget" and sub_anim_uis[words[1]]["animations"]["in_"]["type"] == "fade":
				sub_anim_uis[words[1]]["animations"]["in_"]["endValue"] = int(words[4]) / 255
		if words[0] == "SubAnimOut":
			if words[2] == "Style":
				style_types = {"AlphaFade":"fade","SpriteMask":"fade","BezierLerp":"move"}
				if words[4] in style_types:
					style_type = style_types[words[4]]
				else:
					print("Unknown style type! " + words[4])
					style_type = "none"
				sub_anim_uis[words[1]]["animations"]["out"]["type"] = style_type
			if words[2] == "Time":
				sub_anim_uis[words[1]]["animations"]["out"]["time"] = int(words[4]) / 1000
			if words[2] == "Loc" and sub_anim_uis[words[1]]["animations"]["in_"]["type"] == "move":
				sub_anim_uis[words[1]]["animations"]["in_"]["endPos"] = {"x":int(words[4]),"y":int(words[5])}
				sub_anim_uis[words[1]]["animations"]["out"]["startPos"] = {"x":int(words[4]),"y":int(words[5])}
			if words[2] == "AlphaStart" and sub_anim_uis[words[1]]["animations"]["in_"]["type"] == "fade":
				sub_anim_uis[words[1]]["animations"]["out"]["startValue"] = int(words[4]) / 255
			if words[2] == "AlphaTarget" and sub_anim_uis[words[1]]["animations"]["in_"]["type"] == "fade":
				sub_anim_uis[words[1]]["animations"]["out"]["endValue"] = int(words[4]) / 255

	if name in rule_table:
		for key in rule_table[name]:
			ui_data[key] = rule_table[name][key]

	return ui_data

#
#  Takes .psys file contents and returns particle spawner data.
#

def convert_psys(contents):
	particle_data = {
		"$schema": "../../../schemas/particle.json",
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

	for line in contents:
		line = unindent(line)
		if line == None:
			continue
		words = line.split(" ")
		if words[0] == "//":
			continue # we don't want comments

		if spawner_name == None:
			if words[0] == "Emitter":
				spawner_name = words[1]
				spawner_data = {
					"name":spawner_name,
					"pos":{"x":0,"y":0},
					"speed":{"x":0,"y":0},
					"acceleration":{"x":0,"y":0},
					"lifespan":None,
					"spawnCount":1,
					"spawnMax":1,
					"spawnDelay":None,
					"particleData":{
						"speedMode":"loose",
						"spawnScale":{"x":0,"y":0},
						"speed":{"x":0,"y":0},
						"acceleration":{"x":0,"y":0},
						"lifespan":None,
						"sprite":"",
						"animationFrameCount":1,
						"animationSpeed":0,
						"animationLoop":False,
						"animationFrameRandom":False,
						"fadeInPoint":0,
						"fadeOutPoint":1,
						"posRelative":False,
						"rainbow":False,
						"rainbowSpeed":0
					}
				}
			else:
				print("Unknown type: " + words[0])
			continue

		if words[0] == "}":
			spawner_data["particleData"]["lifespan"] = collapse_random_number(lifespan_min, lifespan_max, True)
			spawner_data["particleData"]["spawnScale"]["x"] = collapse_random_number(spawn_radius_min_x, spawn_radius_max_x, True)
			spawner_data["particleData"]["spawnScale"]["y"] = collapse_random_number(spawn_radius_min_y, spawn_radius_max_y, True)
			spawner_data["particleData"]["speed"]["x"] = collapse_random_number(start_vel_min_x, start_vel_max_x, True)
			spawner_data["particleData"]["speed"]["y"] = collapse_random_number(start_vel_min_y, start_vel_max_y, True)
			spawner_data["speed"]["x"] = collapse_random_number(emitter_vel_min_x, emitter_vel_max_x, True)
			spawner_data["speed"]["y"] = collapse_random_number(emitter_vel_min_y, emitter_vel_max_y, True)

			if "EF_LIFESPAN_INFINITE" in spawner_flags:
				spawner_data["particleData"]["lifespan"] = None
			if "EF_ELIFESPAN_INFINITE" in spawner_flags:
				spawner_data["lifespan"] = None
			if "EF_POS_RELATIVE" in spawner_flags:
				spawner_data["particleData"]["posRelative"] = True
			if "EF_VEL_POSRELATIVE" in spawner_flags:
				spawner_data["particleData"]["speedMode"] = "radius"
			if "EF_SPRITE_ANIM_LOOP" in spawner_flags:
				spawner_data["particleData"]["animationLoop"] = True
			if "EF_SPRITE_RANDOM_FRAME" in spawner_flags:
				spawner_data["particleData"]["animationFrameRandom"] = True
			if "EF_VEL_DEVIATION" in spawner_flags:
				spawner_data["particleData"]["directionDeviationTime"] = dev_delay
				spawner_data["particleData"]["directionDeviationSpeed"] = collapse_random_number(dev_angle_min / 360 * math.pi * 2, dev_angle_max / 360 * math.pi * 2, True)
			if "EF_VEL_ORBIT" in spawner_flags:
				spawner_data["particleData"]["posRelative"] = True
				spawner_data["particleData"]["speedMode"] = "circle"
				spawner_data["particleData"]["speed"] = spawner_data["particleData"]["speed"]["x"]
				spawner_data["particleData"]["acceleration"] = spawner_data["particleData"]["acceleration"]["x"]

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
			image_file = words[2].replace("\\", "/").replace(FDATA + "/bitmaps", "images").replace(".jpg", ".png")
			color_palette_file = words[2].replace("\\", "/").replace(FDATA + "/bitmaps", "color_palettes")
			spawner_data["particleData"]["colorPalette"] = color_palette_file[:-4] + ".json"
			# Create a new Color Palette alongside.
			generate_color_palette(image_file)
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
			spawner_data["particleData"]["acceleration"]["x"] = float(words[2])
			spawner_data["particleData"]["acceleration"]["y"] = float(words[3])
		if words[0] == "DevDelay":
			dev_delay = float(words[2])
		if words[0] == "DevAngle":
			dev_angle_min = float(words[2])
			dev_angle_max = float(words[3])
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

	for line in contents:
		line = unindent(line)
		if line == None:
			continue
		words = line.split(" ")
		if words[0][:2] == "//":
			continue # we don't want comments

		if line == "{":
			param_mode = True
		elif line == "}":
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

				events[name] = event

	return events

#
#  Takes (music.sl3) file contents and generates music tracks that can be saved.
#

def convert_music_from_sl3(contents):
	tracks = {}
	name = ""
	param_mode = False

	for line in contents:
		line = unindent(line)
		if line == None:
			continue
		words = line.split(" ")
		if words[0][:2] == "//":
			continue # we don't want comments

		if line == "{":
			param_mode = True
		elif line == "}":
			param_mode = False
		else:
			if param_mode:
				pass # we aren't interested in parameters
			else:
				name = words[0]
				if words[2] == "playlist":
					continue # we aren't interested in playlists (for now) - TODO: multi-track support

				track = {
					"$schema": "../../../schemas/music_track.json",
					"audio": resolve_path_music(words[3])
				}

				tracks[name] = track

	return tracks

#
#  Takes a path to the image and generates a Color Palette file pointing to it. Temporary function.
#

def generate_color_palette(image_path):
	# TODO: Remove this function in favor of loading color palettes in immediate mode.
	color_palette_data = {
		"$schema": "../" * len(image_path.split("/")) + "schemas/color_palette.json",
		"image": image_path
	}

	# File hierarchy analogic to the image file.
	color_palette_path = image_path.replace("images", "color_palettes")
	try_create_dirs("output/" + "/".join(color_palette_path.split("/")[:-1]))
	store_contents("output/" + color_palette_path[:-4] + ".json", color_palette_data)



### Converts sprites and images.
### Input: data/sprites/**/*.spr + .tga and .jpg files specified inside
### Output: output/sprites/**/*.json + combined output/images/**/*.png
### Plus, extra images.
def convert_sprites():
	# TODO: Convert all images specified as color palettes or in particles.
	# TODO: Don't restrict to data/sprites, scan everything.
	# TODO: Don't change the directory structure for the dialog cursor.
	for r, d, f in os.walk(FDATA + "/sprites"):
		for directory in d:
			for r, d, f in os.walk(FDATA + "/sprites/" + directory):
				for file in f:
					print(directory + "/" + file)
					sprite_path = FDATA + "/sprites/" + directory + "/" + file
					combine_alpha_sprite(sprite_path, "output/" + resolve_path_sprite(sprite_path), "output/" + resolve_path_image(sprite_path))

	# one more lone splash background is needed
	combine_alpha_path(FDATA + "/bitmaps/splash/background.jpg", None, "output/images/splash/background.png")

	# and some palettes, too
	combine_alpha_path(FDATA + "/bitmaps/powerups/wild_pal.jpg", None, "output/images/powerups/wild_pal.png")
	for n in ["blue", "green", "orange", "pink", "purple", "red", "yellow"]:
		combine_alpha_path(FDATA + "/bitmaps/particles/gem_bloom_" + n + ".jpg", None, "output/images/particles/gem_bloom_" + n + ".png")

	# and that blinking cursor thingy
	combine_alpha_sprite(FDATA + "/fonts/dialog_body_cursor.spr", "output/sprites/fonts/dialog_body_cursor.json", "output/images/fonts/dialog_body_cursor.png")



### Converts maps and sprites belonging to maps.
### Input: data/maps/**
### Output: output/maps/**
def convert_maps():
	# TODO: Map sprites should be converted by the methods above...?
	for r, d, f in os.walk(FDATA + "/maps"):
		for directory in d:
			print(directory)
			convert_map(FDATA + "/maps/" + directory + "/", "output/maps/" + directory + "/")



### Converts level files.
### Input: data/levels/*.lvl
### Output: output/config/levels/*.json
def convert_levels():
	try_create_dir("output/config/levels/")

	for r, d, f in os.walk(FDATA + "/levels"):
		for file in f:
			if file == "powerups.txt":
				continue
			print(file)
			store_contents("output/config/levels/" + rename_level(file[:-4]) + ".json", convert_level(get_contents(FDATA + "/levels/" + file)))



### Converts fonts.
### Input: data/fonts/*.font
### Output: output/fonts/*.json
def convert_fonts():
	try_create_dir("output/fonts/")

	for r, d, f in os.walk(FDATA + "/fonts"):
		for file in f:
			if file == "dialog_body_cursor.spr":
				continue
			print(file)
			convert_font(FDATA + "/fonts/" + file, "output/fonts/" + file[:-5] + ".json")



### Converts particles.
### Input: data/psys/*.psys (minus progress.psys)
### Output: output/particles/*.json
def convert_particles():
	try_create_dir("output/particles/")

	for r, d, f in os.walk(FDATA + "/psys"):
		for file in f:
			if file == "progress.psys":
				continue
			print(file)
			store_contents("output/particles/" + file[:-5] + ".json", convert_psys(get_contents(FDATA + "/psys/" + file)))



### Converts sound events.
### Input: data/sound/sounds.sl3
### Output: output/sound_events/*.json
def convert_sounds():
	try_create_dir("output/sound_events/")

	events = convert_sounds_from_sl3(get_contents(FDATA + "/sound/sounds.sl3"))

	for event_name in events:
		print(event_name)
		store_contents("output/sound_events/" + event_name + ".json", events[event_name])



### Converts music tracks.
### Input: data/music/music.sl3
### Output: output/music_tracks/*.json
def convert_music():
	try_create_dir("output/music_tracks/")

	tracks = convert_music_from_sl3(get_contents(FDATA + "/music/music.sl3"))

	for n in tracks:
		print(n)
		store_contents("output/music_tracks/" + n + ".json", tracks[n])



### Main conversion function.
def convert():
	# Sample manual conversion functions:
	# combine_alpha_path("warning.jpg", "warning_alpha.tga", "warning.png")
	# combine_alpha_path("warning2.jpg", "", "warning_gem.png")
	# convert_map(FDATA + "/maps/Demo/", "output/maps/Demo/")
	# store_contents("output/levels/level_0_0.json", convert_level(get_contents(FDATA + "/levels/level_0_0.lvl")))

	if file_exists(FDATA + "/sprites/powerups/scorpion.spr"):
		print("\n\nYOU ARE CONVERTING LUXOR AMUN RISING\n\n")
	else:
		print("\n\nYOU ARE CONVERTING LUXOR 1\n\n")

	###############################################################################################   MAIN START

	CONVERSION_FUNCTIONS = {
		"sprites": convert_sprites,
		"maps": convert_maps,
		"levels": convert_levels,
		"fonts": convert_fonts,
		"particles": convert_particles,
		"sounds": convert_sounds,
		"music": convert_music
	}

	for i in range(len(CONVERSION_SCOPE)):
		registry = CONVERSION_SCOPE[i]
		print("\n\n\n\nConverting " + registry + " (" + str(i + 1) + "/" + str(len(CONVERSION_SCOPE)) + ")...")
		CONVERSION_FUNCTIONS[registry]()
		print("Done!")

	###############################################################################################   MAIN END

	### CONVERT UI (WIP)
	# for name in ["profile_dup"]:
		# # if name + ".ui" in rule_tables["ui"]:
			# # rule_table = rule_tables["ui"][name + ".ui"]
		# # else:
		# rule_table = {}
		# store_contents("output/ui/" + name + ".json", convert_ui(get_contents(FDATA + "/uiscript/" + name + ".ui"), rule_table))



### Entry point of the application. Handles the commandline arguments.
def main():
	global CONVERSION_SCOPE

	if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == "--help"):
		print("Welcome to OpenSMCE Converter!")
		print("Supported games: Luxor, Luxor Amun Rising. Mods not supported!")
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
		print("    --sounds - Converts sounds.")
		print("    --music - Converts music.")
		print()
		print("    -d <folder> - Specify a different input folder, defaults to 'data'.")
		print()
		print("    --help - Prints this message.")
	else:
		CONVERSION_SCOPE_KEYS = {
			"--sprites": "sprites",
			"--maps": "maps",
			"--levels": "levels",
			"--fonts": "fonts",
			"--particles": "particles",
			"--sounds": "sounds",
			"--music": "music"
		}
		next_value = None
		for i in range(len(sys.argv) - 1):
			arg = sys.argv[i + 1]
			if next_value == None:
				if arg == "--all":
					CONVERSION_SCOPE = ["sprites", "maps", "levels", "fonts", "particles", "sounds", "music"]
				elif arg in CONVERSION_SCOPE_KEYS:
					registry = CONVERSION_SCOPE_KEYS[arg]
					if registry in CONVERSION_SCOPE:
						print("Error: key " + arg + " is invalid: duplicate or used with --all!")
						exit(1)
					else:
						CONVERSION_SCOPE.append(registry)
				elif arg == "-d":
					next_value = arg
				else:
					print("Error: key " + arg + " unrecognized")
					exit(1)
			elif next_value == "-d":
				FDATA = arg
				next_value = None
		convert()
		



main()