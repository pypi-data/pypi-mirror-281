import numpy as np


class AbstractContainer():
    def __init__(self, model, threshold: float, initialization: int, pca=False) -> None:
        """Initialize a model for anomaly detection in data stream

        Args:
            model (_type_): a streamad model
            threshold (float): threshold that will change the numbers of anomaly detected
            initialization (int): number of values to wait before the anomaly detection
        """
        self.model = model
        self.threshold = threshold
        self.initialization = initialization
        self.anomalies_scores = []
        self.predictions = []

    def update() -> None:
        """fit the model and calcul an anomaly score for each new point based on drift concept"""
        pass

    def check_anomalies(self) -> bool:
        """check if anomalies are detected"""

        return np.array(self.predictions).any()

    def get_anomalies(self):
        '''return a list of anomalies indices'''
        indices_true = [index for index,
                        value in enumerate(self.predictions) if value]
        return indices_true


class UnivariateContainer(AbstractContainer):
    def __init__(self, model, threshold: float = 0.9, initialization: int = 600) -> None:
        super().__init__(model, threshold, initialization)

    def fit(self, data: np.ndarray):
        current_data = data.reshape(-1, 1)
        for x in current_data:
            score = self.model.fit_score(x)
            try:
                if (score > self.threshold) & (len(self.anomalies_scores) > self.initialization):
                    self.predictions.append(True)
                else:
                    self.predictions.append(False)
            except TypeError:
                self.predictions.append(False)
            self.anomalies_scores.append(score)
