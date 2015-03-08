import pygame

from Util import *
from MapGen import *

import GameData
import GameComponents
from GameState import GameState

import ECS

class Test( ECS.System ):
    def __init__( self, world ):
        super().__init__( world )

    def clean( self ):
        print( 'Cleaning' )

    def process( self ):
        pass


class Game( GameState ):
    def __init__( self, screen, escapeFunc ):
        super().__init__( screen )

        ###########################################################
        # Init the map
        ###########################################################
        GameData.Map = Map( GameData.TileCount[0], GameData.TileCount[1], GameData.MainAtlas, self.screen )
        GameData.Map.makeMap( initializeRandom, preIterInit, postInit )

        self.escapeFunc = escapeFunc
        self.world = ECS.World()
        #self.world.addSystem( Test( self.world ) )

    def runFrame( self ):
        self.handleInput()

        self.world.process()

        self.render()

    def render( self ):
        #Game drawing
        self.screen.fill( ( 255, 255, 255 ) )

        #Render map
        GameData.Map.render( self.camX * GameData.TileSize[0], self.camY * GameData.TileSize[1] )

        #Render entities
        for ent in self.world.getEntityByComponent( ECS.Components.Position, ECS.Components.Renderer ):
            pos = ent.getComponent( ECS.Components.Position )
            pos = ( ( pos.x - self.camX ) * GameData.TileSize[0], ( pos.y - self.camY ) * GameData.TileSize[1] )
            ent.getComponent( ECS.Components.Renderer ).render( self.screen, pos )

        #Render cursor
        GameData.MainAtlas.render( 'cursor', self.screen,
                ( self.mouseTilePos[0] - self.camX ) * GameData.TileSize[0],
                ( self.mouseTilePos[1] - self.camY ) * GameData.TileSize[1] )

        pygame.display.flip()
        self.clock.tick(60)


    def handleInput( self ):
        #Calculate camera position
        self.camX = min( max( GameData.CenterPos[0] - int( self.screenTiles[0] / 2 ), 0 ), GameData.TileCount[0] - self.screenTiles[0] )
        self.camY = min( max( GameData.CenterPos[1] - int( self.screenTiles[1] / 2 ), 0 ), GameData.TileCount[1] - self.screenTiles[1] )

        #Calculate mouse tile
        self.mousePos = pygame.mouse.get_pos()
        self.mouseTilePos = (
                int( ( self.camX * GameData.TileSize[0] + self.mousePos[0] ) / GameData.TileSize[0] ),
                int( ( self.camY * GameData.TileSize[1] + self.mousePos[1] ) / GameData.TileSize[1] ) )

        #Game logic
        for event in pygame.event.get():
            if self.handle( event ):
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                explosive = ECS.Entity()
                explosive.addComponent( ECS.Components.Position( *self.mouseTilePos ) )
                explosive.addComponent( GameComponents.Explosive( 50 ) )
                explosive.addComponent( ECS.Components.Renderer( GameData.Entities, 'tnt' ) )
                self.world.addEntity( explosive )

        curKeys = pygame.key.get_pressed()
        if curKeys[pygame.K_w]:
            GameData.CenterPos[1] -= 1
        if curKeys[pygame.K_s]:
            GameData.CenterPos[1] += 1
        if curKeys[pygame.K_a]:
            GameData.CenterPos[0] -= 1
        if curKeys[pygame.K_d]:
            GameData.CenterPos[0] += 1

    def quit( self, event ):
        if self.escapeFunc( event ):
            self.IsRunning = False
