import os
import pygame

def datadir():
    """ Return the data/ directory."""
    fil = os.path.abspath(__file__)
    codedir = os.path.dirname(fil)
    datadir = os.path.join(codedir,'data')+'/'
    return datadir

def play_mp3_pygame(file_path):
    """
    Plays an MP3 file using Pygame.

    Args:
        file_path (str): The path to the MP3 file.
    """
    pygame.mixer.init()  # Initialize the mixer module
    pygame.mixer.music.load(file_path)  # Load the MP3 file
    pygame.mixer.music.play()  # Start playing the music

    # Keep the program running until the music finishes or is explicitly stopped
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10) # Control CPU usage
