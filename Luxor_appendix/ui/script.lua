-- This is a default UI script file for OpenSMCE games.
-- Keep in mind that more methods may be added, or existing changed in the future.
-- These script files will be automatically updated if needed by the engine.

-- All callbacks will be stored here.
local c = {}

-- The first parameter of each callback is a variable "f".
-- It is used just as a simple way to provide the function library to be used here.

-- SPLASH STUFF
function c.init(f)
  f.getWidgetN("splash"):show()
  f.getWidgetN("splash"):setActive()
  f.getWidgetN("splash"):setCallback("showEnd", c.splashStart)
  f.getWidgetN("splash"):setCallback("hideEnd", c.splashEnd)
  f.getWidgetN("splash/Frame/Button_Play"):setCallback("buttonClick", c.splashClick)
  c.menuMusic(f, true)
end

function c.splashClick(f)
  f.resetActive()
  f.getWidgetN("splash"):hide()
end

function c.splashStart(f)
  f.loadMain()
end

function c.splashEnd(f)
  f.initSession()

  -- initSession() initializes all the UI, so from this point we can initialize all the modules.
  c.root = f.getWidgetN("root")
  c.Main = f.getWidgetN("root/Main")

  c.Profile_Manage = f.getWidgetN("root/Main/Profile_Manage")
  c.Profile_Manage_Button_Up = f.getWidgetN("root/Main/Profile_Manage/Frame/Listbox/Button_Up")
  c.Profile_Manage_Button_Down = f.getWidgetN("root/Main/Profile_Manage/Frame/Listbox/Button_Down")
  c.Profile_Manage_Button_Delete = f.getWidgetN("root/Main/Profile_Manage/Frame/Button_Delete")
  c.Profile_Manage_Button_Select = f.getWidgetN("root/Main/Profile_Manage/Frame/Button_Select")
  c.Profile_Create = f.getWidgetN("root/Main/Profile_Create")
  c.Profile_Create_Button_Cancel = f.getWidgetN("root/Main/Profile_Create/Frame/Button_Cancel")
  c.Profile_Create_Button_Ok = f.getWidgetN("root/Main/Profile_Create/Frame/Button_Ok")
  c.Profile_Duplicate = f.getWidgetN("root/Main/Profile_Duplicate")
  c.Profile_Delete = f.getWidgetN("root/Main/Profile_Delete")

  c.Options_Music = f.getWidgetN("root/Menu_Options/Frame/Slot_music/Slider_Music")
  c.Options_Sound = f.getWidgetN("root/Menu_Options/Frame/Slot_sfx/Slider_Effects")
  c.Options_Fullscreen = f.getWidgetN("root/Menu_Options/Frame/Toggle_Fullscreen")
  c.Options_Mute = f.getWidgetN("root/Menu_Options/Frame/Toggle_Mute")

  c.Menu_Game = f.getWidgetN("root/Menu_Game")
  c.Menu_Highscores = f.getWidgetN("root/Menu_HighScores")
  c.Menu_Highscores_Highlight = f.getWidgetN("root/Menu_HighScores/Frame/Psys_Highlight")
  c.Menu_ClearScores = f.getWidgetN("root/Menu_ClearScores")
  c.Menu_Options = f.getWidgetN("root/Menu_Options")
  c.Menu_QuitGame = f.getWidgetN("root/Menu_QuitGame")
  c.Menu_Credits = f.getWidgetN("root/Menu_Credits")
  c.Menu_Instructions = f.getWidgetN("root/Menu_Instructions")
  c.Menu_Instructions_Toggle_DontShow = f.getWidgetN("root/Menu_Instructions/Frame/Toggle_DontShow")
  c.Menu_Instructions_Mask = f.getWidgetN("root/Menu_Instructions_Mask")
  c.Menu_Continue = f.getWidgetN("root/Menu_Continue")
  c.Menu_StageSelect = f.getWidgetN("root/Menu_StageSelect")

  c.Game = f.getWidgetN("root/Game")
  c.Hud = f.getWidgetN("root/Game/Hud")
  c.Hud_NewLife = f.getWidgetN("root/Game/Hud/Frame/Psys_NewLife")
  c.Button_Menu = f.getWidgetN("root/Game/Hud/Frame/Button_Menu")
  c.Button_Pause = f.getWidgetN("root/Game/Hud/Frame/Button_Pause")
  c.Banner_Paused = f.getWidgetN("root/Game/Hud/Frame/Banner_Paused")
  c.Banner_LevelComplete = f.getWidgetN("root/Game/Hud/Frame/Banner_LevelComplete")
  c.Banner_LevelComplete_Record = f.getWidgetN("root/Game/Hud/Frame/Banner_LevelComplete/Frame/Container/VW_LevelScoreRecord")
  c.Banner_StageMapTrans = f.getWidgetN("root/Game/Hud/Frame/Banner_StageMapTrans")
  c.Banner_StageMap = f.getWidgetN("root/Game/Hud/Frame/Banner_StageMap")
  c.Banner_HighScore = f.getWidgetN("root/Game/Hud/Frame/Banner_Highscore")
  c.Banner_QuitBackground = f.getWidgetN("root/Game/Hud/Frame/Banner_QuitBackground")
  c.Banner_LevelLose = f.getWidgetN("root/Game/Hud/Frame/Banner_LevelLose")
  c.Banner_Intro = f.getWidgetN("root/Game/Hud/Frame/Banner_Intro")
  c.Banner_GameOver = f.getWidgetN("root/Game/Hud/Frame/Banner_GameOver")
  c.Banner_GameWin = f.getWidgetN("root/Game/Hud/Frame/Banner_GameWin")

  c.LevelButtons = f.getWidgetListN("root/Game/Hud/Frame/Banner_StageMap/Frame/StageMap/_Scriptlet/Stage_Select/LevelButtons")
  c.StageButtons = f.getWidgetListN("root/Game/Hud/Frame/Banner_StageMap/Frame/StageMap/_Scriptlet/Stage_Select/StageButtons")
  c.Banner_StageMap_StageCompletePsys = f.getWidgetN("root/Game/Hud/Frame/Banner_StageMap/Frame/StageMap/_Scriptlet/Stage_Select/StageCompletePsys")
  c.Banner_StageMap_StageUnlockPsys = f.getWidgetN("root/Game/Hud/Frame/Banner_StageMap/Frame/StageMap/_Scriptlet/Stage_Select/StageUnlockPsys")
  c.Banner_StageMap_LevelPsys = f.getWidgetN("root/Game/Hud/Frame/Banner_StageMap/Frame/StageMap/_Scriptlet/Stage_Select/LevelPsys")
  c.Banner_StageMap_StageButtons = f.getWidgetN("root/Game/Hud/Frame/Banner_StageMap/Frame/StageMap/_Scriptlet/Stage_Select/StageButtons")
  c.Banner_StageMap_LevelButtons = f.getWidgetN("root/Game/Hud/Frame/Banner_StageMap/Frame/StageMap/_Scriptlet/Stage_Select/LevelButtons")
  c.Banner_StageMap_Set = f.getWidgetN("root/Game/Hud/Frame/Banner_StageMap/Frame/StageMap/_Scriptlet/Stage_Select/Set")

  c.NewGameLevelButtons = f.getWidgetListN("root/Menu_StageSelect/Frame/StageMap/_Scriptlet/Stage_Select/LevelButtons")
  c.NewGameStageButtons = f.getWidgetListN("root/Menu_StageSelect/Frame/StageMap/_Scriptlet/Stage_Select/StageButtons")
  c.Menu_StageSelect_LevelPsys = f.getWidgetN("root/Menu_StageSelect/Frame/StageMap/_Scriptlet/Stage_Select/LevelPsys")
  c.Menu_StageSelect_StageButtons = f.getWidgetN("root/Menu_StageSelect/Frame/StageMap/_Scriptlet/Stage_Select/StageButtons")
  c.Menu_StageSelect_LevelButtons = f.getWidgetN("root/Menu_StageSelect/Frame/StageMap/_Scriptlet/Stage_Select/LevelButtons")
  c.Menu_StageSelect_Set = f.getWidgetN("root/Menu_StageSelect/Frame/StageMap/_Scriptlet/Stage_Select/Set")

  c.HighscoreRows = {}
  local i = 1
  while f.getWidgetN("root/Menu_HighScores/Frame/HSTable/Row" .. tostring(i - 1)) do
    local path = "root/Menu_HighScores/Frame/HSTable/Row" .. tostring(i - 1) .. "/HSRow"
    local row = {}
    row.rank = f.getWidgetN(path .. "/Rank")
    row.name = f.getWidgetN(path .. "/Name")
    row.name2 = f.getWidgetN(path .. "/Name2")
    row.level = f.getWidgetN(path .. "/Level")
    row.score = f.getWidgetN(path .. "/Score")
    c.HighscoreRows[i] = row
    i = i + 1
  end
  c.ProfileRows = {}
  local i = 1
  while f.getWidgetN("root/Main/Profile_Manage/Frame/Listbox/Button_" .. tostring(i)) do
    local path = "root/Main/Profile_Manage/Frame/Listbox/Button_" .. tostring(i)
    local row = {}
    row.button = f.getWidgetN(path)
    row.name = f.getWidgetN(path .. "/Text_E")
    row.name2 = f.getWidgetN(path .. "/Text_H")
    c.ProfileRows[i] = row
    i = i + 1
  end

  c.stageNames = _Utils.loadJson(_ParsePath("ui/stage_names.json"))
  c.newGameStage = 1
  c.newGameStarting = false
  c.scoreDisplay = 0
  c.progressComplete = false
  c.highscorePlace = 1
  c.profileSelectID = 0
  if f.profileGetExists() then
    for i, name in ipairs(f.profileMGetNameOrder()) do
      if f.profileGetName() == name then
        c.profileSelectID = i
        break
      end
    end
  end
  c.profileOffset = 0

  -- Texts and progress bars
  c.Main_Text_PlayerE = f.getWidgetN("root/Main/Menu/Text_PlayerE")
  c.Main_Text_PlayerH = f.getWidgetN("root/Main/Menu/Text_PlayerH")
  c.Main_Text_Version = f.getWidgetN("root/Main/Menu/Text_Version")
  c.Menu_Continue_Text_Stage = f.getWidgetN("root/Menu_Continue/Frame/Text_Stage")
  c.Menu_Continue_Text_Score = f.getWidgetN("root/Menu_Continue/Frame/Text_Score")
  c.Menu_StageSelect_Text_StageName = f.getWidgetN("root/Menu_StageSelect/Frame/StageMap/Text_StageName")
  c.Menu_StageSelect_Text_StageNumber = f.getWidgetN("root/Menu_StageSelect/Frame/StageMap/Text_StageNumber")
  c.Menu_StageSelect_Text_MapName = f.getWidgetN("root/Menu_StageSelect/Frame/StageMap/Text_MapName")
  c.Profile_Create_Entry_Name = f.getWidgetN("root/Main/Profile_Create/Frame/Entry_Name")
  c.Profile_Delete_Text_Name = f.getWidgetN("root/Main/Profile_Delete/Frame/Text_Name")
  c.Hud_Text_Stage = f.getWidgetN("root/Game/Hud/Frame/Text_Stage")
  c.Hud_Text_Lives = f.getWidgetN("root/Game/Hud/Frame/Text_Lives")
  c.Hud_Text_Coins = f.getWidgetN("root/Game/Hud/Frame/Text_Coins")
  c.Hud_Text_Score = f.getWidgetN("root/Game/Hud/Frame/Text_Score")
  c.Hud_Progress = f.getWidgetN("root/Game/Hud/Frame/Progress")
  c.Hud_Progress_Complete = f.getWidgetN("root/Game/Hud/Frame/Progress/_Particle")
  c.Banner_LevelComplete_Text_Stage = f.getWidgetN("root/Game/Hud/Frame/Banner_LevelComplete/Frame/Text_Stage")
  c.Banner_LevelComplete_Text_MapName = f.getWidgetN("root/Game/Hud/Frame/Banner_LevelComplete/Frame/Text_MapName")
  c.Banner_LevelComplete_Text_LevelScore = f.getWidgetN("root/Game/Hud/Frame/Banner_LevelComplete/Frame/Container/Text_LevelScore")
  c.Banner_LevelComplete_Text_ShotsFired = f.getWidgetN("root/Game/Hud/Frame/Banner_LevelComplete/Frame/Container/Text_ShotsFired")
  c.Banner_LevelComplete_Text_MaxCombo = f.getWidgetN("root/Game/Hud/Frame/Banner_LevelComplete/Frame/Container/Text_MaxCombo")
  c.Banner_LevelComplete_Text_Coins = f.getWidgetN("root/Game/Hud/Frame/Banner_LevelComplete/Frame/Container/Text_Coins")
  c.Banner_LevelComplete_Text_MaxChain = f.getWidgetN("root/Game/Hud/Frame/Banner_LevelComplete/Frame/Container/Text_MaxChain")
  c.Banner_LevelComplete_Text_Gems = f.getWidgetN("root/Game/Hud/Frame/Banner_LevelComplete/Frame/Container/Text_Gems")
  c.Banner_LevelComplete_Text_Segments = f.getWidgetN("root/Game/Hud/Frame/Banner_LevelComplete/Frame/Container/Text_Segments")
  c.Banner_StageMap_Text_StageName = f.getWidgetN("root/Game/Hud/Frame/Banner_StageMap/Frame/StageMap/Text_StageName")
  c.Banner_StageMap_Text_StageNumber = f.getWidgetN("root/Game/Hud/Frame/Banner_StageMap/Frame/StageMap/Text_StageNumber")
  c.Banner_StageMap_Text_MapName = f.getWidgetN("root/Game/Hud/Frame/Banner_StageMap/Frame/StageMap/Text_MapName")
  c.Banner_HighScore_Text_Congrats = f.getWidgetN("root/Game/Hud/Frame/Banner_Highscore/Panel/Text_Congrats")
  c.Banner_HighScore_Text_Score = f.getWidgetN("root/Game/Hud/Frame/Banner_Highscore/Panel/Text_Score")
  c.Banner_Intro_Text_Stage = f.getWidgetN("root/Game/Hud/Frame/Banner_Intro/Panel/Text_Stage")
  c.Banner_Intro_Text_Map = f.getWidgetN("root/Game/Hud/Frame/Banner_Intro/Panel/Text_Map")

  -- Level Complete sequence data.
  c.levelCompleteSequence = {
    {widget = c.Banner_LevelComplete_Text_LevelScore, delay = 0.5},
    {widget = c.Banner_LevelComplete_Text_ShotsFired, delay = 1.25},
    {widget = c.Banner_LevelComplete_Text_MaxCombo, delay = 1.5},
    {widget = c.Banner_LevelComplete_Text_Coins, delay = 1.75},
    {widget = c.Banner_LevelComplete_Text_MaxChain, delay = 2},
    {widget = c.Banner_LevelComplete_Text_Gems, delay = 2.25},
    {widget = c.Banner_LevelComplete_Text_Segments, delay = 2.5},
  }

  -- Set up buttons and all callbacks.
  f.getWidgetN("root/Main/Menu/Button_Player"):setCallback("buttonClick", c.mainProfiles)
  f.getWidgetN("root/Main/Menu/Button_Start"):setCallback("buttonClick", c.mainStart)
  f.getWidgetN("root/Main/Menu/Button_Options"):setCallback("buttonClick", c.mainOptions)
  f.getWidgetN("root/Main/Menu/Button_Help"):setCallback("buttonClick", c.mainHelp)
  f.getWidgetN("root/Main/Menu/Button_Scores"):setCallback("buttonClick", c.mainHighscores)
  f.getWidgetN("root/Main/Menu/Button_Quit"):setCallback("buttonClick", c.mainQuit)
  f.getWidgetN("root/Main/Profile_Manage/Frame/Button_Create"):setCallback("buttonClick", c.profilesCreate)
  f.getWidgetN("root/Main/Profile_Manage/Frame/Button_Select"):setCallback("buttonClick", c.profilesSelect)
  f.getWidgetN("root/Main/Profile_Manage/Frame/Button_Delete"):setCallback("buttonClick", c.profilesDelete)
  f.getWidgetN("root/Main/Profile_Manage/Frame/Button_Cancel"):setCallback("buttonClick", c.profilesCancel)
  f.getWidgetN("root/Main/Profile_Manage/Frame/Listbox/Button_1"):setCallback("buttonClick", c.profilesChange, {1})
  f.getWidgetN("root/Main/Profile_Manage/Frame/Listbox/Button_2"):setCallback("buttonClick", c.profilesChange, {2})
  f.getWidgetN("root/Main/Profile_Manage/Frame/Listbox/Button_3"):setCallback("buttonClick", c.profilesChange, {3})
  f.getWidgetN("root/Main/Profile_Manage/Frame/Listbox/Button_4"):setCallback("buttonClick", c.profilesChange, {4})
  f.getWidgetN("root/Main/Profile_Manage/Frame/Listbox/Button_5"):setCallback("buttonClick", c.profilesChange, {5})
  f.getWidgetN("root/Main/Profile_Manage/Frame/Listbox/Button_6"):setCallback("buttonClick", c.profilesChange, {6})
  f.getWidgetN("root/Main/Profile_Manage/Frame/Listbox/Button_Up"):setCallback("buttonClick", c.profilesScrollUp)
  f.getWidgetN("root/Main/Profile_Manage/Frame/Listbox/Button_Down"):setCallback("buttonClick", c.profilesScrollDown)
  f.getWidgetN("root/Main/Profile_Create/Frame/Button_Ok"):setCallback("buttonClick", c.profilesCreateYes)
  f.getWidgetN("root/Main/Profile_Create/Frame/Button_Cancel"):setCallback("buttonClick", c.profilesCreateNo)
  f.getWidgetN("root/Main/Profile_Delete/Frame/Button_Delete"):setCallback("buttonClick", c.profilesDeleteYes)
  f.getWidgetN("root/Main/Profile_Delete/Frame/Button_Cancel"):setCallback("buttonClick", c.profilesDeleteNo)
  f.getWidgetN("root/Main/Profile_Duplicate/Frame/Button_Ok"):setCallback("buttonClick", c.profilesDuplicateOk)
  f.getWidgetN("root/Menu_HighScores/Frame/Button_Done"):setCallback("buttonClick", c.highscoresDone)
  f.getWidgetN("root/Menu_HighScores/Frame/Button_Clear"):setCallback("buttonClick", c.highscoresClear)
  f.getWidgetN("root/Menu_ClearScores/Frame/Button_Clear"):setCallback("buttonClick", c.highscoresClearYes)
  f.getWidgetN("root/Menu_ClearScores/Frame/Button_Cancel"):setCallback("buttonClick", c.highscoresClearNo)
  f.getWidgetN("root/Menu_Options/Frame/Button_Credits"):setCallback("buttonClick", c.optionsCredits)
  f.getWidgetN("root/Menu_Options/Frame/Button_Close"):setCallback("buttonClick", c.optionsDone)
  f.getWidgetN("root/Menu_Credits/Frame/Button_Done"):setCallback("buttonClick", c.creditsDone)
  f.getWidgetN("root/Menu_Instructions/Frame/Button_OK"):setCallback("buttonClick", c.helpDone)
  f.getWidgetN("root/Menu_Continue/Frame/Button_StartNewGame"):setCallback("buttonClick", c.mainContinueNew)
  f.getWidgetN("root/Menu_Continue/Frame/Button_ContinueGame"):setCallback("buttonClick", c.mainContinueContinue)
  f.getWidgetN("root/Menu_Continue/Frame/Button_Cancel"):setCallback("buttonClick", c.mainContinueCancel)
  f.getWidgetN("root/Menu_StageSelect/Frame/StageMap/Button_Start"):setCallback("buttonClick", c.mainMapStart)
  f.getWidgetN("root/Menu_StageSelect/Frame/StageMap/Button_Cancel"):setCallback("buttonClick", c.mainMapCancel)
  f.getWidgetN("root/Menu_Game/Frame/Button_ContinuePlaying"):setCallback("buttonClick", c.gameMenuContinue)
  f.getWidgetN("root/Menu_Game/Frame/Button_Options"):setCallback("buttonClick", c.gameMenuOptions)
  f.getWidgetN("root/Menu_Game/Frame/Button_Instructions"):setCallback("buttonClick", c.gameMenuHelp)
  f.getWidgetN("root/Menu_Game/Frame/Button_QuitGame"):setCallback("buttonClick", c.gameMenuQuit)
  f.getWidgetN("root/Menu_QuitGame/Frame/Button_ContinuePlaying"):setCallback("buttonClick", c.quitMenuContinue)
  f.getWidgetN("root/Menu_QuitGame/Frame/Button_QuitToMain"):setCallback("buttonClick", c.quitMenuQuit)
  f.getWidgetN("root/Menu_QuitGame/Frame/Button_ExitGame"):setCallback("buttonClick", c.quitMenuExit)
  f.getWidgetN("root/Game/Hud/Frame/Button_Menu"):setCallback("buttonClick", c.hudMenu)
  f.getWidgetN("root/Game/Hud/Frame/Button_Pause"):setCallback("buttonClick", c.hudPause)
  f.getWidgetN("root/Game/Hud/Frame/Banner_LevelComplete/Frame/Button_Ok"):setCallback("buttonClick", c.levelCompleteOk)
  f.getWidgetN("root/Game/Hud/Frame/Banner_StageMap/Frame/StageMap/Button_Continue"):setCallback("buttonClick", c.gameMapStart)
  f.getWidgetN("root/Game/Hud/Frame/Banner_StageMap/Frame/StageMap/Button_Menu"):setCallback("buttonClick", c.gameMapCancel)
  f.getWidgetN("root/Game/Hud/Frame/Banner_Highscore/Panel/Button_Ok"):setCallback("buttonClick", c.highscoreOk)
  f.getWidgetN("root/Game/Hud/Frame/Banner_GameWin/Frame/Banner/Button_Ok"):setCallback("buttonClick", c.gameWinOk)

  for i, button in ipairs(c.StageButtons) do
    button:setCallback("buttonClick", c.mainMapSelect, {i})
  end

  for i, button in ipairs(c.NewGameStageButtons) do
    button:setCallback("buttonClick", c.mainMapSelect, {i})
  end

  -- Load options.
  c.Options_Music.widget:setValue(f.optionsGetMusicVolume())
  c.Options_Sound.widget:setValue(f.optionsGetSoundVolume())
  c.Options_Fullscreen.widget:setState(f.optionsGetFullscreen())
  c.Options_Mute.widget:setState(f.optionsGetMute())

  -- Show the menu.
  c.root:show()
  c.Main:show()
  c.Main:setActive()

  -- Prompt a user to write their name if no profiles available.
  if not f.profileGetExists() then
    c.Main:scheduleFunction("showEnd", function()
      c.Profile_Create:show()
      c.Profile_Create:setActive()
    end)
  end
