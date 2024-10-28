class State:
    def __init__(self, name) -> None:
        self.name = name
    
    def enter(self):
        pass

    def update(self, object):
        pass

    def exit(self):
        pass

class Transition:
    def __init(self, _from, _to) -> None:
        self._from = _from
        self._to = _to



class Idle(State):
    def __init__(self) -> None:
        pass

    def update(self, object):
        pass


class Walk(State):
    def __init__(self) -> None:
        pass

    def update(self, object):
        pass


class Jump(State):
    def __init__(self) -> None:
        pass

    def update(self, object):
        pass


class Crouch(State):
    def __init__(self) -> None:
        pass

    def update(self, object):
        pass


class Fire(State):
    def __init__(self) -> None:
        pass

    def update(self, object):
        pass