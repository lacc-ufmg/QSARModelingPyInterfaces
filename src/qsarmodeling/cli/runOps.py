import pandas as pd
from qsarmodelingpy.ops import OPS
from qsarmodelingpy.cross_validation_class import CrossValidation
from qsarmodelingpy.filter import variance_cut, correlation_cut
from qsarmodelingpy import lj_cut as lj
from qsarmodelingpy.validate_yr_lno import validate
import logging

if __name__ == "__main__":
    dfConf = pd.read_csv("confOPS.csv", header=None)
    directory = dfConf[1][0]
    xFile = dfConf[1][1]
    yFile = dfConf[1][2]
    var_cut = float(dfConf[1][3])
    corr_cut = float(dfConf[1][4])
    nLVOPS = None if dfConf.isnull()[1][5] else int(dfConf[1][5])
    nLVModel = None if dfConf.isnull()[1][6] else int(dfConf[1][6])
    opsWindow = int(dfConf[1][7])
    opsIncrement = int(dfConf[1][8])
    percentage = int(dfConf[1][9])
    nModels = int(dfConf[1][10])
    yr_crit = float(dfConf[1][11])
    lno_crit = float(dfConf[1][12])
    out_directory = dfConf[1][13]
    out_matrix = dfConf[1][14]
    out_cv = dfConf[1][15]
    out_models = dfConf[1][16]
    df = pd.read_csv(directory + "/" + xFile, sep=";", index_col=0)
    dfX = lj.transform(df) if dfConf[1][17].upper() == "YES" else df
    autoscale = dfConf[1][18].upper() == "YES"
    y = pd.read_csv(directory + "/" + yFile, sep=";", header=None).values
    indVar = variance_cut(dfX.values, var_cut)
    dfVar = dfX.loc[:, dfX.columns[indVar]]
    logging.info(dfVar.shape)
    indCorr = correlation_cut(dfVar.values, y, corr_cut)
    dfCorr = dfVar.loc[:, dfVar.columns[indCorr]]
    logging.info(dfCorr.shape)
    X = dfCorr.values
    ops = OPS(
        X, y, nLVOPS, nLVModel, opsWindow, opsIncrement, percentage, nModels, True
    )
    ops.runOPS()
    ops.saveModels(out_directory + "/" + out_models)
    var_sel = validate(
        X, y, ops.models["var_sel"], ops.models["Q2"], yr_cut=yr_crit, lno_cut=lno_crit
    )
    if var_sel != []:
        dfSel = dfCorr.loc[:, dfCorr.columns[var_sel]]
        dfSel.to_csv(out_directory + "/" + out_matrix, sep=";")
        cv = CrossValidation(dfSel.values, y)
        cv.saveParameters(out_directory + "/" + out_cv)
    else:
        logging.error("y-randomization or LNO failed!")
