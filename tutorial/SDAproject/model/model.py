class Model:
    
    def __init__(self, params) -> None:
        self.params = params

    def train(self, data):
        self.is_trained = True
        pass

    def predict(self, data):
        if not self.is_trained:
            raise Exception("Model not trained")
        pass
        