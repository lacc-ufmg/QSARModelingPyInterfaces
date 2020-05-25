import pandas, os
from QSARModelingPy.runGa import run as runGA
from QSARModelingPy.runOPS import run as runOPS
from QSARModelingPy.filter import variance_cut


class RunCalculations:

    @staticmethod
    def runGA(config):
        return runGA(config)

    @staticmethod
    def runOPS(config):
        return runOPS(config)

    @staticmethod
    def runVarCut(filename: str, varcut: float, save: bool = True, output: str = ""):
        df = pandas.read_csv(filename, index_col=0)
        indVar = variance_cut(df.values, varcut)
        dfCut = df.loc[:, df.columns[indVar]]
        if save:
            if not output:
                name = os.path.split(filename)[-1][:-4]
                output = os.path.join(os.path.dirname(filename), "{}_filtered_var_{:.2f}.csv".format(name, varcut))
            dfCut.to_csv(output)
            return output
        else:
            """ In the future, the user will be able to cut the matrix without 
             saving it, leaving it temporarily available within the program to
             perform another calculation in the sequence. """
            pass
