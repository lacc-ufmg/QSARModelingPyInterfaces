import sys
import numpy as np
import pandas as pd
from modules.ga import Ga
from modules.cross_validation_class import CrossValidation
from modules.yrandomization import YRandomization
from modules.lno import LNO
from modules.filter import variance_cut, correlation_cut
import modules.lj_cut as lj
from modules.validate_yr_lno import validate

# def validate(X,y,pop,Q2,Q2_cut=0.5,yr_cut=0.3,lno_cut=0.1):
#     # y-randomization
#     Q2 = [Q2[i][0] for i,_ in enumerate(Q2)]
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
#     nLV = int(sys.argv[3])
#     out_directory = sys.argv[4]
#     X = dfCorr.values
#     ga = Ga(X,y,nLV,size_population=500,ngen=300)
#     ga.run()
#     ga.saveQ2(out_directory+"/Q2out.json")
#     ga.savePop(out_directory+"/Popout.json")
#     var_sel = validate(X,y,ga.pop_selected,ga.Q2,yr_cut=0.3,lno_cut=0.1)
#     if var_sel != []:
#         dfSel = dfCorr.loc[:,dfCorr.columns[var_sel]]
#         dfSel.to_csv(out_directory+"/XSel.csv",sep=';')
#         cv = CrossValidation(dfSel.values,y)
#         cv.saveParameters(out_directory+"/parameters_cv.csv")
#     else:
#         print("y-randomization or LNO failed!")

if __name__ == '__main__':
    dfConf = pd.read_csv(
        "/home/helitonmrf/OneDrive/Documentos/QSAR/Amostragem por Fecho Convexo/Descritores 4D/matrizes_C_LJ/confGA.csv", header=None)
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
    print("Dimensions of the original matrix")
    print(dfX.shape)
    y = pd.read_csv(directory+"/"+yFile, sep=';', header=None).values
    indVar = variance_cut(dfX.values, var_cut)
    dfVar = dfX.loc[:, dfX.columns[indVar]]
    print("Dimensions of the matrix after of the variance cut")
    print(dfVar.shape)
    indCorr = correlation_cut(dfVar.values, y, corr_cut)
    dfCorr = dfVar.loc[:, dfVar.columns[indCorr]]
    print("Dimensions of the matrix after of the correlation cut")
    print(dfCorr.shape)
    X = dfCorr.values
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
        dfSel = dfCorr.loc[:, dfCorr.columns[var_sel]]
        dfSel.to_csv(out_directory+"/"+out_matrix, sep=';')
        cv = CrossValidation(dfSel.values, y)
        cv.saveParameters(out_directory+"/"+out_cv)
    else:
        print("y-randomization or LNO failed!")
