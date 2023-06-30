import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        #dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface

        #Player Movement
        self.direction = pygame.math.Vector2(0,0) #needs 2 arguments
        #Vectors are just arrows that you can draw on a coordinate system
        #100,50 -> 100 on x axis and 50 y axis and straight arrow from start to end 
        #In pygame, a vector is a list that contains an x and a y value
        #You can add a vector to the position of a rect: rect.center += pygame.math.Vector2(100,50)
        #You can also access the x and y part separately
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -15

        #player status
        self.status = 'idle'
        self.facing_right = True #if false, want player facing left
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assets(self):
        character_path = 'graphics/character/'
        self.animations = {
            'idle': [],
            'run' : [],
            'jump' : [],
            'fall' : []
        }
        #the name of the animation, is the exact same as the folder inside of the character path folder, a folder for each
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('graphics/character/dust_particles/run')

    def animate(self):
        #to play different animations, we need to know what we have to play, our player status
        animation = self.animations[self.status]

        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image #this is a tuple, but we need an integer to target something inside of a list
        else:
            flipped_image = pygame.transform.flip(image, True, False) #3 arguments: surface, want to flip horizontally (booleans), want to flip vertically (booleans)
            self.image = flipped_image

        #set origin of the rectangle
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0
            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]
            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6,10)
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else: 
            self.direction.x = 0
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def get_status(self):
        #what the player is doing
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1: #only plays fall animation if player is falling at a certain speed (gravity)
            self.status = 'fall'
        else:
            #now figure out if player is running or idling
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed


    def update(self):
        self.get_input()
        self.get_status()
        self.run_dust_animation()
        self.animate()
