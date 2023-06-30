#We create a class called level, and will rely on tiles to place something on the screen
#Then in our main file, we will create one instance of this level and draw it
import pygame
from tiles import Tile
from settings import tile_size, screen_width
from player import Player
from particles import ParticleEffect

class Level:
    def __init__(self, level_data, surface):
        #level set up
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0

        #dust
        self.dust_sprite = pygame.sprite.GroupSingle() #only need one because its jumping or landing, cannot do both same time

    #to get position, we must create the ParticleEffect class inside the level.py file
    #because only in here can we use the world_shift argument
    #thus both landing and jumping particle effects must be inside level
    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10,5)
        else:
            pos += pygame.math.Vector2(10,-5)
        jump_particle_sprite = ParticleEffect(pos, 'jump') #pos will be given from the pos that is passed into the argument
        self.dust_sprite.add(jump_particle_sprite)

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        #this tells us what row we have, and where that row is going to be
        for row_index,row in enumerate(layout): #enumerate gives us the index, and the information
            #for each column
            for col_index,cell in enumerate(row):
                # print(f'{row_index},{col_index}: {cell}')
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == 'X':
                    tile = Tile((x,y), tile_size) #pos, size
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x,y), self.display_surface, self.create_jump_particles)
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < screen_width/4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width/4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else: 
            self.world_shift = 0
            player.speed = 8

    def run(self):
        #dust particles, place behind the tiles, and it looks much better
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        #level tiles
        self.tiles.update(self.world_shift) #later when we have a player, we will change our argument to move to tiles based on player movement
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)


    def horizontal_movement_collision(self):
        player = self.player.sprite
        #applying horizontal movement
        player.rect.x += player.direction.x * player.speed

        #this loops through all of our sprites
        for sprite in self.tiles.sprites():
            #this if statement checks if any of the sprite rects are colliding with the player rect
            if sprite.rect.colliderect(player.rect): #why not spritecollision? we want access of the rects of each tile
                #if our player moving left, then collides with a sprite, we know that it is coming from the 
                #left side, so we place the player on the right of the sprite rect
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right #we can tell the x position of where the collision has occurred and store that into self.current_x
                    
        if player.on_left and (player.rect.left < self.current_x) or player.direction.x >= 0:
            player.on_left = False #if we are touching a wall on the left, we could possibly be just moving right, so we need or statement
        if player.on_right and (player.rect.right > self.current_x) or player.direction.x <= 0:
            player.on_right = False
        
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity() #increasing gravity, never stops doing that unless jump, at some point it will fall right through all the tiles

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                #player on the floor
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                #player on ceiling
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        #checking, once the player is on the ground, and the player is jumping or falling, then the player cannot be on the floor
        #meaning we can put player.on_ground to False
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False