class Block:
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY

class Block_Normal(Block):
    def __init__(self, posX, posY):
        super().__init__(posX, posY)
        self.sprite = None


class Block_Coin(Block):
    def __init__(self, posX, posY, nc):
        super().__init__(posX, posY)
        self.numCoins = nc
        self.sprite = None


class Block_PowerUp(Block):
    def __init__(self, posX, posY, pu):
        super().__init__(posX, posY)
        self.sprite = None
        self.powerUp = pu


class Block_Int(Block):
    def __init__(self, posX, posY, pu):
        super().__init__(posX, posY)
        self.sprite = None
        self.powerUp = pu


class Block_Invisible(Block):
    def __init__(self, posX, posY, pu):
        super().__init__(posX, posY)
        self.sprite = None
        self.powerUp = pu
