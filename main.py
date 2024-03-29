from cmu_112_graphics import *
import jetC
import mslC
import random
import nmyJetC


################################################
# first-person view (bonus feature)
################################################

def appStarted(app):
    app.score = 0
    app.planeFullHealth = 100
    app.planeHealth = 100
    app.damage = 10
    app.circleRadius = 50

def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app)

def drawJetFirstPerson(app, canvas):
    e = 180
    canvas.create_arc(0, 1/9*app.height, app.width, app.height, style = 'arc', extent=e,
                        outline = 'gray', width = 1/20*app.height)
    canvas.create_arc(0, 1/10*app.height, app.width, app.height, style = 'arc', extent=e,
                        outline = 'black', width = 1/20*app.height)
    canvas.create_line(0, 1/2*app.height, app.width, 1/2*app.height, fill = 'black', 
                        width = 1/20*app.height)

def drawJetBirdEye(app, canvas):
    pass

def drawHealthBar(app, canvas):
    x0, x1, y0, y1 = 0, 1/5*app.width, 0, 1/50*app.height
    # each bar represents 20% of health
    for bar in range(5):
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'red', outline = 'black')
        x0 += 1/5*app.width
        x1 += 1/5*app.width
    # health percentage

def firstPerson_redrawAll(app, canvas):
    drawJetFirstPerson(app, canvas)
    drawHealthBar(app, canvas)

def firstPerson_keyPressed(app, event):
    pass

def firstPerson_mousePressed(app, event):
    pass

################################################
# home screen
################################################

def drawHomeScreen(app, canvas):
    cx = app.width//2
    cy = app.height//2
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_rectangle(cx-300, cy-350, cx+300, cy+350, fill = 'black', 
                            outline = 'red')
    canvas.create_text(cx, cy-200, text = 'missileAirDefense', 
                        font = 'Courier 50 bold', fill = 'red')

def start_redrawAll(app, canvas):
    drawHomeScreen(app, canvas)
    for jet in app.startEnemyJets:
        drawEnemyJet(app, canvas, jet[0], jet[1], 1)
    for missile in app.enemyMissiles:
        missile.redraw(app, canvas)

    # draw "choose your fighter"
    canvas.create_text(app.width//2, app.height-200, text = 'Choose Your Fighter',
                        font = 'Courier 30 bold', fill = 'maroon')
    # draw selection of jets 
    app.Hawk.redraw(app, canvas)
    app.Falcon.redraw(app, canvas)
    app.Thunderbolt.redraw(app, canvas)
    

def start_mousePressed(app, event):
    # when you click on figter jet, screen will show strengths and weaknesses of jet
    if app.width//2-80 <= event.x <= app.width//2+80:
        if (4*app.height/5-10) <= event.y <= (app.height-30):
            app.mode = 'hawkInfo'
    if app.width//3-80 <= event.x <= app.width//3+80:
        if (4*app.height/5-10) <= event.y <= (app.height-30):
            app.mode = 'falconInfo'
    if 2*app.width//3-80 <= event.x <= 2*app.width//3+80:
        if (4*app.height/5-10) <= event.y <= (app.height-30):
            app.mode = 'thunderboltInfo'

def start_mouseMoved(app, event):
    # when you hover over fighter the outline of jet will turn white
    if app.width//2-80 <= event.x <= app.width//2+80:
        if (4*app.height/5-10) <= event.y <= (app.height-30):
            app.Hawk.color = 'white'
    else:
        app.Hawk.color = 'black'
    if app.width//3-80 <= event.x <= app.width//3+80:
        if (4*app.height/5-10) <= event.y <= (app.height-30):
            app.Falcon.color = 'white'
    else:
        app.Falcon.color = 'black'
    if 2*app.width//3-80 <= event.x <= 2*app.width//3+80:
        if (4*app.height/5-10) <= event.y <= (app.height-30):
            app.Thunderbolt.color = 'white'
    else:
        app.Thunderbolt.color = 'black'

