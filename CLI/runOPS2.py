# Importing libraries
import pandas as pd
from qsarmodelingpy.ops import OPS
from qsarmodelingpy.cross_validation_class import CrossValidation
from qsarmodelingpy.filter import variance_cut, correlation_cut, autocorrelation_cut
from qsarmodelingpy import lj_cut as lj
from qsarmodelingpy.validate_yr_lno import validate
import os
import argparse
import logging
import coloredlogs
logging_level = logging.INFO
coloredlogs.DEFAULT_FIELD_STYLES = {'filename': {'color': 'blue'}, 'lineno': {
    'color': 'blue'}, 'funcName': {'color': 'magenta'}, 'levelname': {'bold': True, 'color': 'black'}}
coloredlogs.install(
    fmt="%(filename)s:%(lineno)s %(funcName)s() %(levelname)s  %(message)s", level=logging_level)



def run(filename, typeOPS):
    """Open configuration file in order to look for the matrices and the parameters to run OPS and cross-validation"""
    dfConf = pd.read_csv(filename, header=None)
    for idx in range(1, dfConf.shape[1]):
        logging.info(f"Running {idx}/{dfConf.shape[1]-1}.")
        directory = dfConf[idx][0]
        xFile = dfConf[idx][1]
        yFile = dfConf[idx][2]
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
        df = pd.read_csv(os.path.join(directory, xFile), sep=';', index_col=0)
        # Filtering the matrix according to the options in configuration file
        dfX = lj.transform(df) if dfConf[idx][17].upper() == "YES" else df
        logging.info("Dimensions of the original matrix")
        logging.info(dfX.shape)
        autoscale = dfConf[idx][18].upper() == "YES"
        y = pd.read_csv(os.path.join(directory, yFile),
                        sep=';', header=None).values
        indVar = variance_cut(dfX.values, var_cut)
        dfVar = dfX.loc[:, dfX.columns[indVar]]
        logging.info("Dimensions of the matrix after variance cut")
        logging.info(dfVar.shape)
        indCorr = correlation_cut(dfVar.values, y, corr_cut)
        dfCorr = dfVar.loc[:, dfVar.columns[indCorr]]
        logging.info("Dimensions of the matrix after correlation cut")
        logging.info(dfCorr.shape)
        auto_cut = float(dfConf[idx][19])
        indAuto = autocorrelation_cut(dfCorr.values, y, auto_cut)
        dfRest = dfCorr.loc[:, dfCorr.columns[indAuto]]
        logging.info("Dimensions of the matrix after auto correlation cut")
        logging.info(dfRest.shape)
        dfRest.to_csv(os.path.join(
            out_directory, "filtered_" + out_matrix), sep=';')
        X = dfRest.values
        ops = OPS(X, y, nLVOPS, nLVModel, opsWindow,
                  opsIncrement, percentage, nModels, autoscale)
        if typeOPS == 's':
            ops.runOPS()
        elif typeOPS == 'f':
            ops.feedOPS()
        else:
            logging.error(
                "Invalid option for type OPS. Type s for single run or f for feedOPS")
            return
        ops.saveModels(os.path.join(out_directory, out_models))
        var_sel = validate(
            X, y, ops.models["var_sel"], ops.models["Q2"], yr_cut=yr_crit, lno_cut=lno_crit)
        if var_sel != []:
            dfSel = dfCorr.loc[:, dfCorr.columns[var_sel]]
            dfSel.to_csv(os.path.join(out_directory, out_matrix), sep=';')
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

    args = parser.parse_args()
    filename = args.filename
    typeOPS = args.type
    run(filename, typeOPS)
