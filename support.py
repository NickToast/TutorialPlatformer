import pygame
from os import walk
#go through file system
#always use walk inside of a for loop because it returns 3 different things
#directory path, directory name, and file names inside of folder you specified

def import_folder(path):
    surface_list = []
    for _,__, img_files in walk(path):
        #import the images and put them into a surface
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
        #then put the surfaces into a list
        #return the list of surfaces
    return surface_list

#ENSURE THAT YOU ONLY HAVE IMAGE FILES INSIDE EACH FOLDER
#meaning only, png or jpeg files
#pygame will try to still import and place it on the surface, but will get an error