end

-- WHEN CLICKED PAUSE ON HUD
function c.hudPause(f)
  if c.Banner_Paused:isVisible() then
    c.Banner_Paused:hide()
    c.Banner_Paused:scheduleFunction("hideEnd", function()
      f.levelUnpause()
    end)
  else
    c.Banner_Paused:show()
    f.levelPause()
  end
end

-- WHEN CLICKED MENU ON HUD
function c.hudMenu(f)
  if c.Banner_Paused:isVisible() then
    c.Banner_Paused:hide()
    c.Banner_Paused:scheduleFunction("hideEnd", c.hudMenu)
  else
    c.Menu_Game:show()
    c.Menu_Game:setActive()
    f.levelPause()
  end
end

-- WHEN CLICKED DONE ON LEVEL COMPLETE SCREEN
function c.levelCompleteOk(f)
  f.resetActive()
  c.Banner_LevelComplete:hide()
  c.Banner_LevelComplete:scheduleFunction("hideEnd", function()
    f.levelWin()
    c.stageMapShow(f, true)
  end)
end

-- WHEN CLICKED DONE ON GAME WIN SCREEN
function c.gameWinOk(f)
  local place = f.profileHighscoreWrite()
  if place then
    c.highscorePlace = place
    c.Banner_HighScore:show()
    c.Banner_HighScore:setActive()
  else
    c.gameWinHide(f)
  end