def start_timerFired(app):
    app.timePassed += 2*app.timerDelay
    
    # spawn jets
    enemySpawnX0 = random.randint(50, app.width//2-350)
    enemySpawnX1 = random.randint(app.width//2+350, app.width-100)
    L = [enemySpawnX0, enemySpawnX1]
    for x in L:
        bound1 = x - 100
        bound2 = x + 100
        if len(app.startEnemyJets) <= 1:
            if isNotOverlap(app, bound1, bound2):
                app.enemyJetXCoord.add(x)
                app.startEnemyJets.append([x, app.enemySpawnY0])
        
    # move jets
    for coordinate in app.startEnemyJets:
        coordinate[1] += 2
        if coordinate[1] >= app.height:
            app.startEnemyJets.remove(coordinate)
            app.enemyJetXCoord.remove(coordinate[0])
    
    # add missiles to enemy jet
    if app.timePassed % 500 == 0:
        for coordinate in app.startEnemyJets:
            missileType = random.choice(app.enemyMissileTypes)
            if missileType == 'linear':
                missile = mslC.Linear(coordinate[0], coordinate[1])
            elif missileType == 'sin':
                missile = mslC.Sinusoidal(coordinate[0], coordinate[1])
            elif missileType == 'para1':
                missile = mslC.Parabolic(coordinate[0], coordinate[1])
            elif missileType == 'para2':
                missile = mslC.Parabolic2(coordinate[0], coordinate[1])
            elif missileType == 'cubic':
                missile  = mslC.Cubic(coordinate[0], coordinate[1])
            app.enemyMissiles.append(missile)
    
    # shoot missiles
    for missile in app.enemyMissiles:
        missile.eq()


################################################
# jet information screen
################################################
def drawHealth(app, canvas, health):
    canvas.create_rectangle(app.width//2-450, app.height//2+75, app.width//2+450, 
                            app.height//2+65, fill = 'black', outline = 'black')
    x0 = app.width//2-450
    y0 = app.height//2+75
    x1 = x0+7
    y1 = app.height//2+65
    for bar in range(health//2+1):
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'red', outline = 'black')
        x0, x1 = x1, x0+7
    canvas.create_text(300, y0-20, text = 'health', fill = 'white', 
                        font = 'Courier 14 bold')

def drawSpeed(app, canvas, speed):
    canvas.create_rectangle(app.width//2-450, app.height//2+95, app.width//2+450, 
                            app.height//2+105, fill = 'black', outline = 'black')
    x0 = app.width//2-450
    y0 = app.height//2+95
    x1 = x0+17
    y1 = app.height//2+105
    for bar in range(speed//2+1):
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'red', outline = 'black')
        x0, x1 = x1, x0+17
    canvas.create_text(295, y0-10, text = 'speed', fill = 'white', 
                        font = 'Courier 14 bold')

# Hawk's Info
###############################################
def hawkInfo_redrawAll(app, canvas):
    cx = app.width//2
    cy = app.height//2
    canvas.create_rectangle(0, 0, app.width, app.height,
                            fill = 'black')
    canvas.create_rectangle(cx-500, cy-150, cx+500, cy+150, fill = 'gray21',
                            outline = 'medium sea green')
    canvas.create_rectangle(cx-70, cy+200, cx+70, cy+250, fill = 'red', 
                            outline = 'black')
    canvas.create_text(cx, cy+225, text = 'Play', font = 'Courier 20 bold',
                        fill = 'black')
    colors = ['medium sea green', 'OliveDrab4', 'LightSteelBlue4', 'black', 'OliveDrab4',
                 'gray16', 'gray16', 'OliveDrab4', 'gray55', 'gray55']
    drawUserJet(app, canvas, app.width//2, app.height//2-100, colors, 'Hawk')
    drawHealth(app, canvas, app.Hawk.health)
    drawSpeed(app, canvas, app.Hawk.speed)
    canvas.create_rectangle(app.width//2-70, 75, app.width//2+70, 125, 
                            fill = 'maroon', outline = 'black')
    canvas.create_text(app.width//2, 100, 
                        text = 'Back',
                        fill = 'black', font = 'Courier 20 bold')

def hawkInfo_keyPressed(app, event):
    if event.key == 'Return':
        appStarted(app)
        app.userJet = app.jetSelection[0]
        app.userJetFull = app.userJet.health
        app.mode = 'gameMode'

def hawkInfo_mousePressed(app, event):
    cx = app.width//2
    cy = app.height//2
    if cx-70 <= event.x <= cx+70:
        if cy+200 <= event.y <= cy+250:
            appStarted(app)
            app.userJet = app.jetSelection[0]
            app.userJetFull = app.userJet.health
            app.mode = 'gameMode'
    if cx-70 <= event.x <= cx+70:
        if 75 <= event.y <= 125:
            app.mode = 'start'

# Falcon's Info
###############################################
def falconInfo_redrawAll(app, canvas):
    cx = app.width//2
    cy = app.height//2
    canvas.create_rectangle(0, 0, app.width, app.height,
                            fill = 'black')
    canvas.create_rectangle(cx-500, cy-150, cx+500, cy+150, fill = 'grey10',
                            outline = 'GreenYellow')
    canvas.create_rectangle(cx-70, cy+200, cx+70, cy+250, fill = 'red', 
                            outline = 'black')
    canvas.create_text(cx, cy+225, text = 'Play', font = 'Courier 20 bold',
                        fill = 'black')
    colors = ['bisque4', 'bisque4', 'GreenYellow', 'green', 'burlywood4', 
            'burlywood4', 'burlywood4', 'burlywood4', 'coral4', 'coral4']
    drawUserJet(app, canvas, app.width//2, app.height//2-100, colors, 'Falcon')
    drawHealth(app, canvas, app.Falcon.health)
    drawSpeed(app, canvas, app.Falcon.speed)
    canvas.create_rectangle(app.width//2-70, 75, app.width//2+70, 125, 
                            fill = 'maroon', outline = 'black')
    canvas.create_text(app.width//2, 100, 
                        text = 'Back',
                        fill = 'black', font = 'Courier 20 bold')

def falconInfo_keyPressed(app, event):
    if event.key == 'Return':
        appStarted(app)
        app.userJet = app.jetSelection[1]
        app.userJetFull = app.userJet.health
        app.mode = 'gameMode'

def falconInfo_mousePressed(app, event):
    cx = app.width//2
    cy = app.height//2
    if cx-70 <= event.x <= cx+70:
        if cy+200 <= event.y <= cy+250:
            appStarted(app)
            app.userJet = app.jetSelection[1]
            app.userJetFull = app.userJet.health
            app.mode = 'gameMode'
    if cx-70 <= event.x <= cx+70:
        if 75 <= event.y <= 125:
            app.mode = 'start'


# Thunderbolt's Info
###############################################
def thunderboltInfo_redrawAll(app, canvas):
    cx = app.width//2
    cy = app.height//2
    canvas.create_rectangle(0, 0, app.width, app.height,
                            fill = 'black')
    canvas.create_rectangle(cx-500, cy-150, cx+500, cy+150, fill = 'grey15',
                            outline = 'medium slate blue')
    canvas.create_rectangle(cx-70, cy+200, cx+70, cy+250, fill = 'red',
                            outline = 'black')
    canvas.create_text(cx, cy+225, text = 'Play', font = 'Courier 20 bold',
                        fill = 'black')
    canvas.create_rectangle(app.width//2-70, 75, app.width//2+70, 125, 
                            fill = 'maroon', outline = 'black')
    canvas.create_text(app.width//2, 100, 
                        text = 'Back',
                        fill = 'black', font = 'Courier 20 bold')
    colors = ['grey61', 'grey30', 'medium slate blue', 'purple', 'grey35', 
            'grey35', 'grey35', 'grey35', 'MediumPurple4', 'MediumPurple4']
    drawUserJet(app, canvas, app.width//2, app.height//2-100, colors, 'Thunderbolt')
    drawHealth(app, canvas, app.Thunderbolt.health)
    drawSpeed(app, canvas, app.Thunderbolt.speed)
    

def thunderboltInfo_keyPressed(app, event):
    if event.key == 'Return':
        appStarted(app)
        app.userJet = app.jetSelection[2]
        app.userJetFull = app.userJet.health
        app.mode = 'gameMode'

def thunderboltInfo_mousePressed(app, event):
    cx = app.width//2
    cy = app.height//2
    if cx-70 <= event.x <= cx+70:
        if cy+200 <= event.y <= cy+250:
            appStarted(app)
            app.userJet = app.jetSelection[2]
            app.userJetFull = app.userJet.health
            app.mode = 'gameMode'
    if cx-70 <= event.x <= cx+70:
        if 75 <= event.y <= 125:
            app.mode = 'start'

################################################
# game play (bird-eye view)
################################################

def appStarted(app):
    # starting screen
    app.mode = 'start'
    app.startEnemyJets = []

    # gameplay features/information
    app.score = 0
    app.gameOver = False
    app.timePassed = 0
    app.difficultyTracker = 0
    # app.enemyJetCapacity = 0
    app.enemyJetCapacity = 0
    app.timerDelay = 10
    app.pause = False
    app.mslPerSec = 2000 # increase fire rate by 0.04s every 10 targets down

    # enemy jet's coordinates
    app.enemySpawnX0 = random.randint(60, app.width-110)
    app.enemySpawnY0 = 0
    app.enemyJets = []
    app.enemyJetXCoord = set()
    # enemy jet's missiles
    app.enemyMissiles = []

    # user jet's coordinates
    app.UserX = app.width//2
    app.UserY = app.height-(1/5*app.height)

    # user jet's missiles
    app.specialActivated = False
    app.MissilesInAir = 0
    app.userMissiles = []
    # app.image1 = 

    # selection of Jets (for user)
    Hawk = jetC.Hawk(400, 100, app.UserX, app.UserY, 'black')
    Falcon = jetC.Falcon(500, 75, app.UserX, app.UserY, 'black')
    Thunderbolt = jetC.Thunderbolt(300, 150, app.UserX, app.UserY, 'black')
    app.jetSelection = [Hawk, Falcon, Thunderbolt]

    # types of missiles (for enemy)
    # app.enemyMissileTypes = ['cubic']
    app.enemyMissileTypes = ['para1', 'para2', 'cubic']

    # home screen selection
    app.Hawk = jetC.Hawk(400, 100, app.width//2, app.height-(1/5*app.height), 'black')
    app.Falcon = jetC.Falcon(500, 75, app.width//3, app.height-(1/5*app.height), 'black')
    app.Thunderbolt = jetC.Thunderbolt(300, 150, 2*app.width//3, app.height-(1/5*app.height), 'black')

    # enemy jet selections 
    app.enemyJetChoice = ['bomber', 'light', 'light', 'light', 'light', 'torpedo']
    # app.enemyJetChoice = ['torpedo']
    app.squadron = nmyJetC.Squadron()

    # key released
    app.pressedKey = None
    app.count = 0


def gameMode_mousePressed(app, event):
    if app.gameOver:
        return
    if app.pause:
        if app.width//2-140 <= event.x <= app.width//2-30:
            if app.height//2+20 <= event.y <= app.height//2+60:
                app.pause = False
        if app.width//2+30 <= event.x <= app.width//2+140:
            if app.height//2+20 <= event.y <= app.height//2+60:
                appStarted(app)
                app.mode = 'start'
        return

    # if game is not over
    if 25 <= event.x <= 50 and 25 <= event.y <= 50:
        app.pause = not app.pause
    else:
        if app.specialActivated:
            getUserMissileCoord(app)
        else:
            getUserMissileCoord(app)
        if app.MissilesInAir > 30:
            app.gameOver = not app.gameOver
            app.userJet.health = 0
            
def gameMode_keyPressed(app, event):
    app.pressedKey = event.key

    if event.key == 'r':
        appStarted(app)

    if app.gameOver:
        return

    if event.key == 'p':
        app.pause = not app.pause
    
    if app.pause:
        return

    # keys accessible when game is not paused or over
    # shoot missiles from user jet
    if event.key == 't':
        app.specialActivated = not app.specialActivated


def gameMode_keyReleased(app, event):
    app.pressedKey = None
    app.count = 0
        
def gameMode_mouseMoved(app, event):
    if app.gameOver:
        return
    if app.pause:
        return
    else: 
        app.userJet.UserX = event.x
       
def gameMode_timerFired(app):
    if app.userJet.health <= 0:
        app.gameOver = True
        return
    if app.pause:
        return
    app.timePassed += app.timerDelay
    app.difficultyTracker += app.timerDelay
    if app.difficultyTracker == 15000:
        app.difficultyTracker = 0
        app.enemyJetCapacity += 1
    if app.pressedKey == 's' and app.timePassed % 40 == 0:
        app.count += 1
        if app.specialActivated:
            getUserMissileCoord(app)
        else:
            getUserMissileCoord(app)
        if app.MissilesInAir > 30:
            app.gameOver = not app.gameOver
            app.userJet.health = 0
            
    
    # if game is not paused or over
    if len(app.enemyJets) <= app.enemyJetCapacity and app.timePassed % 100 == 0:
        createEnemyJetVariation(app, getSquadronSize(app)[0], 
                                getSquadronSize(app)[1], 
                                validCoord(app), 0)
    if len(app.enemyJets) > 0 and app.timePassed % 5 == 0:
        # debug
        moveEnemyJet(app)
    # need to set general variable for addEnemyMissile (default = 1000)
    # if app.timePassed % app.mslPerSec == 0:
    if app.timePassed % 1000 == 0: # test conditional
        addEnemyMissile(app)
    # need to set general variable for shootEnemyMissile
    if app.timePassed % 10 == 0:
        shootEnemyMissile(app)
        shootUserMissile(app)

def drawHealthBar(app, canvas, health, divider):
    x0 = 0
    x1 = 1/10 * app.width
    y0 = 0
    y1 = 1/50 * app.height
    # draw rectangle to fill in colors when health bars disappear
    canvas.create_rectangle(x0, y0, app.width, y1, fill = 'dark gray')
    for bar in range(health//divider):
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'red', 
                                    outline = 'red', width = 3)
        x0, x1 = x1, (x1 + 1/10*app.width)
    x0 = 0
    x1 = app.width
    y0 = 1/50 * app.height
    y1 = 1/50 * app.height
    canvas.create_line(x0, y0, x1, y1, fill = 'tan')
    # draw heart icon
    cx = app.width-100
    cy = 160
    canvas.create_rectangle(cx-15, cy-135, cx+15, 
                            cy-105, fill = 'snow')
    canvas.create_rectangle(cx-13, cy-125, cx+13, 
                            cy-115, fill = 'red', outline = 'red')
    canvas.create_rectangle(cx-5, cy-132, cx+5, 
                            cy-108, fill = 'red', outline = 'red')
    # draw health number 
    canvas.create_text(app.width-45, 42, text = f'{app.userJet.health}/{app.userJetFull}',
                        fill = 'red', font = 'Courier 16 bold')

def drawPauseButton(app, canvas):
    canvas.create_image
    canvas.create_rectangle(25, 25, 50, 50, fill = 'navy blue', outline = 'royal blue',
                            width = 3)
    canvas.create_text(40, 60, text = 'Pause/Resume', font = 'Courier 10 bold',
                        fill = 'white')
    
def drawPause(app, canvas):
    cx = app.width//2
    cy = app.height//2
    canvas.create_rectangle(cx - 210, cy - 100, cx + 210, cy + 110, fill = 'black')
    canvas.create_text(app.width//2, app.height//2-20, text = 'Game paused', 
                        font = 'Courier 30 bold', fill = 'red')
    # resume game button
    canvas.create_rectangle(app.width//2-140, app.height//2+20, app.width//2-30, 
                            app.height//2+60, fill = 'red', outline = 'black')
    canvas.create_text(app.width//2-85, app.height//2+40, text = 'Resume', 
                        fill = 'black', font = 'Courier 15 bold')
    # restart game button
    canvas.create_rectangle(app.width//2+140, app.height//2+20, app.width//2+30, 
                            app.height//2+60, fill = 'red', outline = 'black')
    canvas.create_text(app.width//2+85, app.height//2+40, text = 'Return Home', 
                        fill = 'black', font = 'Courier 15 bold')

def drawScore(app, canvas):
    canvas.create_text(app.width//2, 40, text = f"Targets Down: {app.score}", 
                        fill = 'green', font = 'Courier 30 bold')

def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    

def drawMissileCounter(app, canvas):
    canvas.create_text(app.width//2, 68, text = f'Missiles On Course: {app.MissilesInAir}', 
                        fill = "green", font = 'Courier 20')
    canvas.create_text(app.width//2, 90, text = f'Enemy Fire Rate: 1 msls/{app.mslPerSec/1000}sec', fill = 'green',
                        font = 'Courier 15')

def drawUserJet(app, canvas, x0, y0, colors, name):
    # upper half of body
    canvas.create_arc(x0 - 15, y0+70, x0 + 15, y0-110, 
                        fill = colors[0], outline = 'black', extent = 180)
     # lower half of body
    canvas.create_arc(x0 - 15, y0-90, x0 + 15, y0+60, 
                        fill = colors[1], outline = 'black', extent = -180)
    canvas.create_rectangle(x0+15, y0-20, x0-15, y0-13, fill = 'black', 
                            outline = 'black')
    # pilot's head-up-display (HUD)
    canvas.create_oval(x0 - 7, y0-5, x0 + 7, y0-100, fill = colors[2],
                        outline = colors[3])
     # right front wing
    wingY = (y0-10+y0-30)//2     
    canvas.create_polygon(x0 + 15, wingY, x0 + 50, wingY, x0 + 80, wingY + 20, 
                        x0 + 10, wingY + 20, outline = 'black', 
                        fill = colors[4])
    # right tail
    canvas.create_polygon(x0 + 10, wingY + 40, x0 + 30, wingY + 40, x0 + 50, 
                        wingY + 55, x0 + 5, wingY + 55, outline = 'black', 
                        fill = colors[5])
    # left front wing
    canvas.create_polygon(x0 - 15, wingY, x0 - 50, wingY, x0 - 80, wingY + 20, 
                        x0 - 10, wingY + 20, outline = 'black', 
                        fill = colors[6])
    # left tail
    canvas.create_polygon(x0 - 10, wingY + 40, x0 - 30, wingY + 40, x0 - 50, 
                        wingY + 55, x0 - 5, wingY + 55, outline = 'black', 
                        fill = colors[7])
    # right missile shooter
    mslCx = x0 + 7.5
    canvas.create_rectangle(mslCx + 30, wingY - 10, mslCx + 20, wingY, 
                            fill = colors[8], outline = 'black')
    
    # left missile shooter
    mslCx1 = x0 - 7.5
    canvas.create_rectangle(mslCx1 - 30, wingY - 10, mslCx1 - 20, wingY, 
                            fill = colors[9], outline = 'black')

    # name tag
    canvas.create_text(x0, y0+80, text = name, fill = 'white',
                        font = 'Courier 25 bold')
                            
def drawEnemyJet(app, canvas, x0, y0, unit):
    # draw jet's body
    # x and y-coord in app.enemyJets are the center coordinates of enemy jets

    canvas.create_rectangle(x0-10*unit, y0-10*unit, x0+10*unit, y0+40*unit, outline = 'black',
                            fill = 'silver')

    # draw jet's missile shooter

    canvas.create_arc(x0-8*unit, y0+35*unit, x0+8*unit, y0+50*unit, outline = 'black', 
                            fill = 'medium violet red', extent = -180)
    
    #draw right wing 
    
    canvas.create_polygon(x0-10*unit, y0, x0-50*unit, y0, x0-30*unit, 
                        y0+20*unit, x0-10*unit, y0+20*unit, 
                        fill = 'SlateGray2', outline = 'black')
    # draw right tail

    #draw left wing
    canvas.create_polygon(x0+10*unit, y0, x0+50*unit, y0, x0+30*unit, 
                            y0+20*unit, x0+10*unit, y0+20*unit, 
                            fill = 'SlateGray2', outline = 'black')
    #draw left tail 

# shield   
# spawn health kits
# make screen flash
# create background 
# collision animations
# enderman

def getSquadronSize(app):
    # get random squadron size 1 - 3 
    squadronSize = random.randint(1,3)
    newSquadron = nmyJetC.Squadron()
    return squadronSize, newSquadron 
    # use return values for parameters in createEnemyJetVariation 
    # (squadron object and size)

def createEnemyJetVariation(app, size, squadron, cx, cy):
    if app.pause:
        return
    # if squadron is complete add to enemyJet list
    if len(squadron.team) == size:
        app.enemyJets.append(squadron.team)
    # or else pick random enemy jet type and add to squadron list
    else:
        jetType = random.choice(app.enemyJetChoice)
        if jetType == 'bomber':
            enemyJet = nmyJetC.Bomber(50, 10, cx, cy)
        elif jetType == 'light':
            enemyJet = nmyJetC.LightFighter(20, 10, cx, cy)
        elif jetType == 'torpedo':
            enemyJet = nmyJetC.Torpedo(30, 15, cx, cy)
        squadron.addJet(enemyJet)
        app.enemyJetXCoord.add(cx)
        if len(squadron.team) % 2 != 0:
            return createEnemyJetVariation(app, size, squadron, cx+100, cy)
        elif len(squadron.team) % 2 == 0:
            return createEnemyJetVariation(app, size, squadron, cx-50, cy-20)


# spawns enemy jets at the top of the screen
def spawnEnemyJet(app):
    enemySpawnX0 = random.randint(50, app.width-100)
    # debug:
    # print('original:', enemySpawnX0)
    bound1 = enemySpawnX0 - 100
    bound2 = enemySpawnX0 + 100
   
    if isNotOverlap(app, bound1, bound2):
        return enemySpawnX0

def validCoord(app):
    x_Coord = spawnEnemyJet(app)
    while x_Coord == None:
        x_Coord = spawnEnemyJet(app)
    return x_Coord
      

# makes sure enemy jets don't overlap when spawning into the window
def isNotOverlap(app, bound1, bound2):
    include = set(range(bound1, bound2+1))
    for num in include:
        if num in app.enemyJetXCoord:
            return False
    return True
 
# moves enemy jet down the window
def moveEnemyJet(app):
    if app.pause:
        return
    else:
        # x-coordinate --> jet.EnemyX
        # y-coordinate --> jet.EnemyY
        for squadron in app.enemyJets:
            for jet in squadron:
                jet.EnemyY += 1
                if hitBoxEnemy(app, jet):
                    if jet.health <= 0:
                        squadron.remove(jet)
                        app.score += 1
                        app.enemyJetXCoord.remove(jet.EnemyX)
                        if len(squadron) == 0:
                            app.enemyJets.remove(squadron)
                    if app.score % 5 == 0:
                        app.mslPerSec -= 25
                        if app.mslPerSec <= 0:
                            app.mslPerSec = 25
                # user gains 5 health when killing enemy jet
                # if app.userJet.health <= app.userJetFull:
                #     app.userJet.health += 2
                #     if app.userJet.health > app.userJetFull:
                #         app.userJet.health = app.userJetFull
                if jet.EnemyY >= app.height:
                    squadron.remove(jet)
                    app.enemyJetXCoord.remove(jet.EnemyX)
                    if len(squadron) == 0:
                        app.enemyJets.remove(squadron)
                    app.userJet.health -= 10


# chooses random missile type and adds it to enemy jet
def addEnemyMissile(app):
    for squadron in app.enemyJets:
        for jet in squadron:
            # lightfighters can only shoot linear bullets
            if isinstance(jet, nmyJetC.LightFighter):
                missile = mslC.Linear(jet.EnemyX, jet.EnemyY)
            # torpedo fighters can only shoot sinusoidal bullets
            elif isinstance(jet, nmyJetC.Torpedo):
                missile = mslC.Sinusoidal(jet.EnemyX, jet.EnemyY)
            # bomber fighters have a random selection of parabolic bullets
            else:
                missileType = random.choice(app.enemyMissileTypes)
                if missileType == 'para1':
                    missile = mslC.Parabolic(jet.EnemyX, jet.EnemyY)
                elif missileType == 'para2':
                    missile = mslC.Parabolic2(jet.EnemyX, jet.EnemyY)
                elif missileType == 'cubic':
                    missile  = mslC.Cubic(jet.EnemyX, jet.EnemyY)
            app.enemyMissiles.append(missile)

# shoots enemy missile from enemy missile list 
def shootEnemyMissile(app):
    for missile in app.enemyMissiles:
        missile.eq()
        if hitboxUserEnemyMissiles(app, app.userMissiles, missile):
            app.enemyMissiles.remove(missile)
            app.userMissiles.remove(app.userMissiles[0])
            app.MissilesInAir -= 2
        elif hitBoxUser(app):
            app.userJet.health -= missile.damage
        elif missile.y >= app.height:
            app.enemyMissiles.remove(missile)
        

def getUserMissileCoord(app):
    if app.specialActivated:
        special = mslC.Special(app.userJet.UserX, app.userJet.UserY, app.userJet.speed)
        app.userMissiles.append(special)
    else:
        linear = mslC.ULinear(app.userJet.UserX, app.userJet.UserY, app.userJet.speed)
        app.userMissiles.append(linear)
    # each actual missile x-coordinate in userMissile is +- 7.5 units from
    # the x-coordinate in the userMissiles list
    app.MissilesInAir += 2


# shoots missile when user presses 'space'
def shootUserMissile(app):
    for missile in app.userMissiles:
        missile.eq()
        if missile.y <= -700:
            app.userMissiles.remove(missile)
            app.MissilesInAir -= 2

# hitbox when enemy missiles hit user's jet
def hitBoxUser(app):
    for missile in app.enemyMissiles:
        x = missile.x
        y = missile.y
        possibleX = [x-8, x+8, x]
        for x in possibleX:
            if app.userJet.UserX-80 <= x <= app.userJet.UserX+80:
                if y >= app.userJet.UserY-40 and y <= app.userJet.UserY+60:
                    app.enemyMissiles.remove(missile)
                    return True
    
    return False

# hitbox when user missiles hit enemy's jet
def hitBoxEnemy(app, enemyJet):
    for missile in app.userMissiles:
        x = missile.x
        y = missile.y
        wingY = (y-10+app.height-30)//2
        possibleX = [x-27.5, x+27.5, x-37.5, x+37.5]
        for x in possibleX:
            if enemyJet.EnemyX-50 <= x <= enemyJet.EnemyX+50:
                if enemyJet.EnemyY<= wingY <= enemyJet.EnemyY+50:
                    app.userMissiles.remove(missile)
                    app.MissilesInAir -= 2
                    enemyJet.health -= missile.damage
                    return True
    
    return False

# if user missile hits enemy missile, both missiles cancel out
def hitboxUserEnemyMissiles(app, userMissiles, enemyMissile):
    # compare user missile list with enemy missile list 
    if len(userMissiles) == 0:
        return False
    else:
        x = userMissiles[0].x
        y = userMissiles[0].y
        wingY = (userMissiles[0].y-10+app.height-30)//2
        possibleX = [enemyMissile.x-10, enemyMissile.x+10]
        for x1 in possibleX:
            if x-37.5 <= x1 <= x+37.5:
                if wingY-12 <= enemyMissile.y <= wingY:
                    return True
        return hitboxUserEnemyMissiles(app, userMissiles[1:], enemyMissile)


def gameMode_redrawAll(app, canvas):
    # draw background first
    drawBackground(app, canvas)
    # draw user's jet
    app.userJet.redraw(app, canvas)
    # draw missiles shot by user
    for missile in app.userMissiles:
        missile.redraw(app, canvas)
    # draw enemy jets 
    for squadron in app.enemyJets:
        for jet in squadron:
            jet.redraw(app, canvas)
    # draw enemy missiles
    for missile in app.enemyMissiles:
        missile.redraw(app, canvas)
    # extra features/gameplay information
    # draw health bar
    drawHealthBar(app, canvas, app.userJet.health, app.userJetFull//10)
    # draw box to enclosed missile counter and score
    cx = app.width//2
    cy = 50
    canvas.create_rectangle(cx -210, cy-30, cx + 210, cy + 60, fill = 'black')
    # draw missiles in the air 
    drawMissileCounter(app, canvas)
    # draw score (enemy jets taken down)
    drawScore(app, canvas)
    
    # game over animation (condition 1)
    if app.MissilesInAir > 30:
        cx = app.width//2
        cy = app.height//2
        canvas.create_rectangle(cx - 310, cy - 50, cx + 310, cy + 60, fill = 'black')
        canvas.create_text(app.width//2, app.height//2, 
                            text = 'System Failure: Overheat'.upper(), fill = 'red',
                            font = 'Courier 40 bold')
        canvas.create_text(app.width//2, app.height//2+30, text = "[Missile Limit: 30] (EXCEEDED)", fill = 'red',
                            font = 'Courier 20 bold')
    elif app.MissilesInAir >= 20:
        canvas.create_text(app.width//2, app.height//2, 
                            text = 'Overheating: Missiles Fired Exceeding Limit', fill = 'orange',
                            font = 'Courier 40 bold')
    # game over animation (condition 2)
    elif app.userJet.health <= 0:
        cx = app.width // 2
        cy = app.height//2
        canvas.create_rectangle(cx-200, cy-100, cx+200, cy+100, fill = 'black')
        canvas.create_text(app.width//2, app.height//2-20, text = 'FIGHTER DOWN', 
                            fill = 'red', font = 'Courier 40 bold')
        canvas.create_text(app.width//2, app.height//2+50, 
                            text = 'Press "r" to restart', fill = 'red', 
                            font = 'Courier 30 bold')
    elif app.userJet.health <= 20:
        if app.timePassed % 50 == 0:
            canvas.create_text(1150, 100, text = "WARNING", fill= 'red',
                                font = 'Courier 90 bold')
    
    # draw pause button/pause animation
    drawPauseButton(app, canvas)
    if app.pause:
        drawPause(app, canvas)
    if app.gameOver:
        canvas.create_text(app.width//2, 10, text = "Game Over", fill = 'black', 
                            font = 'Courier 15 bold')

    # draw icon for enemy jet capacity
    drawEnemyJet(app, canvas, app.width - 95, 73, 0.5)
    # show enemy jet capacity
    canvas.create_text(app.width-50, 80, text = f"{app.enemyJetCapacity+1}", fill= 'red',
                                font = 'Courier 30 bold')


    
# change width to 1440 (final)
runApp(width = 1440, height = 778)


