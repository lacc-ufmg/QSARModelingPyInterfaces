import sys
import numpy as np
import pandas as pd
from ops import OPS
from cross_validation_class import CrossValidation
from yrandomization import YRandomization
from lno import LNO
from filter import variance_cut,correlation_cut
import lj_cut as lj
from validate_yr_lno import validate

# def validate(X,y,pop,Q2,Q2_cut=0.5,yr_cut=0.3,lno_cut=0.1):
#     # y-randomization
#     # Q2 = [Q2[i][0] for i,_ in enumerate(Q2)]
#     lpass = []
#     intercepts = []
#     for i,var_sel in enumerate(pop):
#         if Q2[i] > Q2_cut:
#             XSel = X[:,var_sel]
#             cv = CrossValidation(XSel,y)
#             nLV = np.argmax(cv.Q2())+1
#             yr = YRandomization(XSel,y,nLV,50)
#             intercepts.append(yr.returnIntercept())
#             if yr.returnIntercept() < yr_cut:
#                 lpass.append(i)
#     # leave-N-out
#     lpass2 = []
#     if lpass != []:
#         for i in lpass:
#             if Q2[i] > Q2_cut:
#                 XSel = X[:,pop[i]]
#                 m,_ = np.shape(X)
#                 cv = CrossValidation(XSel,y)
#                 nLV = np.argmax(cv.Q2())+1
#                 lno = LNO(XSel,y,nLV,int(m/4),5)
#                 m = np.mean(lno.Q2,1)
#                 std = max([abs(m[j]-m[0]) for j in range(len(m))])
#                 if std < lno_cut:
#                     lpass2.append(i)
#         if lpass2 != []:
#             i = np.argmax([Q2[i] for i in lpass2])
#             var_sel = pop[lpass2[i]]
#             return var_sel
#     else:
#         return []

if __name__=='__main__':
    dfConf = pd.read_csv("confOPS.csv",header=None)
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
    df = pd.read_csv(directory+"/"+xFile,sep=';',index_col=0)
    dfX = lj.transform(df) if dfConf[1][17].upper() == "YES" else df
    autoscale  = dfConf[1][18].upper() == "YES"
    y = pd.read_csv(directory+"/"+yFile,sep=';',header=None).values
    indVar = variance_cut(dfX.values,var_cut)
    dfVar = dfX.loc[:,dfX.columns[indVar]]
    print(dfVar.shape)
    indCorr = correlation_cut(dfVar.values,y,corr_cut)
    dfCorr = dfVar.loc[:,dfVar.columns[indCorr]]
    print(dfCorr.shape)
    X = dfCorr.values
    ops = OPS(X,y,nLVOPS, nLVModel, opsWindow, opsIncrement, percentage, nModels,True)
    ops.runOPS()
    ops.saveModels(out_directory+"/"+out_models)
    var_sel = validate(X,y,ops.models["var_sel"],ops.models["Q2"],yr_cut=yr_crit,lno_cut=lno_crit)
    if var_sel != []:
        dfSel = dfCorr.loc[:,dfCorr.columns[var_sel]]
        dfSel.to_csv(out_directory+"/"+out_matrix,sep=';')
        cv = CrossValidation(dfSel.values,y)
        cv.saveParameters(out_directory+"/"+out_cv)        
    else:
        print("y-randomization or LNO failed!")

# if __name__=='__main__':
#     df = pd.read_csv(sys.argv[1],sep=';',index_col=0)
#     dfX = lj.transform(df)
#     # dfX = df
#     y = pd.read_csv(sys.argv[2],sep=';',header=None).values
#     indVar = variance_cut(dfX.values,0.1)
#     dfVar = dfX.loc[:,dfX.columns[indVar]]
#     print(dfVar.shape)
#     indCorr = correlation_cut(dfVar.values,y,0.3)
#     dfCorr = dfVar.loc[:,dfVar.columns[indCorr]]
#     print(dfCorr.shape)
#     out_directory = sys.argv[3]
#     X = dfCorr.values
#     ops = OPS(X,y,percentage=1,nModels=20)
#     ops.runOPS()
#     # ga.saveQ2(out_directory+"/Q2out.json")
#     # ga.savePop(out_directory+"/Popout.json")
#     var_sel = validate(X,y,ops.models["var_sel"],ops.models["Q2"],yr_cut=0.3,lno_cut=0.1)
#     if var_sel != []:
#         dfSel = dfCorr.loc[:,dfCorr.columns[var_sel]]
#         dfSel.to_csv(out_directory+"/XSel.csv",sep=';')
#         cv = CrossValidation(dfSel.values,y)
#         cv.saveParameters(out_directory+"/parameters_cv.csv")
#     else:
#         print("y-randomization or LNO failed!")