end

-- WHEN CLICKED "DONE" ON NEW HIGHSCORE SCREEN
function c.highscoreOk(f)
  c.Banner_HighScore:hide()
  c.Banner_HighScore:scheduleFunction("hideEnd", function()
    -- Two possibilities:
    -- 1. we won the game (show credits)
    -- 2. we lost the game (kick to main menu)
    if c.Banner_GameWin:isVisible() then
      c.gameWinHide(f)
    else
      c.Game:hide()
      c.Game:scheduleFunction("hideEnd", function()
        f.profileDeleteGame()
        c.Menu_Highscores:show()
        c.Menu_Highscores:setActive()
        c.Menu_Highscores_Highlight.y = c.highscorePlace * 45 + 62
        c.Menu_Highscores_Highlight:show()
        c.menuMusic(f, true)
      end)
    end
  end)
end

-- WHEN CLICKED "CONTINUE PLAYING" ON GAME MENU
function c.gameMenuContinue(f)
  c.Menu_Game:hide()
  c.Menu_Game:scheduleFunction("hideEnd", function()
    c.Game:setActive()
    f.levelUnpause()
  end)
end

-- WHEN CLICKED "OPTIONS" ON GAME MENU
function c.gameMenuOptions(f)
  c.Menu_Options:show()
  c.Menu_Options:setActive()
