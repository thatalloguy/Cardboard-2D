import pygame
from pygame import mixer


class Mixer:
    def __init__(self,volume):
        mixer.init()
        self.volume = volume
        mixer.music.set_volume(self.volume)
        self.last_update = pygame.time.get_ticks()
        self.play = True


    def play_sound(self,sound):
        if pygame.time.get_ticks() - self.last_update >= 1000:
            self.play = True
        if self.play:
            self.sound = pygame.mixer.Sound(sound)
            pygame.mixer.Sound.play(self.sound)
            pygame.mixer.music.stop()
            self.play = False
            self.last_update = pygame.time.get_ticks()

    def play_soung(self,song,volume):
        mixer.Sound.set_volume(volume)
        self.song = song
        pygame.mixer.music.load(self.song)
        pygame.mixer.music.play(-1)