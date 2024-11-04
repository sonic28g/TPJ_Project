class Observer:
    def on_notify(self, entity, event):
        raise NotImplementedError("This method must be implemented by a subclass")
    
class CoinColector(Observer):
    def on_notify(self, entity, event):
        if event == "coin_collected":
            print("Coin collected by", entity)
            
class Subject:
    def __init__(self):
        self.observers = []
    
    def add_observer(self, obs: Observer):
        self.observers.append(obs)
    
    def npotify(self, entity, event):
        for obs in self.observers:
            obs.on_notify(entity, event)