end

-- WHEN CLICKED "INSTRUCTIONS" ON GAME MENU
function c.gameMenuHelp(f)
  c.Menu_Instructions_Mask:show()
  c.Menu_Instructions_Mask:scheduleFunction("showEnd", function()
    c.Menu_Instructions:show()
    c.Menu_Instructions:showParticles()
    c.Menu_Instructions:setActive()
    c.Menu_Instructions_Toggle_DontShow.widget:setState(f.profileGetVariable("dontShowInstructions"))
  end)
end

-- WHEN CLICKED "QUIT GAME" ON GAME MENU
function c.gameMenuQuit(f)
  c.Menu_Game:hide()
  c.Menu_Game:scheduleFunction("hideEnd", function()
    c.Menu_QuitGame:show()
    c.Menu_QuitGame:setActive()
  end)
end

-- WHEN CLICKED "CONTINUE PLAYING" ON GAME QUIT MENU
function c.quitMenuContinue(f)
  c.Menu_QuitGame:hide()
  c.Menu_QuitGame:scheduleFunction("hideEnd", function()
    c.Menu_Game:show()
    c.Menu_Game:setActive()
  end)
end

-- WHEN CLICKED "EXIT GAME" ON GAME QUIT MENU
function c.quitMenuExit(f)
  f.quit()
