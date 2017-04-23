### Ludam Dare 38 - 20170421 ###################################################
import pygame
import time
import sys

### init #######################################################################
# start pygame
pygame.init()

# our window sizes (800x600)
displayWidth = 800
displayHeight = 600

# our alpha key
alphaColor = (224, 111, 139, 0)

# make our display and set the caption (Ludum Dare!!)
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Ludum Dare 38')

# let's define some simple colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
grey = (119, 136, 153)

# define our hero properties minus padding
heroWidth = 32
heroHeight = 32

# setup a clock and our exit conditions
clock = pygame.time.Clock()
crashed = False

### classes ####################################################################
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # constructor function

        # call the parent constructor
        super().__init__()

        # set our size and load our image
        width = 32
        height = 32
        self.dead = False # have we hit a spike or the floor?
        self.goal = False # have we hit the door?
        self.image = pygame.image.load('assets/hero.png').convert()
        self.image.set_colorkey(alphaColor)

        # get our collision rect
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        # set our speed vectors
        self.changeX = 0
        self.changeY = 0

        # list of sprites for collision detection
        self.level = None

    def update(self):
        # move the Player
        self.CalculateGravity()
        # move left and right
        self.rect.x += self.changeX
        self.rect.y += self.changeY

        # check if we hit any platforms in the Level
        blockHitList = pygame.sprite.spritecollide(self, self.level.platformList, False)
        for block in blockHitList:
            # reset position
            if self.changeY > 0:
                self.rect.bottom = block.rect.top
            if self.changeY < 0:
                self.rect.top = block.rect.bottom

            # stop vertical movement
            self.changeY = 0

        # check if we hit a spike
        spikeHitList = pygame.sprite.spritecollide(self, self.level.enemyList, False)
        for spike in spikeHitList:
            # set player state to dead
            self.dead = True

        # check if we hit a boost platform
        boostHitList = pygame.sprite.spritecollide(self, self.level.boostList, False)
        for boost in boostHitList:
            # player gets a lot of vertical momentum
            self.changeY = -15

        # check if we hit the door
        doorHitList = pygame.sprite.spritecollide(self, self.level.doorList, False)
        for door in doorHitList:
            # we need to somehow advance the level from here
            self.goal = True
            self.xPos = 40
            self.yPos = 40
            self.xChange = 0
            self.yChange = 0

    def CalculateGravity(self):
        if self.changeY == 0:
            self.changeY = 1
        else:
            self.changeY += .35

        if self.rect.y >= displayHeight - self.rect.height and self.changeY >= 0:
            self.changeY = 0
            self.rect.y = displayHeight - self.rect.height
            self.dead = True

    def jump(self):
        # user hit the jump button
        self.rect.y += 2
        platformHitList = pygame.sprite.spritecollide(self, self.level.platformList, False)
        self.rect.y -= 2

        if len(platformHitList) > 0 or self.rect.bottom >= displayHeight:
            self.changeY = - 10

    def goLeft(self):
        self.changeX = -6
    def goRight(self):
        self.changeX = 6
    def stop(self):
        self.changeX = 0

class Level(object):
    def __init__(self, player):
        self.platformList = pygame.sprite.Group()
        self.enemyList = pygame.sprite.Group()
        self.doorList = pygame.sprite.Group()
        self.boostList = pygame.sprite.Group()
        self.player = player

        # background
        self.background = grey

    def update(self):
        self.platformList.update()
        self.enemyList.update()
        self.doorList.update()
        self.boostList.update()

    def draw(self, screen):
        screen.fill(self.background)

        self.platformList.draw(screen)
        self.enemyList.draw(screen)
        self.doorList.draw(screen)
        self.boostList.draw(screen)

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.image.load('assets/platform.png').convert()
        self.image.set_colorkey(alphaColor)

        self.rect = self.image.get_rect()

