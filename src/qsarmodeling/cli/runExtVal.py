# Importing libraries
import pandas as pd
from qsarmodelingpy.external_validation import ExternalValidation
from qsarmodelingpy.cross_validation_class import CrossValidation
from qsarmodelingpy.kennardstonealgorithm import kennardstonealgorithm
from qsarmodelingpy import lj_cut as lj
import os
import argparse
import logging
import coloredlogs
logging_level = logging.INFO
coloredlogs.DEFAULT_FIELD_STYLES = {'filename': {'color': 'blue'}, 'lineno': {
    'color': 'blue'}, 'funcName': {'color': 'magenta'}, 'levelname': {'bold': True, 'color': 'black'}}
coloredlogs.install(
    fmt="%(filename)s:%(lineno)s %(funcName)s() %(levelname)s  %(message)s", level=logging_level)



def run(filename):
    """Run External Validation with configuration given by `config`.

    `filename` is (usually) a CSV containing all needed information for this function. Please, [see this template](https://github.com/hellmrf/QSARModelingPy/blob/master/examples/confExtVal.csv) and edit for your needs.

    Args:
        filename (str, path, file-like, `io`): The configuration file (usually a CSV). [See this template](https://github.com/hellmrf/QSARModelingPy/blob/master/examples/confExtVal.csv).
    """
    dfConf = pd.read_csv(filename, header=None)
    for idx in range(1, dfConf.shape[1]):
        logging.info(f"Running {idx}/{dfConf.shape[1]-1}.")
        directory = dfConf[idx][0]
        Xfile = dfConf[idx][1]
        yfile = dfConf[idx][2]
        nLV = None if dfConf.isnull()[1][4] else int(dfConf[idx][4])
        out_directory = dfConf[idx][5]
        ext_val_file = dfConf[idx][6]
        cv_file = dfConf[idx][7]
        Xtrain_file = dfConf[idx][8]
        ytrain_file = dfConf[idx][9]
        Xtest_file = dfConf[idx][10]
        ytest_file = dfConf[idx][11]
        autoscale = dfConf[idx][12].upper() == "YES"
        y = pd.read_csv(os.path.join(directory, yfile),
                        sep=';', header=None).values
        dfX = pd.read_csv(os.path.join(directory, Xfile), sep=';', index_col=0)
        dfX = lj.transform(dfX) if dfConf[idx][13].upper() == "YES" else dfX
        X = dfX.values
        type_ext_val = int(dfConf[idx][14])
        if type_ext_val == 1:  # manual selection
            test_set = dfConf[idx][3]
            test = [int(i) - 1 for i in test_set.split(',')]
            train = [j for j in range(len(y)) if j not in test]
        elif type_ext_val == 2:  # Kennard-Stone
            size_test_set = int(dfConf[idx][3])
            # parameter is the size of training set
            train, test = kennardstonealgorithm(dfX, len(dfX) - size_test_set)
        else:  # Random selection
            pass
        ext = ExternalValidation(X, y, nLV)
        ext.extVal(train, test, nLV)
        if ext.validateExtVal(train, test):
            logging.info("External validation passed")
        else:
            logging.info("External validation failed")
        ext.saveExtVal(train, test, out_directory + "/" + ext_val_file)
        cv = CrossValidation(X[train, :], y[train], nLVMax=nLV, scale=True)
        cv.saveParameters(os.path.join(out_directory, cv_file))
        dfXtrain = dfX.loc[dfX.index[train], dfX.columns]
        dfXtrain.to_csv(os.path.join(out_directory, Xtrain_file), sep=';')
        dfytrain = pd.DataFrame(y[train])
        dfytrain.to_csv(os.path.join(out_directory, ytrain_file),
                        sep=',', header=False)
        dfXtest = dfX.loc[dfX.index[test], dfX.columns]
        dfXtest.to_csv(os.path.join(out_directory, Xtest_file), sep=';')
        dfytest = pd.DataFrame(y[test])
        dfytest.to_csv(os.path.join(out_directory, ytest_file),
                       sep=',', header=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--filename', '-f', required=True,
                        metavar='<filename>',
                        help='Config External Validation file.')
    args = parser.parse_args()
    filename = args.filename
    run(filename)