end

-- WHEN CLICKED "QUIT TO MAIN MENU" ON GAME QUIT MENU
function c.quitMenuQuit(f)
  c.Menu_QuitGame:hide()
  c.Menu_QuitGame:scheduleFunction("hideEnd", function()
    c.Banner_QuitBackground:show()
    c.Banner_QuitBackground:scheduleFunction("showEnd", function()
      c.Banner_LevelComplete:hide()
      c.Banner_HighScore:hide()
      c.Game:hide()
      c.Game:scheduleFunction("hideEnd", function()
        f.levelSave()
        c.Banner_QuitBackground:hide()
        c.Main:show()
        c.Main:setActive()
        c.menuMusic(f, true)
      end)
    end)
  end)
end

-- WHEN CLICKED "DONE" ON OPTIONS MENU
function c.optionsDone(f)
  c.Menu_Options:hide()
  if c.Menu_Game:isVisible() then
    c.Menu_Game:setActive()
  else
    c.Main:setActive()
  end
end

-- WHEN CLICKED "CREDITS" ON OPTIONS MENU
function c.optionsCredits(f)
  c.Menu_Credits:show()
  c.Menu_Credits:setActive()
end

-- WHEN CLICKED "DONE" ON CREDITS MENU
function c.creditsDone(f)
  c.Menu_Credits:hide()
  -- Two possibilities:
  -- 1. we came from options (activate options back)
  -- 2. we came from game win (show main menu)
  c.Menu_Credits:scheduleFunction("hideEnd", function()
    if c.Menu_Options:isVisible() then
      c.Menu_Options:setActive()
    else
      c.Main:show()
      c.Main:setActive()
    end
  end)
end


-- WHEN CLICKED "OK" ON INSTRUCTIONS MENU
function c.helpDone(f)
  f.resetActive()
  c.Menu_Instructions:hide()
  c.Menu_Instructions:scheduleFunction("hideEnd", function()
    c.Menu_Instructions:hideParticles()
    -- Three possibilities:
    -- 1. from menu during level
    -- 2. popup when starting a new game
    -- 3. from menu
    if c.Menu_Game:isVisible() then
      c.Menu_Instructions_Mask:hide()
      c.Menu_Game:setActive()
    elseif c.newGameStarting then
      c.startGame(f)
    else
      c.Main:show()
      c.Main:setActive()
    end
  end)
end

-- WHEN CLICKED "DONE" ON HIGHSCORES MENU
function c.highscoresDone(f)
  f.resetActive()
  c.Menu_Highscores:hide()
  c.Menu_Highscores:scheduleFunction("hideEnd", function()
    c.Main:show()
    c.Main:setActive()
  end)
end

-- WHEN CLICKED "CLEAR" ON HIGHSCORES MENU
function c.highscoresClear(f)
  c.Menu_ClearScores:show()
  c.Menu_ClearScores:setActive()
end

-- WHEN CLICKED "YES" ON HIGHSCORE CLEAR MENU
function c.highscoresClearYes(f)
  f.highscoreReset()
  c.Menu_ClearScores:hide()
  c.Menu_Highscores:setActive()
end

-- WHEN CLICKED "YES" ON HIGHSCORE CLEAR MENU
function c.highscoresClearNo(f)
  c.Menu_ClearScores:hide()
  c.Menu_Highscores:setActive()
end

-- WHEN CLICKED "START GAME" ON MAIN MENU
function c.mainStart(f)
  if f.profileGetSession() then
    c.Menu_Continue:show()
    c.Menu_Continue:setActive()
  else
    c.stageSelectShow(f)
  end
end

-- WHEN CLICKED "OPTIONS" ON MAIN MENU
function c.mainOptions(f)
  c.Menu_Options:show()
  c.Menu_Options:setActive()
end

-- WHEN CLICKED "INSTRUCTIONS" ON MAIN MENU
function c.mainHelp(f)
  f.resetActive()
  c.Main:hide()
  c.Main:scheduleFunction("hideEnd", function()
    c.Menu_Instructions:show()
    c.Menu_Instructions:showParticles()
    c.Menu_Instructions:setActive()
    c.Menu_Instructions_Toggle_DontShow.widget:setState(f.profileGetVariable("dontShowInstructions"))
  end)
end

-- WHEN CLICKED "HALL OF FAME" ON MAIN MENU
function c.mainHighscores(f)
  f.resetActive()
  c.Main:hide()
  c.Main:scheduleFunction("hideEnd", function()
    c.Menu_Highscores:show()
    c.Menu_Highscores:setActive()
  end)
end

-- WHEN CLICKED "IF IT'S NOT YOU, CLICK HERE" ON MAIN MENU
function c.mainProfiles(f)
  c.profileManagerUpdateButtons(f)
  c.Profile_Manage:show()
  c.Profile_Manage:setActive()
end

-- WHEN CLICKED "CREATE" ON PROFILE MENU
function c.profilesCreate(f)
  c.Profile_Create:show()
  c.Profile_Create:setActive()
end

-- WHEN CLICKED "CREATE" ON PROFILE CREATE MENU
function c.profilesCreateYes(f)
  if f.profileMCreate(c.Profile_Create_Entry_Name.widget.text) then
    c.Profile_Create_Entry_Name.widget.text = ""
    c.profileManagerUpdateButtons(f)
    c.Profile_Create:hide()
    -- Profile Manage may be invisible if the creation prompt is from the main menu (no profiles exist)
    if c.Profile_Manage:isVisible() then
      c.Profile_Manage:setActive()
    else
      c.Main:setActive()
    end
  else
    c.Profile_Duplicate:show()
    c.Profile_Duplicate:setActive()
  end
end

-- WHEN CLICKED "OK" ON PROFILE DUPLICATE MENU
function c.profilesDuplicateOk(f)
  c.Profile_Duplicate:hide()
  c.Profile_Create:setActive()
end

-- WHEN CLICKED "CANCEL" ON PROFILE CREATE MENU
function c.profilesCreateNo(f)
  c.Profile_Create:hide()
  c.Profile_Manage:setActive()
end

-- WHEN CLICKED "DELETE" ON PROFILE MENU
function c.profilesDelete(f)
  c.Profile_Delete_Text_Name.widget.text = f.profileMGetNameOrder()[c.profileSelectID]
  c.Profile_Delete:show()
  c.Profile_Delete:setActive()
end

-- WHEN CLICKED "DELETE" ON PROFILE DELETE MENU
function c.profilesDeleteYes(f)
  f.profileMDelete(f.profileMGetNameOrder()[c.profileSelectID])
  c.profileManagerUpdateButtons(f)
  c.Profile_Delete:hide()
  c.Profile_Manage:setActive()
end

-- WHEN CLICKED "CANCEL" ON PROFILE DELETE MENU
function c.profilesDeleteNo(f)
  c.Profile_Delete:hide()
  c.Profile_Manage:setActive()
