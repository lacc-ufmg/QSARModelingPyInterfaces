import sys
import numpy as np
import pandas as pd
import os
import argparse
from QSARModelingPy.ga import Ga
from QSARModelingPy.cross_validation_class import CrossValidation
from QSARModelingPy.yrandomization import YRandomization
from QSARModelingPy.lno import LNO
from QSARModelingPy.filter import variance_cut, correlation_cut, autocorrelation_cut
import QSARModelingPy.lj_cut as lj
from QSARModelingPy.validate_yr_lno import validate


def run(config: dict) -> bool:
    """
    Run Genetic Algorithm
    :param config:
    :return: True if validation pass, False otherwise
    :rtype: bool
    """
    xFile = config['XMatrix']
    yFile = config['yvector']
    var_cut = float(config['varcut'])
    corr_cut = float(config['corrcut'])
    nLVModel = None if int(config['max_latent_model']) == 0 else int(config['max_latent_model'])
    min_size = int(config['min_vars_model'])
    max_size = int(config['max_vars_model'])
    size_population = int(config['population_size'])
    mig_rate = float(config['migration_rate'])
    cxpb = float(config['crossover_rate'])
    mutpb = float(config['mutation_rate'])
    ngen = int(config['generations'])
    yr_crit = float(config['yrand'])
    lno_crit = float(config['lno'])
    out_matrix = config['output_matrix']
    out_cv = config['output_cv']
    Q2_file = config['output_q2']
    var_sel_file = config['output_selected']
    autoscale = config['autoscale']
    df = pd.read_csv(xFile, index_col=0)
    dfX = lj.transform(df) if config['lj_transform'] else df
    print("Dimensions of the original matrix")
    print(dfX.shape)
    y = pd.read_csv(yFile, header=None).values
    indVar = variance_cut(dfX.values, var_cut)
    dfVar = dfX.loc[:, dfX.columns[indVar]]
    print("Dimensions of the matrix after the variance cut")
    print(dfVar.shape)
    indCorr = correlation_cut(dfVar.values, y, corr_cut)
    dfCorr = dfVar.loc[:, dfVar.columns[indCorr]]
    print("Dimensions of the matrix after the correlation cut")
    print(dfCorr.shape)
    auto_cut = float(config['autocorrcut'])
    indAuto = autocorrelation_cut(dfCorr.values,y,auto_cut)
    dfRest = dfCorr.loc[:,dfCorr.columns[indAuto]]
    print("Dimensions of the matrix after auto correlation cut")
    print(dfRest.shape)
    dfRest.to_csv(out_matrix)
    X = dfRest.values
    if nLVModel is None:
        nLVModel = int(dfCorr.shape[0]/5)
    ga = Ga(X, y, nLVModel, autoscale, min_size, max_size, size_population, mig_rate, cxpb, mutpb, ngen)
    ga.run()
    ga.saveQ2(Q2_file)
    ga.savePop(var_sel_file)
    Q2 = ga.Q2
    Q2 = [Q2[i][0] for i, _ in enumerate(Q2)]
    var_sel = validate(X, y, ga.pop_selected, Q2, yr_cut=yr_crit, lno_cut=lno_crit)
    if var_sel != []:
        dfSel = dfRest.loc[:,dfRest.columns[var_sel]]
        dfSel.to_csv(out_matrix)
        cv = CrossValidation(dfSel.values, y)
        cv.saveParameters(out_cv)
        return True
    else:
        return False