import pandas as pd
from qsarmodelingpy.ga import Ga
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



def run(filename):
    dfConf = pd.read_csv(filename, header=None)
    for idx in range(1, dfConf.shape[1]):
        logging.info(f"Running {idx}/{dfConf.shape[1]-1}.")
        directory = dfConf[idx][0]
        xFile = dfConf[idx][1]
        yFile = dfConf[idx][2]
        var_cut = float(dfConf[idx][3])
        corr_cut = float(dfConf[idx][4])
        nLVModel = None if dfConf.isnull()[1][5] else int(dfConf[idx][5])
        min_size = int(dfConf[idx][6])
        max_size = int(dfConf[idx][7])
        size_population = int(dfConf[idx][8])
        mig_rate = float(dfConf[idx][9])
        cxpb = float(dfConf[idx][10])
        mutpb = float(dfConf[idx][11])
        ngen = int(dfConf[idx][12])
        yr_crit = float(dfConf[idx][13])
        lno_crit = float(dfConf[idx][14])
        out_directory = dfConf[idx][15]
        out_matrix = dfConf[idx][16]
        out_cv = dfConf[idx][17]
        Q2_file = dfConf[idx][18]
        var_sel_file = dfConf[idx][19]
        autoscale = dfConf[idx][20].upper() == "YES"
        df = pd.read_csv(directory + "/" + xFile, sep=';', index_col=0)
        dfX = lj.transform(df) if dfConf[idx][21].upper() == "YES" else df
        logging.info("Dimensions of the original matrix")
        logging.info(dfX.shape)
        y = pd.read_csv(directory + "/" + yFile, sep=';', header=None).values
        indVar = variance_cut(dfX.values, var_cut)
        dfVar = dfX.loc[:, dfX.columns[indVar]]
        logging.info("Dimensions of the matrix after the variance cut")
        logging.info(dfVar.shape)
        indCorr = correlation_cut(dfVar.values, y, corr_cut)
        dfCorr = dfVar.loc[:, dfVar.columns[indCorr]]
        logging.info("Dimensions of the matrix after the correlation cut")
        logging.info(dfCorr.shape)
        auto_cut = float(dfConf[idx][22])
        indAuto = autocorrelation_cut(dfCorr.values, y, auto_cut)
        dfRest = dfCorr.loc[:, dfCorr.columns[indAuto]]
        logging.info("Dimensions of the matrix after auto correlation cut")
        logging.info(dfRest.shape)
        dfRest.to_csv(os.path.join(
            out_directory, "filtered_" + out_matrix), sep=';')
        X = dfRest.values
        if nLVModel == None:
            nLVModel = int(dfCorr.shape[0] / 5)
        ga = Ga(X, y, nLVModel, autoscale, min_size, max_size,
                size_population, mig_rate, cxpb, mutpb, ngen)
        ga.run()
        ga.saveQ2(out_directory + "/" + Q2_file)
        ga.savePop(out_directory + "/" + var_sel_file)
        Q2 = ga.Q2
        Q2 = [Q2[i][0] for i, _ in enumerate(Q2)]
        var_sel = validate(X, y, ga.pop_selected, Q2,
                           yr_cut=yr_crit, lno_cut=lno_crit)
        if var_sel != []:
            dfSel = dfRest.loc[:, dfRest.columns[var_sel]]
            dfSel.to_csv(out_directory + "/" + out_matrix, sep=';')
            cv = CrossValidation(dfSel.values, y)
            cv.saveParameters(out_directory + "/" + out_cv)
        else:
            logging.error("y-randomization or LNO failed!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--filename', '-f', required=True,
                        metavar='<filename>',
                        help='Config GA file.')
    args = parser.parse_args()
    filename = args.filename
    run(filename)