end

-- WHEN CLICKED "SELECT" ON PROFILE MENU
function c.profilesSelect(f)
  f.profileMSet(f.profileMGetNameOrder()[c.profileSelectID])
  c.Profile_Manage:hide()
  c.Main:setActive()
end

-- WHEN CLICKED "CANCEL" ON PROFILE MENU
function c.profilesCancel(f)
  c.Profile_Manage:hide()
  c.Main:setActive()
  -- If no profiles, prompt for addition of one
  if not f.profileGetExists() then
    c.Profile_Manage:scheduleFunction("hideEnd", function()
      c.Profile_Create:show()
      c.Profile_Create:setActive()
    end)
  end
end

-- WHEN CLICKED AN ENTRY ON PROFILE MENU
function c.profilesChange(f, params)
  local id = params[1]
  c.profileSelectID = id + c.profileOffset
  c.profileManagerUpdateButtons(f)
end

-- WHEN SCROLLED UP ON PROFILE MENU
function c.profilesScrollUp(f)
  c.profileOffset = c.profileOffset - 1
  c.profileManagerUpdateButtons(f)
end

-- WHEN SCROLLED DOWN ON PROFILE MENU
function c.profilesScrollDown(f)
  c.profileOffset = c.profileOffset + 1
  c.profileManagerUpdateButtons(f)
end

-- WHEN CLICKED QUIT ON MAIN MENU
function c.mainQuit(f)
  f.quit()
end

-- WHEN CLICKED NEW GAME ON CONTINUE MENU
function c.mainContinueNew(f)
  c.Menu_Continue:hide()
  c.Menu_Continue:scheduleFunction("hideEnd", c.stageSelectShow)
end

-- WHEN CLICKED CONTINUE GAME ON CONTINUE MENU
function c.mainContinueContinue(f)
  local hasSavedLevel = f.profileGetSavedLevel()
  c.Menu_Continue:hide()
  c.Menu_Continue:scheduleFunction("hideEnd", function()
    if hasSavedLevel then
      c.menuMusic(f, false)
    end
    c.Main:hide()
    c.Game:show()
    c.Main:scheduleFunction("hideEnd", function()
      if hasSavedLevel then
        c.Game:setActive()
        f.levelStart()
      else
        c.stageMapShow(f, false)
      end
    end)
  end)
end

-- WHEN CLICKED CANCEL ON CONTINUE MENU
function c.mainContinueCancel(f)
  c.Menu_Continue:hide()
  c.Main:setActive()
end

-- WHEN CLICKED START ON LEVEL MAP
function c.mainMapStart(f)
  f.resetActive()
  f.profileNewGame(c.newGameStage, "difficulties/default.json")
  c.Menu_StageSelect:hide()
  c.Menu_StageSelect:scheduleFunction("hideEnd", function()
    c.Menu_StageSelect_LevelPsys:hide()
    c.menuMusic(f, false)
    if not f.profileGetVariable("dontShowInstructions") then
      c.newGameStarting = true
      c.Menu_Instructions:show()
      c.Menu_Instructions:showParticles()
      c.Menu_Instructions:setActive()
      c.Menu_Instructions_Toggle_DontShow.widget:setState(f.profileGetVariable("dontShowInstructions"))
    else
      c.startGame(f)
    end
  end)
end

-- WHEN CLICKED CANCEL ON LEVEL MAP
function c.mainMapCancel(f)
  f.resetActive()
  c.Menu_StageSelect:hide()
  c.Menu_StageSelect:scheduleFunction("hideEnd", function()
    c.Menu_StageSelect_LevelPsys:hide()
    c.Main:show()
    c.Main:setActive()
  end)
end

-- WHEN CLICKED A STAGE BUTTON ON LEVEL MAP
function c.mainMapSelect(f, params)
  local stage = params[1]
  c.newGameStage = stage
  c.stageSelectUpdateButtons(f)
end

-- WHEN CLICKED START ON LEVEL MAP 2
function c.gameMapStart(f)
  f.resetActive()
  c.menuMusic(f, false)
  c.Banner_StageMap:hide()
  c.Banner_StageMap:scheduleFunction("hideEnd", function()
    c.Banner_StageMap_LevelPsys:hide()
    c.Banner_StageMapTrans:hide()
    c.Banner_StageMapTrans:scheduleFunction("hideEnd", function()
      c.Game:setActive()
      f.levelStart()
    end)
  end)
end

-- WHEN CLICKED CANCEL ON LEVEL MAP 2
function c.gameMapCancel(f)
  f.resetActive()
  c.Game:hide()
  c.Banner_StageMap:hide()
  c.Banner_StageMap:scheduleFunction("hideEnd", function()
    c.Banner_StageMap_LevelPsys:hide()
    c.Banner_StageMapTrans:hide()
    c.Banner_StageMapTrans:scheduleFunction("hideEnd", function()
      c.Main:show()
      c.Main:setActive()
    end)
  end)
end

----------------------
-- GLOBAL CALLBACKS --
----------------------