class Spike(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.image.load('assets/spike.png').convert()
        self.image.set_colorkey(alphaColor)

        self.rect = self.image.get_rect()

class Door(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.image.load('assets/door.png').convert()
        self.image.set_colorkey(alphaColor)

        self.rect = self.image.get_rect()

class Boost(pygame.sprite.Sprite):
    def __init__(self, width, height_):
        super().__init__()

        self.image = pygame.image.load('assets/boost.png').convert()
        self.image.set_colorkey(alphaColor)

        self.rect = self.image.get_rect()

class Level01(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        level = [[32, 32, 0, 568], [32, 32, 32, 568], [32, 32, 64, 568],
                 [32, 32, 96, 568], [32, 32, 126, 568], [32, 32, 158, 568],
                 [32, 32, 190, 568], [32, 32, 222, 568], [32, 32, 300, 450],
                 [32, 32, 332, 450], [32, 32, 364, 450], [32, 32, 396, 450]]

        # boost = [[32, 32, 550, 500]]

        exit = [[32, 32, 364, 418]]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platformList.add(block)

        for door in exit:
            block = Door(door[0], door[1])
            block.rect.x = door[2]
            block.rect.y = door[3]
            block.player = self.player
            self.doorList.add(block)


class Level02(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        player.xChange = 0
        level = [[32, 32, 0, 568], [32, 32, 32, 568], [32, 32, 64, 568],
                 [32, 32, 96, 568], [32, 32, 126, 568], [32, 32, 158, 568],
                 [32, 32, 190, 568], [32, 32, 222, 568], [32, 32, 300, 350],
                 [32, 32, 332, 350], [32, 32, 364, 350], [32, 32, 396, 350]]

        boost = [[32, 32, 170, 500]]
        exit = [[32, 32, 364, 318]]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platformList.add(block)

        for high in boost:
            block = Boost(high[0], high[1])
            block.rect.x = high[2]
            block.rect.y = high[3]
            block.player = self.player
            self.boostList.add(block)

        for door in exit:
            block = Door(door[0], door[1])
            block.rect.x = door[2]
            block.rect.y = door[3]
            block.player = self.player
            self.doorList.add(block)

class Level03(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        player.xChange = 0

        with open("assets/level3.dat") as file:
            levelFile = [line.rstrip("\n").split(", ") for line in file]

        rows = 19
        cols = 25
        level = []
        spikes = []
        exit = []
        boost = []

        for i in range(0, rows):
            for j in range(0, cols):
                if (levelFile[i][j]) == '1':
                    level.append([32, 32, 32*j, 32*i])
                elif (levelFile[i][j]) == '2':
                    spikes.append([32, 32, 32*j, 32*i])
                elif (levelFile[i][j]) == '3':
                    boost.append([32, 32, 32*j, 32*i])
                elif (levelFile[i][j]) == '4':
                    exit.append([32, 32, 32*j, 32*i])

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platformList.add(block)

        for danger in spikes:
            block = Spike(danger[0], danger[1])
            block.rect.x = danger[2]
            block.rect.y = danger[3]
            block.player = self.player
            self.enemyList.add(block)

        for door in exit:
            block = Door(door[0], door[1])
            block.rect.x = door[2]
            block.rect.y = door[3]
            block.player = self.player
            self.doorList.add(block)

        for high in boost:
            block = Boost(high[0], high[1])
            block.rect.x = high[2]
            block.rect.y = high[3]
            block.player = self.player
            self.boostList.add(block)

class Level04(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        player.xChange = 0

        with open("assets/level4.dat") as file:
            levelFile = [line.rstrip("\n").split(", ") for line in file]

        rows = 19
        cols = 25
        level = []
        spikes = []
        exit = []
        boost = []

        for i in range(0, rows):
            for j in range(0, cols):
                if (levelFile[i][j]) == '1':
                    level.append([32, 32, 32*j, 32*i])
                elif (levelFile[i][j]) == '2':
                    spikes.append([32, 32, 32*j, 32*i])
                elif (levelFile[i][j]) == '3':
                    boost.append([32, 32, 32*j, 32*i])
                elif (levelFile[i][j]) == '4':
                    exit.append([32, 32, 32*j, 32*i])

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platformList.add(block)

        for danger in spikes:
            block = Spike(danger[0], danger[1])
            block.rect.x = danger[2]
            block.rect.y = danger[3]
            block.player = self.player
            self.enemyList.add(block)

        for door in exit:
            block = Door(door[0], door[1])
            block.rect.x = door[2]
            block.rect.y = door[3]
            block.player = self.player
            self.doorList.add(block)

        for high in boost:
            block = Boost(high[0], high[1])
            block.rect.x = high[2]
            block.rect.y = high[3]
            block.player = self.player
            self.boostList.add(block)

class Level05(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        player.xChange = 0

        with open("assets/level5.dat") as file:
            levelFile = [line.rstrip("\n").split(", ") for line in file]

        rows = 19
        cols = 25
        level = []
        spikes = []
        exit = []
        boost = []

        for i in range(0, rows):
            for j in range(0, cols):
                if (levelFile[i][j]) == '1':
                    level.append([32, 32, 32*j, 32*i])
                elif (levelFile[i][j]) == '2':
                    spikes.append([32, 32, 32*j, 32*i])
                elif (levelFile[i][j]) == '3':
                    boost.append([32, 32, 32*j, 32*i])
                elif (levelFile[i][j]) == '4':
                    exit.append([32, 32, 32*j, 32*i])

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platformList.add(block)

        for danger in spikes:
            block = Spike(danger[0], danger[1])
            block.rect.x = danger[2]
            block.rect.y = danger[3]
            block.player = self.player
            self.enemyList.add(block)

        for door in exit:
            block = Door(door[0], door[1])
            block.rect.x = door[2]
            block.rect.y = door[3]
            block.player = self.player
            self.doorList.add(block)

        for high in boost:
            block = Boost(high[0], high[1])
            block.rect.x = high[2]
            block.rect.y = high[3]
            block.player = self.player
            self.boostList.add(block)

class Level06(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        player.xChange = 0

        with open("assets/level6.dat") as file:
            levelFile = [line.rstrip("\n").split(", ") for line in file]

        rows = 19
        cols = 25
        level = []
        spikes = []
        exit = []
        boost = []

        for i in range(0, rows):
            for j in range(0, cols):
                if (levelFile[i][j]) == '1':
                    level.append([32, 32, 32*j, 32*i])
                elif (levelFile[i][j]) == '2':
                    spikes.append([32, 32, 32*j, 32*i])
                elif (levelFile[i][j]) == '3':
                    boost.append([32, 32, 32*j, 32*i])
                elif (levelFile[i][j]) == '4':
                    exit.append([32, 32, 32*j, 32*i])

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platformList.add(block)

        for danger in spikes:
            block = Spike(danger[0], danger[1])
            block.rect.x = danger[2]
            block.rect.y = danger[3]
            block.player = self.player
            self.enemyList.add(block)

        for door in exit:
            block = Door(door[0], door[1])
            block.rect.x = door[2]
            block.rect.y = door[3]
            block.player = self.player
            self.doorList.add(block)

        for high in boost:
            block = Boost(high[0], high[1])
            block.rect.x = high[2]
            block.rect.y = high[3]
            block.player = self.player
            self.boostList.add(block)

class Level07(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        player.xChange = 0

        with open("assets/level7.dat") as file:
            levelFile = [line.rstrip("\n").split(", ") for line in file]

        rows = 19
        cols = 25
        level = []
        spikes = []
        exit = []
        boost = []

        for i in range(0, rows):
            for j in range(0, cols):
                if (levelFile[i][j]) == '1':
                    level.append([32, 32, 32*j, 32*i])
                elif (levelFile[i][j]) == '2':
                    spikes.append([32, 32, 32*j, 32*i])
                elif (levelFile[i][j]) == '3':
                    boost.append([32, 32, 32*j, 32*i])
                elif (levelFile[i][j]) == '4':
                    exit.append([32, 32, 32*j, 32*i])

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platformList.add(block)

        for danger in spikes:
            block = Spike(danger[0], danger[1])
            block.rect.x = danger[2]
            block.rect.y = danger[3]
            block.player = self.player
            self.enemyList.add(block)

        for door in exit:
            block = Door(door[0], door[1])
            block.rect.x = door[2]
            block.rect.y = door[3]
            block.player = self.player
            self.doorList.add(block)

        for high in boost:
            block = Boost(high[0], high[1])
            block.rect.x = high[2]
            block.rect.y = high[3]
            block.player = self.player
            self.boostList.add(block)

class Level08(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        player.xChange = 0

        with open("assets/level8.dat") as file:
            levelFile = [line.rstrip("\n").split(", ") for line in file]

        rows = 19
        cols = 25
        level = []
        spikes = []
        exit = []
        boost = []

        for i in range(0, rows):
            for j in range(0, cols):
                if (levelFile[i][j]) == '1':
                    level.append([32, 32, 32*j, 32*i])
                elif (levelFile[i][j]) == '2':
                    spikes.append([32, 32, 32*j, 32*i])
                elif (levelFile[i][j]) == '3':
                    boost.append([32, 32, 32*j, 32*i])
                elif (levelFile[i][j]) == '4':
                    exit.append([32, 32, 32*j, 32*i])

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platformList.add(block)

        for danger in spikes:
            block = Spike(danger[0], danger[1])
            block.rect.x = danger[2]
            block.rect.y = danger[3]
            block.player = self.player
            self.enemyList.add(block)

        for door in exit:
            block = Door(door[0], door[1])
            block.rect.x = door[2]
            block.rect.y = door[3]
            block.player = self.player
            self.doorList.add(block)

        for high in boost:
            block = Boost(high[0], high[1])
            block.rect.x = high[2]
            block.rect.y = high[3]
            block.player = self.player
            self.boostList.add(block)

class Game(object):
    def __init__(self, screen, states, startState):
        self.done = False
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.states = states
        self.stateName = startState
        self.state = self.states[self.stateName]

    def eventLoop(self):
        for event in pygame.event.get():
            self.state.getEvent(event)

    def flipState(self):
        currentState = self.stateName
        nextState = self.state.nextState
        self.state.done = False
        self.stateName = nextState
        persistent = self.state.persist
        self.state = self.states[self.stateName]
        self.state.startup(persistent)

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flipState()
        self.state.update(dt)

    def draw(self):
        self.state.draw(self.screen)

    def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.eventLoop()
            self.update(dt)
            self.draw()
            pygame.display.update()

class GameState(object):
    def __init__(self):
        self.done = False
        self.quit = False
        self.nextState = None
        self.screenRect = pygame.display.get_surface().get_rect()
        self.persist = {}
        self.font = pygame.font.Font("assets/ARCADEPI.ttf", 24)

    def startup(self, persistent):
        self.persist = persistent

    def getEvent(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass

class SplashScreen(GameState):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.splashList = ["MINI PLATFORMS", "Made by Dev",
                           "Press ENTER to play!"]
        self.nextState = "GAMEPLAY"

    def getEvent(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.done = True

    def draw(self, surface):
        surface.fill(grey)
        for i, line in enumerate(self.splashList):
            self.title = self.font.render(line, 1, pygame.Color("black"))
            self.titleRect = self.title.get_rect(center = self.screenRect.center,
                                                 y = 200 + (i * 45))
            surface.blit(self.title, self.titleRect)

class CreditScreen(GameState):
    def __init__(self):
        super(CreditScreen, self).__init__()
        self.creditList = ["-=CREDITS=-", "MINI PLATFORMS", "Made by Dev",
                           "Music - Global Resonance by Knight of Fire",
                           "-=SPECIAL THANKS=-",
                           "All of the great pyGame Tutorials out there",
                           "Official pyGame Documentation",
                           "-=IN MEMORIUM=-",
                           "4HORSEMEN STUDIOS"]
        self.texts = []

        self.persist["screenColor"] = "black"
        self.nextState = "GAMEPLAY"


    def getEvent(self, event):
        if event.type == pygame.QUIT:
            self.quit = True


    def draw(self, surface):
        surface.fill(grey)
        for i, line in enumerate(self.creditList):
            self.title = self.font.render(line, 1, pygame.Color("black"))
            self.titleRect = self.title.get_rect(center = self.screenRect.center,
                                                 y = 100 + (i * 45))
            surface.blit(self.title, self.titleRect)

def GameOver(surface, player):
    print("We are in game over")
    player.rect.x = 0
    player.rect.y = 0
    player.xChange = 0
    player.yChange = 0
    player.stop()

    screenRect = pygame.display.get_surface().get_rect()
    font = pygame.font.Font("assets/ARCADEPI.ttf", 24)
    finished = False
    surface.fill(grey)
    title = font.render("GAME OVER", 1, pygame.Color("black"))
    titleRect = title.get_rect(center = screenRect.center,
                                             y = 250 )
    surface.blit(title, titleRect)
    title = font.render("PRESS ESCAPE TO CONTINUE", 1, pygame.Color("black"))
    titleRect = title.get_rect(center = screenRect.center,
                                             y = 300 )

    surface.blit(title, titleRect)
    pygame.display.update()
    while finished == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    finished = True

def Goal(surface, player):

    print("We are in goal")
    player.rect.x = 0
    player.rect.y = 0
    player.stop()
    player.xChange = 0
    player.yChange = 0

    screenRect = pygame.display.get_surface().get_rect()
    font = pygame.font.Font("assets/ARCADEPI.ttf", 24)
    finished = False
    surface.fill(grey)
    title = font.render("CONGRATULATIONS", 1, pygame.Color("black"))
    titleRect = title.get_rect(center = screenRect.center,
                                             y = 250 )
    surface.blit(title, titleRect)
    title = font.render("PRESS SPACE TO CONTINUE", 1, pygame.Color("black"))
    titleRect = title.get_rect(center = screenRect.center,
                                             y = 300 )
    surface.blit(title, titleRect)
    pygame.display.update()

    while finished == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    finished = True

def printLevelNumber(surface, levelnumber):
    screenRect = pygame.display.get_surface().get_rect()
    font = pygame.font.Font("assets/ARCADEPI.ttf", 24)
    title = font.render(f"Level {levelnumber}", 1, pygame.Color("black"))
    titleRect = title.get_rect(x = 15, y = 50 )
    surface.blit(title, titleRect)

def GameBeat(surface):

    # the player has beaten the game

    # reset player's position


    screenRect = pygame.display.get_surface().get_rect()
    font = pygame.font.Font("assets/ARCADEPI.ttf", 24)
    finished = False
    surface.fill(grey)
    title = font.render("CONGRATULATIONS, YOU ARE A PLATFORM MASTER!", 1, pygame.Color("black"))
    titleRect = title.get_rect(center = screenRect.center, y = 250 )
    surface.blit(title, titleRect)
    title = font.render("PRESS ENTER TO CONTINUE", 1, pygame.Color("black"))
    titleRect = title.get_rect(center = screenRect.center, y = 300 )

    surface.blit(title, titleRect)
    pygame.display.update()

    while finished == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    finished = True


class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.nextState = "CREDITS"
        self.activeSpriteList = pygame.sprite.Group()
        self.player = Player()
        self.size = [displayWidth, displayHeight]
        self.levelList = []
        self.levelList.append( Level01(self.player) )
        self.levelList.append( Level02(self.player) )
        self.levelList.append( Level03(self.player) )
        self.levelList.append( Level04(self.player) )
        self.levelList.append( Level05(self.player) )
        self.levelList.append( Level06(self.player) )
        self.levelList.append( Level07(self.player) )
        self.levelList.append( Level08(self.player) )
        self.currentLevelNumber = 0
        self.levelNumberText = self.currentLevelNumber + 1
        self.currentLevel = self.levelList[self.currentLevelNumber]

    def startup(self, persistent):
        self.persist = persistent

        self.player.level = self.currentLevel

        self.player.rect.x = 0
        self.player.rect.y = 0
        self.activeSpriteList.add(self.player)
        pygame.mixer.music.load('assets/song.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)

    def getEvent(self, event):
        print("We are pulling events.")
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.titleRect.center = event.pos
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.mixer.music.fadeout(1000)
                self.done = True
            elif event.key == pygame.K_LEFT:
                # move hero left
                self.player.goLeft()
            elif event.key == pygame.K_RIGHT:
                # move hero right
                self.player.goRight()
            elif event.key == pygame.K_UP:
                self.player.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and self.player.changeX < 0:
                self.player.stop()
            elif event.key == pygame.K_RIGHT and self.player.changeX > 0:
                self.player.stop()

    def update(self, dt):
        self.activeSpriteList.update()
        self.currentLevel.update()
        if self.player.rect.right > displayWidth:
            self.player.rect.right = displayWidth
        if self.player.rect.left < 0:
            self.player.rect.left = 0
        if self.player.dead == True:
            self.player.dead = False
            #self.currentLevel = self.levelList[0]
            #self.player.level = self.levelList[0]
            #self.currentLevelNumber = 0
            GameOver(gameDisplay, self.player)

        # has the player reached the goal?
        if self.player.goal == True:
            self.player.goal = False
            Goal(gameDisplay, self.player)
            if ((self.currentLevelNumber + 1) <= 7):
                self.currentLevelNumber = self.currentLevelNumber + 1
                self.currentLevel = self.levelList[self.currentLevelNumber]
                self.player.level = self.levelList[self.currentLevelNumber]
            elif ((self.currentLevelNumber + 1) > 7):
                # check if we are past the last level
                GameBeat(gameDisplay)
                self.currentLevelNumber = 1
                self.currentLevel = self.levelList[self.currentLevelNumber]
                self.player.level = self.levelList[self.currentLevelNumber]
                pygame.mixer.music.fadeout(1000)
                self.done = True


    def draw(self, surface):
          self.currentLevel.draw(gameDisplay)
          self.activeSpriteList.draw(gameDisplay)
          printLevelNumber(gameDisplay, self.currentLevelNumber + 1)
          # update the display and clock
          pygame.display.update()
          clock.tick(60)
          print(self.nextState)
### functions ##################################################################

### execution ##################################################################
if __name__ == "__main__":
    states = {"SPLASH": SplashScreen(),
              "GAMEPLAY": Gameplay(),
              "CREDITS": CreditScreen(),
              }

    game = Game(gameDisplay, states, "SPLASH")
    game.run()
    pygame.quit()
    sys.exit()
### eof ########################################################################
