from QSARModelingPy.runGa import run as runGA
from QSARModelingPy.runOPS import run as runOPS


class RunCalculations:

    @staticmethod
    def runGA(config):
        return runGA(config)

    @staticmethod
    def runOPS(config):
        return runOPS(config)