function c.tick(f)
  -- update splash screen
  local splash = f.getWidgetN("splash")
  if splash then
    local splashProgress = f.getWidgetN("splash/Frame/Progress")
    local splashPlay = f.getWidgetN("splash/Frame/Button_Play")
    local progress = f.loadingGetProgress()
    splashProgress.widget.valueData = progress
    if progress == 1 then
      splashPlay.x, splashPlay.y = splashProgress.x, splashProgress.y
    end
  end

  -- when the options menu is open, update options to the widget positions

  -- The "if Menu_Options" check refers to the existence of the widget itself.
  -- Note that this script is loaded when the splash screen starts, and most of
  -- the widgets do not exist at this point yet.
  if c.Menu_Options and c.Menu_Options:isVisible() then
    -- Save options.
    f.optionsSetMusicVolume(c.Options_Music.widget.value)
    f.optionsSetSoundVolume(c.Options_Sound.widget.value)
    f.optionsSetFullscreen(c.Options_Fullscreen.widget.state)
    f.optionsSetMute(c.Options_Mute.widget.state)
  end

  if c.Profile_Create and c.Profile_Create:isVisible() then
    c.Profile_Create_Button_Cancel:buttonSetEnabled(f.profileGetExists())
    c.Profile_Create_Button_Ok:buttonSetEnabled(c.Profile_Create_Entry_Name.widget.text:len() > 0)
  end

  if c.Menu_Instructions and c.Menu_Instructions:isVisible() then
    f.profileSetVariable("dontShowInstructions", c.Menu_Instructions_Toggle_DontShow.widget.state)
  end

  -- Update texts
  if c.Banner_StageMap then
    local player = ""
    if f.profileGetExists() then
      player = f.profileGetName()

      if f.profileGetSession() then
        local lives = tostring(f.profileGetLives())
        local coins = tostring(f.profileGetCoins())
        local score = f.profileGetScore()
        local scoreStr = _Utils.formatNumber(score)
        if c.scoreDisplay < score then
          c.scoreDisplay = c.scoreDisplay + math.ceil((score - c.scoreDisplay) / 10)
        elseif c.scoreDisplay > score then
          c.scoreDisplay = c.scoreDisplay + math.floor((score - c.scoreDisplay) / 10)
        end
        local scoreAnim = _Utils.formatNumber(c.scoreDisplay)
        local levelName = f.profileGetLevelName()
        local levelMapName = f.profileGetMap().name
        local stageName = c.stageNames[f.profileGetLatestCheckpoint()]

        c.Menu_Continue_Text_Stage.widget.text = "STAGE " .. levelName
        c.Menu_Continue_Text_Score.widget.text = scoreStr

        c.Hud_Text_Stage.widget.text = levelName
        c.Hud_Text_Lives.widget.text = lives
        c.Hud_Text_Coins.widget.text = coins
        c.Hud_Text_Score.widget.text = scoreAnim

        c.Banner_StageMap_Text_StageName.widget.text = stageName
        c.Banner_StageMap_Text_StageNumber.widget.text = "STAGE " .. levelName
        c.Banner_StageMap_Text_MapName.widget.text = levelMapName

        c.Banner_HighScore_Text_Congrats.widget.text = "CONGRATULATIONS, " .. player .. "!"
        c.Banner_HighScore_Text_Score.widget.text = scoreStr

        c.Banner_Intro_Text_Stage.widget.text = "STAGE " .. levelName
        c.Banner_Intro_Text_Map.widget.text = levelMapName

        -- Level
        if f.levelExists() then
          local levelProgress = f.levelGetProgress()
          local levelScore = _Utils.formatNumber(f.levelGetScore())
          local levelShots = tostring(f.levelGetShots())
          local levelCoins = tostring(f.levelGetCoins())
          local levelGems = tostring(f.levelGetGems())
          local levelChains = tostring(f.levelGetChains())
          local levelMaxCombo = tostring(f.levelGetMaxStreak())
          local levelMaxChain = tostring(f.levelGetMaxCascade())

          c.Hud_Progress.widget.valueData = levelProgress
          local complete = c.Hud_Progress.widget.value == 1
          if complete ~= c.progressComplete then
            c.progressComplete = complete
            if complete then
              c.Hud_Progress_Complete:show()
              f.playSound("sound_events/progress_complete.json")
            else
              c.Hud_Progress_Complete:hide()
            end
          end

          c.Banner_LevelComplete_Text_Stage.widget.text = "STAGE " .. levelName
          c.Banner_LevelComplete_Text_MapName.widget.text = levelMapName
          c.Banner_LevelComplete_Text_LevelScore.widget.text = levelScore
          c.Banner_LevelComplete_Text_ShotsFired.widget.text = levelShots
          c.Banner_LevelComplete_Text_MaxCombo.widget.text = levelMaxCombo
          c.Banner_LevelComplete_Text_Coins.widget.text = levelCoins
          c.Banner_LevelComplete_Text_MaxChain.widget.text = levelMaxChain
          c.Banner_LevelComplete_Text_Gems.widget.text = levelGems
          c.Banner_LevelComplete_Text_Segments.widget.text = levelChains
        end
      end

      -- New game
      local newCheckpointID = f.configGetCheckpointID("level_sets/adventure.json", c.newGameStage)
      local newLevelData = f.configGetLevelData("level_sets/adventure.json", newCheckpointID)
      local newLevelName = f.configGetLevelName("level_sets/adventure.json", newCheckpointID)
      local newLevelMapName = f.configGetMapData(newLevelData.map).name
      local newStageName = c.stageNames[c.newGameStage]


      c.Main_Text_PlayerE.widget.text = player
      c.Main_Text_PlayerH.widget.text = player
      if c.Main_Text_Version then
        c.Main_Text_Version.widget.text = "Running on OpenSMCE " .. _VERSION
      end

      for i, row in ipairs(c.HighscoreRows) do
        local entry = f.highscoreGetEntry(i)
        row.rank.widget.text = tostring(i)
        row.name.widget.text = entry.name
        if row.name2 then
          row.name2.widget.text = entry.name
        end
        row.level.widget.text = entry.level
        row.score.widget.text = _Utils.formatNumber(entry.score)
      end

      c.Menu_StageSelect_Text_StageName.widget.text = newStageName
      c.Menu_StageSelect_Text_StageNumber.widget.text = "STAGE " .. newLevelName
      c.Menu_StageSelect_Text_MapName.widget.text = newLevelMapName
    end
  end
end

function c.lostFocus(f)
  if c.Button_Pause and c.Button_Pause:isActive() and c.Button_Pause:isButtonEnabled() and not c.Banner_Paused:isVisible() then
    c.Banner_Paused:show()
    f.levelPause()
  end
end

function c.levelStart(f)
  c.Banner_Intro:show()
  c.Banner_Intro:hideAfter(2.75)
  c.Banner_Intro:scheduleFunction("hideEnd", function()
    f.levelRestartMusic()
    f.levelContinue()
    c.Button_Pause:buttonSetEnabled(true)
  end)
end

function c.levelLoaded(f)
  f.levelRestartMusic()
  c.Banner_Paused:show()
  c.Button_Pause:buttonSetEnabled(true)
end

function c.levelComplete(f)
  c.Button_Pause:buttonSetEnabled(false)
  c.Banner_LevelComplete:show()
  -- Stats
  for i, data in ipairs(c.levelCompleteSequence) do
    data.widget:showAfter(data.delay)
    data.widget:scheduleFunction("showStart", function()
      data.widget:showParticles()
      f.playSound("sound_events/score_tally.json")
    end)
  end
  -- Level Record
  c.Banner_LevelComplete_Record:hide()
  if f.levelGetNewRecord() then
    c.Banner_LevelComplete_Record:showAfter(1)
    c.Banner_LevelComplete_Record:scheduleFunction("showStart", function()
      f.playSound("sound_events/new_record.json")
    end)
  end
end

function c.levelLost(f)
  c.Button_Pause:buttonSetEnabled(false)
  c.Banner_LevelLose:show()
  c.Banner_LevelLose:hideAfter(2.5)
  c.Banner_LevelLose:scheduleFunction("hideEnd", function()
    f.levelRestart()
  end)
end

function c.gameOver(f)
  c.Banner_GameOver:show()
  c.Banner_GameOver:hideAfter(2.5)
  c.Button_Menu:buttonSetEnabled(false)
  c.Banner_GameOver:scheduleFunction("hideEnd", function()
    local place = f.profileHighscoreWrite()
    if place then
      c.highscorePlace = place
      c.Banner_HighScore:show()
      c.Banner_HighScore:setActive()
    else
      c.Game:hide()
      c.Game:scheduleFunction("hideEnd", function()
        f.profileDeleteGame()
        c.Main:show()
        c.Main:setActive()
        c.menuMusic(f, true)
      end)
    end
  end)
