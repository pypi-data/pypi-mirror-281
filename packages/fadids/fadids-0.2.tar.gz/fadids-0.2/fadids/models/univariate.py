import numpy as np
from typing import List
from streamad.model import SRDetector
from fadids.models.container import UnivariateContainer


class MeanDeviationAD():
    def __init__(self, window_len=50, threshold=1) -> None:
        """
        Initialize the MeanDeviationAD anomaly detection model.

        Args:
            window_len (int): The number of samples in the moving window.
            threshold (float): The number of standard deviations away from the mean
                               to consider an observation as an anomaly.

        Attributes:
            expected_low (float): Lower boundary for anomaly detection.
            expected_high (float): Upper boundary for anomaly detection.
            init_done (bool): Flag to check if the initialization is complete.
            predictions (list[bool]): List to store anomaly predictions.
            last_sample (list[float]): List to store the last window of observations.
        """
        self.window_len = window_len
        self.threshold = threshold
        self.expected_low: float = 0
        self.expected_high: float = 0
        self.init_done: bool = False
        self.predictions = []
        self.last_sample = []

    def fit(self, data: List[float]):
        """Fill a list of last data values, and predict if the list > window.size. Finally, reduct the list.

        Args:
            data (List[float]): values for fit and predict
        """
        current_sample = self.last_sample + data
        if len(current_sample) > self.window_len:
            for index in range(len(current_sample)):
                if index >= self.window_len:
                    self._predict(current_sample[index-self.window_len:index])
        try:
            self.last_sample = current_sample[-self.window_len:]
        except KeyError:
            self.last_sample = current_sample

    def _predict(self, data):
        means = np.mean(data)
        deviations = np.std(data)
        if self.init_done:  # initialize expected values before anomaly detection
            pred_tmp = (means > self.expected_high) | (
                means < self.expected_low)
            self.predictions.append(pred_tmp)
        else:
            for i in range(self.window_len + 1):
                self.predictions.append(False)
            self.init_done = True
        self.expected_high = means + self.threshold * deviations
        self.expected_low = means - self.threshold * deviations

    def check_anomalies(self):
        """check if anomalies are detected"""
        return np.array(self.predictions).any()

    def get_anomalies(self):
        '''return a list of anomalies indices'''
        indices_true = [index for index,
                        value in enumerate(self.predictions) if value]
        return indices_true

    def get_scores(self):
        """return scores anomalies scores for each prediction

        Returns:
            Dict[int, float]: dictionnaire score
        """
        idxs = [i for i in range(len(self.predictions))]
        scores = dict(zip(idxs, self.predictions))
        return scores


class SpectralResidualAD(UnivariateContainer):
    def __init__(self, threshold=0.9, initialization=300, extend_len=5, ahead_len=10, mag_num=5) -> None:
        self.model = SRDetector(extend_len, ahead_len, mag_num)
        super().__init__(self.model, threshold, initialization)
        self.threshold = threshold
        self.initialization = initialization
