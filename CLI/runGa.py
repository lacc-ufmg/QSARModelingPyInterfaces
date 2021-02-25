import pandas as pd
from qsarmodelingpy.ga import Ga
from qsarmodelingpy.cross_validation_class import CrossValidation
from qsarmodelingpy.filter import variance_cut, correlation_cut, autocorrelation_cut
from qsarmodelingpy import lj_cut as lj
from qsarmodelingpy.validate_yr_lno import validate
import os
import argparse
import logging


def run(filename):
    dfConf = pd.read_csv(filename, header=None)
    directory = dfConf[1][0]
    xFile = dfConf[1][1]
    yFile = dfConf[1][2]
    var_cut = float(dfConf[1][3])
    corr_cut = float(dfConf[1][4])
    nLVModel = None if dfConf.isnull()[1][5] else int(dfConf[1][5])
    min_size = int(dfConf[1][6])
    max_size = int(dfConf[1][7])
    size_population = int(dfConf[1][8])
    mig_rate = float(dfConf[1][9])
    cxpb = float(dfConf[1][10])
    mutpb = float(dfConf[1][11])
    ngen = int(dfConf[1][12])
    yr_crit = float(dfConf[1][13])
    lno_crit = float(dfConf[1][14])
    out_directory = dfConf[1][15]
    out_matrix = dfConf[1][16]
    out_cv = dfConf[1][17]
    Q2_file = dfConf[1][18]
    var_sel_file = dfConf[1][19]
    autoscale = dfConf[1][20].upper() == "YES"
    df = pd.read_csv(directory+"/"+xFile, sep=';', index_col=0)
    dfX = lj.transform(df) if dfConf[1][21].upper() == "YES" else df
    logging.info("Dimensions of the original matrix")
    logging.info(dfX.shape)
    y = pd.read_csv(directory+"/"+yFile, sep=';', header=None).values
    indVar = variance_cut(dfX.values, var_cut)
    dfVar = dfX.loc[:, dfX.columns[indVar]]
    logging.info("Dimensions of the matrix after the variance cut")
    logging.info(dfVar.shape)
    indCorr = correlation_cut(dfVar.values, y, corr_cut)
    dfCorr = dfVar.loc[:, dfVar.columns[indCorr]]
    logging.info("Dimensions of the matrix after the correlation cut")
    logging.info(dfCorr.shape)
    auto_cut = float(dfConf[1][22])
    indAuto = autocorrelation_cut(dfCorr.values, y, auto_cut)
    dfRest = dfCorr.loc[:, dfCorr.columns[indAuto]]
    logging.info("Dimensions of the matrix after auto correlation cut")
    logging.info(dfRest.shape)
    dfRest.to_csv(os.path.join(out_directory, "filtered_"+out_matrix), sep=';')
    X = dfRest.values
    if nLVModel == None:
        nLVModel = int(dfCorr.shape[0]/5)
    ga = Ga(X, y, nLVModel, autoscale, min_size, max_size,
            size_population, mig_rate, cxpb, mutpb, ngen)
    ga.run()
    ga.saveQ2(out_directory+"/"+Q2_file)
    ga.savePop(out_directory+"/"+var_sel_file)
    Q2 = ga.Q2
    Q2 = [Q2[i][0] for i, _ in enumerate(Q2)]
    var_sel = validate(X, y, ga.pop_selected, Q2,
                       yr_cut=yr_crit, lno_cut=lno_crit)
    if var_sel != []:
        dfSel = dfRest.loc[:, dfRest.columns[var_sel]]
        dfSel.to_csv(out_directory+"/"+out_matrix, sep=';')
        cv = CrossValidation(dfSel.values, y)
        cv.saveParameters(out_directory+"/"+out_cv)
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
