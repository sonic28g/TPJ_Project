from Goomba import Goomba
from Koopa import Koopa

class MonsterSpawner:
    def __init__(self):
        # Create prototype instances
        self.prototypes = {
            'goomba': Goomba(0, 0),
            'koopa': Koopa(0, 0)
        }
        
    def spawn_monster(self, monster_type, x, y):
        """Spawn a new monster from prototype"""
        if monster_type in self.prototypes:
            monster = self.prototypes[monster_type].clone()
            monster.rect.x = x
            monster.rect.y = y
            return monster
        else:
            raise ValueError(f"Unknown monster type: {monster_type}")