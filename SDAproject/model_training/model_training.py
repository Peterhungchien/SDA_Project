class TestModel:
    def __init__(self, hyper_param) -> None:
        self.hyper_param = hyper_param

    def train(self, data):
        print("Training model with hyper param: ", self.hyper_param)
        print("Training data: ", data)
        self.is_trained = True

    def predict(self, data):
        print("Predicting with model: ", self.hyper_param)
        print("Predicting data: ", data)
        return [1, 2, 3]
