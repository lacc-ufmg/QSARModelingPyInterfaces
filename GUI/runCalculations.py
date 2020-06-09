import pandas, os
from QSARModelingPy.runGa import run as runGA
from QSARModelingPy.runOPS import run as runOPS
from QSARModelingPy.filter import variance_cut, correlation_cut, autocorrelation_cut


class RunCalculations:

    @staticmethod
    def runGA(config):
        return runGA(config)

    @staticmethod
    def runOPS(config):
        return runOPS(config)

    @staticmethod
    def runVarCut(filename: str, value: float, save: bool = True, output: str = ""):
        df = pandas.read_csv(filename, index_col=0)
        indVar = variance_cut(df.values, value)
        dfCut = df.loc[:, df.columns[indVar]]
        if save:
            if not output:
                name = os.path.split(filename)[-1][:-4]
                output = os.path.join(os.path.dirname(filename),
                                      "{}_filtered_var_{:.2f}.csv".format(name, value))
            dfCut.to_csv(output)
            return output
        else:
            """ In the future, the user will be able to cut the matrix without 
             saving it, leaving it temporarily available within the program to
             perform another calculation in the sequence. """
            pass

    @staticmethod
    def runCorrelationFilter(auto: bool, X_path: str, y_path: str, value: float, save: bool = True, output: str = ""):
        dfX = pandas.read_csv(X_path, index_col=0)
        dfy = pandas.read_csv(y_path, header=None)
        indVar = autocorrelation_cut(dfX.values, dfy, value) if auto else correlation_cut(dfX.values, dfy.values, value)
        dfCut = dfX.loc[:, dfX.columns[indVar]]
        if save:
            if not output:
                name = os.path.split(X_path)[-1][:-4]
                output = os.path.join(os.path.dirname(X_path),
                                      "{}_filtered_{}_{:.2f}.csv".format(name, "autocorr" if auto else "corr", value))
            dfCut.to_csv(output)
            return output
        else:
            """ In the future, the user will be able to cut the matrix without 
             saving it, leaving it temporarily available within the program to
             perform another calculation in the sequence. """
            pass

    @staticmethod
    def runCorrCut(X_path: str, y_path: str, corrcut: float, save: bool = True, output: str = ""):
        RunCalculations.runCorrelationFilter(False, X_path, y_path, corrcut, save, output)

    @staticmethod
    def runAutoCorrCut(X_path: str, y_path: str, autocorrcut: float, save: bool = True, output: str = ""):
        RunCalculations.runCorrelationFilter(True, X_path, y_path, autocorrcut, save, output)
