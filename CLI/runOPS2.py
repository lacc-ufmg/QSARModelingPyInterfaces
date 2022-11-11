# Importing libraries
import pandas as pd
from qsarmodelingpy.ops import OPS
from qsarmodelingpy.cross_validation_class import CrossValidation
from qsarmodelingpy.filter import filter_matrix #, variance_cut, correlation_cut, autocorrelation_cut
from qsarmodelingpy import lj_cut as lj
from qsarmodelingpy.validate_yr_lno import validate
from qsarmodelingpy import Utils
import os
import argparse
import logging
import coloredlogs



def run(filename, typeOPS):
    """Open configuration file in order to look for the matrices and the parameters to run OPS and cross-validation"""
    dfConf = pd.read_csv(filename, header=None)
    for idx in range(1, dfConf.shape[1]):
        logging.info(f"Running {idx}/{dfConf.shape[1]-1}.")
        directory = dfConf[idx][0]
        xFile = dfConf[idx][1]
        yFile = dfConf[idx][2]

        xpath = os.path.join(directory, xFile)
        ypath = os.path.join(directory, yFile)

        var_cut = float(dfConf[idx][3])
        corr_cut = float(dfConf[idx][4])
        nLVOPS = None if dfConf.isnull()[1][5] else dfConf[idx][5]
        nLVModel = None if dfConf.isnull()[1][6] else dfConf[idx][6]
        opsWindow = int(dfConf[idx][7])
        opsIncrement = int(dfConf[idx][8])
        percentage = int(dfConf[idx][9])
        nModels = int(dfConf[idx][10])
        yr_crit = float(dfConf[idx][11])
        lno_crit = float(dfConf[idx][12])
        out_directory = dfConf[idx][13]
        out_matrix = dfConf[idx][14]
        out_cv = dfConf[idx][15]
        out_models = dfConf[idx][16]
        lj_transform = dfConf[idx][17].upper() == "YES"
        autoscale = dfConf[idx][18].upper() == "YES"
        autocorr_cut = float(dfConf[idx][19])

        df = Utils.load_matrix(xpath)
        y = pd.read_csv(ypath, header=None).values
        dfFiltered = filter_matrix(df, y, lj_transform, var_cut, corr_cut, autocorr_cut)
        X = dfFiltered.values
        ops = OPS(X, y, nLVOPS, nLVModel, opsWindow,
                  opsIncrement, percentage, nModels, autoscale)
        if typeOPS.lower() == 's':
            ops.runOPS()
        elif typeOPS.lower() == 'f':
            ops.feedOPS()
        else:
            logging.error(
                "Invalid option for type OPS. Type s for single run or f for feedOPS")
            return
        ops.saveModels(os.path.join(out_directory, out_models))
        var_sel = validate(
            X, y, ops.models["var_sel"], ops.models["Q2"], yr_cut=yr_crit, lno_cut=lno_crit)
        if var_sel != []:
            dfSel = dfFiltered.loc[:, dfFiltered.columns[var_sel]]
            dfSel.to_csv(os.path.join(out_directory, out_matrix))
            cv = CrossValidation(dfSel.values, y)
            cv.saveParameters(os.path.join(out_directory, out_cv))
        else:
            logging.error("y-randomization or LNO failed!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--filename', '-f', required=True,
                        metavar='<filename>',
                        help='Config OPS file.')
    parser.add_argument('--type', '-t', required=True, type=str,
                        metavar='<t>',
                        help='Type of OPS run (s for single and f for feed).'
                        )
    parser.add_argument('--verbose', '-v', required=False, action='store_true', help="Print more detailed (and potentialy trash) information.")

    args = parser.parse_args()
    filename = args.filename
    typeOPS = args.type
    verbose = args.verbose

    logging_level = logging.DEBUG if verbose else logging.INFO
    coloredlogs.DEFAULT_FIELD_STYLES = {'filename': {'color': 'blue'}, 'lineno': {
        'color': 'blue'}, 'funcName': {'color': 'magenta'}, 'levelname': {'bold': True, 'color': 'black'}}
    coloredlogs.install(
        fmt="%(filename)s:%(lineno)s %(funcName)s() %(levelname)s  %(message)s", level=logging_level)
    
    logging.debug("Debug (verbose) mode active.")

    run(filename, typeOPS)
