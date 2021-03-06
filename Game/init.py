import pygame
import sys
import glob

import Cheats

for n in sys.argv:
    if hasattr( Cheats, n ):
        setattr( Cheats, n, True )

###########################################################
# Init pygame
###########################################################
pygame.init()

pygame.display.set_caption( "That's okay. You've got explosives." )
screen = pygame.display.set_mode( ( 1280, 960 ) )

#TODO Render a loading screen to the map?
###########################################################
# Init game data
###########################################################
import GameData

import DataInit
for n in glob.glob( 'data/*.json' ):
    if Cheats.Verbose:
        print( 'Loading file: %s' % n )
    DataInit.Load( n )
DataInit.Finalize()

#This loads the textures referenced in GameData TODO
GameData.Screen = screen
GameData.update()

from Util import LoadFont
LoadFont( 'ButtonFont', 'data/framd.ttf', 10 )
LoadFont( 'NameFont', 'data/framd.ttf', 14 )

import MainMenu
state = MainMenu.MainMenu( GameData.Screen )
state.run()