end

function c.newLife(f)
  c.Hud_NewLife:show()
  f.playSound("sound_events/extra_life.json")
end

----------------------
-- HELPER FUNCTIONS --
----------------------

function c.menuMusic(f, state)
  f.musicVolume("music_tracks/menu_music.json", state and 1 or 0, 1)
end

function c.startGame(f)
  c.newGameStarting = false
  c.Game:show()
  c.Game:scheduleFunction("showEnd", function()
    c.Game:setActive()
    c.Button_Menu:buttonSetEnabled(true)
    f.levelStart()
  end)
end

function c.stageMapShow(f, advance)
  c.Banner_StageMapTrans:show()
  c.Banner_StageMapTrans:scheduleFunction("showEnd", function()
    c.stageMapUpdateButtons(f)
    c.Banner_StageMap:show()
    c.Banner_StageMap_LevelPsys:show()
    if advance then
      c.Banner_StageMap:scheduleFunction("showEnd", function()
        if f.profileGetLevel() == f.configGetLevelCount("level_sets/adventure.json") or f.profileIsCheckpointUpcoming() then
          f.playSound("sound_events/stage_complete.json")
          c.Banner_StageMap_StageCompletePsys:show()
          c.Banner_StageMap_StageCompletePsys:scheduleFunction("particleDespawn", function()
            if f.profileIsCheckpointUpcoming() then
              f.playSound("sound_events/level_advance.json")
              f.profileLevelAdvance()
              c.stageMapSetActive(f)
              c.menuMusic(f, true)
              c.Banner_StageMap_StageUnlockPsys:show()
            else
              c.Banner_StageMap:hide()
              c.Banner_StageMap:scheduleFunction("hideEnd", function()
                -- Game Won!
                f.playSound("sound_events/game_win.json")
                c.Banner_GameWin:show()
                c.Banner_GameWin:setActive()
                c.Banner_StageMap_LevelPsys:hide()
              end)
            end
          end)
        else
          f.playSound("sound_events/level_advance.json")
          f.profileLevelAdvance()
          c.stageMapSetActive(f)
          c.menuMusic(f, true)
        end
      end)
    else
      c.stageMapSetActive(f)
    end
  end)
end

function c.stageMapSetActive(f)
  c.Banner_StageMap:setActive()
  c.Banner_StageMap_StageButtons:resetActive()
  c.Banner_StageMap_LevelButtons:resetActive()
  c.stageMapUpdateButtons(f)
end

function c.stageMapUpdateButtons(f)
  local s = f.profileGetLatestCheckpoint()
  for i, StageButton in ipairs(c.StageButtons) do
    StageButton:buttonSetEnabled(i <= s)
    StageButton.widget.clickedV = i == s
    if i == s then
      c.Banner_StageMap_StageUnlockPsys.x, c.Banner_StageMap_StageUnlockPsys.y = StageButton.x + 32, StageButton.y + 32
    end
  end
  if s == f.configGetCheckpointCount("level_sets/adventure.json") then
    c.Banner_StageMap_Set:show()
  else
    c.Banner_StageMap_Set:hide()
  end

  local n = f.profileGetLevel()
  for i, LevelButton in ipairs(c.LevelButtons) do
    if i < n then
      LevelButton:show()
    else
      LevelButton:hide()
    end
    if i == n then
      c.Banner_StageMap_LevelPsys.x, c.Banner_StageMap_LevelPsys.y = LevelButton.x, LevelButton.y
    end
  end
end

function c.stageSelectShow(f)
  c.Main:hide()
  c.Main:scheduleFunction("hideEnd", function()
    -- latest checkpoint will be selected by default
    local checkpoints = f.profileGetUnlockedCheckpoints("level_sets/adventure.json")
    c.newGameStage = checkpoints[#checkpoints]
    --
    c.stageSelectUpdateButtons(f)
    c.Menu_StageSelect:show()
    c.Menu_StageSelect_LevelPsys:show()
    c.Menu_StageSelect:setActive()
    c.Menu_StageSelect_LevelButtons:resetActive()
  end)
end

function c.stageSelectUpdateButtons(f)
  c.Menu_StageSelect_StageButtons:show()

  local n = f.configGetCheckpointLevel("level_sets/adventure.json", c.newGameStage)
  for i, LevelButton in ipairs(c.NewGameLevelButtons) do
    if i < n then
      LevelButton:show()
    else
      LevelButton:hide()
    end
    if i == n then
      c.Menu_StageSelect_LevelPsys.x, c.Menu_StageSelect_LevelPsys.y = LevelButton.x, LevelButton.y
    end
  end

  local s = c.newGameStage
  for i, StageButton in ipairs(c.NewGameStageButtons) do
    StageButton:buttonSetEnabled(f.profileIsCheckpointUnlocked("level_sets/adventure.json", i))
    StageButton.widget.clickedV = i == s
  end
  if s == f.configGetCheckpointCount("level_sets/adventure.json") then
    c.Menu_StageSelect_Set:show()
  else
    c.Menu_StageSelect_Set:hide()
  end
end

function c.profileManagerUpdateButtons(f)
  local names = f.profileMGetNameOrder()

  if c.profileSelectID > #names then
    c.profileSelectID = #names
  end
  if c.profileOffset > 0 and c.profileOffset > #names - #c.ProfileRows then
    c.profileOffset = #names - #c.ProfileRows
  end

  local s = c.profileSelectID
  for i, row in ipairs(c.ProfileRows) do
    local n = c.profileOffset + i
    local name = names[n] or ""
    row.name.widget.text = name
    row.name2.widget.text = name
    row.button:buttonSetEnabled(names[n])
    row.button.widget.clickedV = n == s
  end

  c.Profile_Manage_Button_Up:buttonSetEnabled(c.profileOffset > 0)
  c.Profile_Manage_Button_Down:buttonSetEnabled(c.profileOffset < #names - #c.ProfileRows)
  c.Profile_Manage_Button_Delete:buttonSetEnabled(c.profileSelectID > 0)
  c.Profile_Manage_Button_Select:buttonSetEnabled(c.profileSelectID > 0)
end

function c.gameWinHide(f)
  c.Banner_GameWin:hide()
  c.Banner_GameWin:scheduleFunction("hideEnd", function()
    c.Game:hide()
    c.Game:scheduleFunction("hideEnd", function()
      c.Banner_StageMapTrans:hide()
    end)
    f.profileDeleteGame()
    c.Menu_Credits:show()
    c.Menu_Credits:setActive()
    c.menuMusic(f, true)
  end)
end

-- Now we need to carry all functions that we've inserted over to the engine.
return c
