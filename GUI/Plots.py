import numpy as np
import logging, logger
import matplotlib.pyplot as plt  # TODO: add do dependecies
logger.silence_matplotlib_logger()
from abc import ABC, abstractmethod
from qsarmodelingpy.cross_validation_class import CrossValidation
import Utils


class Plots(ABC):

    @abstractmethod
    def get_methods(self) -> dict:
        pass


class CrossValidationPlots(Plots):
    def __init__(self) -> None:
        matplolib_config = Utils.read_config("matplotlib")
        plt.rcParams.update(matplolib_config)

    def Q2_R2_evolution(self, cv: CrossValidation):
        xaxis = range(1, cv.nLVMax + 1)
        y1 = cv.R2()
        y2 = cv.Q2()
        plt.plot(xaxis, y1, label="R²", marker='o')
        plt.plot(xaxis, y2, label="Q²", marker='o')
        plt.legend()
        plt.title("Cross-Validation error - PLS")
        plt.xlabel("nLV")
        plt.ylabel(r"$R^2 / Q^2$")
        plt.show()

    def scatter_Q2_R2(self):
        raise NotImplementedError()

    def y_versus_ŷ_CV(self, cv: CrossValidation):
        nLV = int(cv.returnParameters().loc["nLV"][0])
        xaxis = np.array(cv.y)
        yaxis = list(cv.ycv[:, nLV-1])
        plt.plot(xaxis, xaxis, color="red", linewidth=1, label="y = x line")
        plt.plot(xaxis, yaxis, linestyle="None", marker="o", label="Data")
        plt.title("Cross-Validation prediction")
        plt.xlabel("Experimental activity")
        plt.ylabel("Predicted activity")
        plt.show()

    def y_versus_ŷ_cal(self, cv: CrossValidation):
        nLV = int(cv.returnParameters().loc["nLV"][0])
        xaxis = np.array(cv.y)
        yaxis = list(cv.ycal[:, nLV-1])
        plt.plot(xaxis, xaxis, color="red", linewidth=1, label="y = x line")
        plt.plot(xaxis, yaxis, linestyle="None", marker="o", label="Data")
        plt.title("Calibration prediction")
        plt.xlabel("Experimental activity")
        plt.ylabel("Predicted activity")
        plt.show()

    def get_methods(self) -> list:
        return {
            "Q² and R² × Latent Variables": self.Q2_R2_evolution,
            "Exprimental × Predicted (calibration)": self.y_versus_ŷ_cal,
            "Exprimental × Predicted (cross-validation)": self.y_versus_ŷ_CV,
        }


if __name__ == "__main__":
    import pandas as pd
    import os
    import coloredlogs
    import logging
    logging_level = logging.DEBUG
    coloredlogs.install(
        fmt="%(filename)s:%(lineno)s %(funcName)s() %(levelname)s  %(message)s", level=logging_level)
    coloredlogs.DEFAULT_FIELD_STYLES = {'filename': {'color': 'blue'}, 'lineno': {
        'color': 'blue'}, 'funcName': {'color': 'magenta'}, 'levelname': {'bold': True, 'color': 'black'}}

    directory = "/home/helitonmrf/Documents/QSAR/cancer_prostata/resultados"
    X_matrix_file = "filtered_10_GA_X_sel.csv"
    y_matrix_file = "../atividades.txt"

    df = pd.read_csv(os.path.join(directory, X_matrix_file),
                     sep=';', index_col=0)
    X = df.to_numpy()
    y = pd.read_csv(os.path.join(directory, y_matrix_file),
                    sep=';', header=None).values
    cv = CrossValidation(X, y)
    methods = CrossValidationPlots().get_methods()
    logging.debug(f"{methods = }")

    for method in methods:
        methods[method](cv)
        break