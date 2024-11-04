import pygame

class Sound():
    def __init__(self):
        self.sounds = {}
        self.load_sounds()
    
    def load_sounds(self):
        self.sounds['overworld'] = pygame.mixer.Sound('assets/sound/overworld.wav')
        self.sounds['overworld_fast'] = pygame.mixer.Sound('assets/sound/overworld-fast.wav')
        self.sounds['level_end'] = pygame.mixer.Sound('assets/sound/levelend.wav')
        self.sounds['coin'] = pygame.mixer.Sound('assets/sound/coin.wav')
        self.sounds['small_mario_jump'] = pygame.mixer.Sound('assets/sound/jump.wav')
        self.sounds['big_mario_jump'] = pygame.mixer.Sound('assets/sound/jumpbig.wav')
        self.sounds['brick_break'] = pygame.mixer.Sound('assets/sound/blockbreak.wav')
        self.sounds['block_hit'] = pygame.mixer.Sound('assets/sound/blockhit.wav')
        self.sounds['mushroom_appear'] = pygame.mixer.Sound('assets/sound/mushroomappear.wav')
        self.sounds['mushroom_eat'] = pygame.mixer.Sound('assets/sound/mushroomeat.wav')
        self.sounds['death'] = pygame.mixer.Sound('assets/sound/death.wav')
        self.sounds['pipe'] = pygame.mixer.Sound('assets/sound/pipe.wav')
        self.sounds['kill_mob'] = pygame.mixer.Sound('assets/sound/kill_mob.wav')
        self.sounds['game_over'] = pygame.mixer.Sound('assets/sound/gameover.wav')
        self.sounds['scorering'] = pygame.mixer.Sound('assets/sound/scorering.wav')
        self.sounds['fireball'] = pygame.mixer.Sound('assets/sound/fireball.wav')
        self.sounds['shot'] = pygame.mixer.Sound('assets/sound/shot.wav')

    def play(self, name, loops, volume):
        self.sounds[name].play(loops=loops)
        self.sounds[name].set_volume(volume)

    def stop(self, name):
        self.sounds[name].stop()

    def start_fast_music(self, core):
        if core.get_map().get_name() == '1-1':
            self.stop('overworld')
            self.play('overworld_fast', 99999, 0.5)