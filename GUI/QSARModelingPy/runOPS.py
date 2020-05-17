import sys
import numpy as np
import pandas as pd
from QSARModelingPy.ops import OPS
from QSARModelingPy.cross_validation_class import CrossValidation
from QSARModelingPy.yrandomization import YRandomization
from QSARModelingPy.lno import LNO
from QSARModelingPy.filter import variance_cut, correlation_cut, autocorrelation_cut
import QSARModelingPy.lj_cut as lj
from QSARModelingPy.validate_yr_lno import validate
import os
import sys
import argparse


def run(config):
    # Open configuration file in order to look for the matrices and the parameters to run
    # OPS and cross-validation
    xFile = config['XMatrix']
    yFile = config['yvector']
    var_cut = float(config['varcut'])
    corr_cut = float(config['corrcut'])
    nLVOPS = None if int(config['latent_vars_ops']) == 0 else int(config['latent_vars_ops'])
    nLVModel = None if int(config['latent_vars_model']) == 0 else int(config['latent_vars_model'])
    opsWindow = int(config['ops_window'])
    opsIncrement = int(config['ops_increment'])
    percentage = int(config['vars_percentage'])
    nModels = int(config['models_to_save'])
    yr_crit = float(config['yrand'])
    lno_crit = float(config['lno'])
    out_matrix = config['output_matrix']
    out_cv = config['output_cv']
    out_models = config['output_models']
    df = pd.read_csv(xFile, index_col=0)
    # Filtering the matrix according to the options in configuration file
    dfX = lj.transform(df) if config['lj_transform'] else df
    print("Dimensions of the original matrix")
    print(dfX.shape)
    autoscale = config['autoscale']
    y = pd.read_csv(yFile, header=None).values
    indVar = variance_cut(dfX.values, var_cut)
    dfVar = dfX.loc[:, dfX.columns[indVar]]
    print("Dimensions of the matrix after variance cut")
    print(dfVar.shape)
    indCorr = correlation_cut(dfVar.values, y, corr_cut)
    dfCorr = dfVar.loc[:, dfVar.columns[indCorr]]
    print("Dimensions of the matrix after correlation cut")
    print(dfCorr.shape)
    auto_cut = float(config['autocorrcut'])
    indAuto = autocorrelation_cut(dfCorr.values, y, auto_cut)
    dfRest = dfCorr.loc[:, dfCorr.columns[indAuto]]
    print("Dimensions of the matrix after auto correlation cut")
    print(dfRest.shape)
    dfRest.to_csv(out_matrix)
    X = dfRest.values
    ops = OPS(X, y, nLVOPS, nLVModel, opsWindow, opsIncrement, percentage, nModels, autoscale)
    typeOPS = config['ops_type']
    if typeOPS == 's':
        ops.runOPS()
    elif typeOPS == 'f':
        ops.feedOPS()
    else:
        print("Invalid option for type OPS. Type s for single run or f for feedOPS")
        return
    ops.saveModels(out_models)
    var_sel = validate(X, y, ops.models["var_sel"], ops.models["Q2"], yr_cut=yr_crit, lno_cut=lno_crit)
    if var_sel:
        dfSel = dfCorr.loc[:, dfCorr.columns[var_sel]]
        dfSel.to_csv(out_matrix)
        cv = CrossValidation(dfSel.values, y)
        cv.saveParameters(out_cv)
    else:
        print("y-randomization or LNO failed!")