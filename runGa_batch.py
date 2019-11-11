import sys, os
import numpy as np
import pandas as pd
from ga import Ga
from cross_validation_class import CrossValidation
from yrandomization import YRandomization
from lno import LNO
from filter import variance_cut,correlation_cut
import lj_cut as lj
from validate_yr_lno import validate
# sendMail():
from datetime import datetime
import yagmail

def sendMail(current_matrix,current_matrix_name, total_matrices, status, out_file, end = False):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    yag = yagmail.SMTP("contato.ongrade@gmail.com","8425408778")
    to = "helitonmrf@gmail.com"
    content = ""
    attachment = None
    if(status == True):
        content += "Last job terminated <b style='color:#009900;'>SUCCESSFULLY</b>."
        attachment = out_file
    elif (status == False):
        content += "Last job terminated <b style='color:#CC0000;'>ABNORMALLY</b>."

    if(end == True):
        subject = "QSARModelingPy Update: all jobs are done!"
        content += "\n\n[{}] All jobs are now done.".format(now)
    else:
        subject = "QSARModelingPy Update #{}: Running Genetic Algorithm".format(current_matrix)
        content += "\n\n[{}] Starting genetic algorithm in <code>{}</code>. Matrix {} of {}.".format(now, current_matrix_name, current_matrix,total_matrices)
    yag.send(to = to, subject = subject, contents = content, attachments = attachment)

if __name__== '__main__':
    dfConf = pd.read_csv("batch_confGA.csv",header=None)
    last_run_status = None
    last_run_cv = None
    total_matrices = dfConf.shape[1] - 1
    for runIndex in range(1, dfConf.shape[1]):
        sendMail(runIndex, dfConf[runIndex][1], total_matrices,last_run_status, last_run_cv)
        #print("\n\n******************************")
        #print("********Matrix {} of {}.********".format(runIndex, total_matrices))
        #print("******************************")
        #continue
        directory = dfConf[runIndex][0]
        xFile = dfConf[runIndex][1]
        yFile = dfConf[runIndex][2]
        var_cut = float(dfConf[runIndex][3])
        corr_cut = float(dfConf[runIndex][4])
        nLVModel = None if dfConf.isnull()[1][5] else int(dfConf[runIndex][5])
        min_size = int(dfConf[runIndex][6])
        max_size = int(dfConf[runIndex][7])
        size_population = int(dfConf[runIndex][8])
        mig_rate = float(dfConf[runIndex][9])
        cxpb = float(dfConf[runIndex][10])
        mutpb = float(dfConf[runIndex][11])
        ngen = int(dfConf[runIndex][12])
        yr_crit = float(dfConf[runIndex][13])
        lno_crit = float(dfConf[runIndex][14])
        out_directory = dfConf[runIndex][15]
        out_matrix = dfConf[runIndex][16]
        out_cv = dfConf[runIndex][17]
        Q2_file = dfConf[runIndex][18]
        var_sel_file = dfConf[runIndex][19]
        autoscale = dfConf[runIndex][20].upper() == "YES"
        df = pd.read_csv(directory+"/"+xFile,sep=';',index_col=0)
        dfX = lj.transform(df) if dfConf[runIndex][21].upper() == "YES" else df
        print("Dimensions of the original matrix")
        print(dfX.shape)
        y = pd.read_csv(directory+"/"+yFile,sep=';',header=None).values
        indVar = variance_cut(dfX.values,var_cut)
        dfVar = dfX.loc[:,dfX.columns[indVar]]
        print("Dimensions of the matrix after of the variance cut")
        print(dfVar.shape)
        indCorr = correlation_cut(dfVar.values,y,corr_cut)
        dfCorr = dfVar.loc[:,dfVar.columns[indCorr]]
        print("Dimensions of the matrix after of the correlation cut")
        print(dfCorr.shape)
        X = dfCorr.values
        if nLVModel == None:
            nLVModel = int(dfCorr.shape[0]/5)
        ga = Ga(X,y,nLVModel, autoscale, min_size, max_size, size_population, mig_rate, cxpb, mutpb, ngen)
        ga.run()
        ga.saveQ2(out_directory+"/"+Q2_file)
        ga.savePop(out_directory+"/"+var_sel_file)
        Q2 = ga.Q2
        Q2 = [Q2[i][0] for i,_ in enumerate(Q2)]
        var_sel = validate(X,y,ga.pop_selected,Q2,yr_cut=yr_crit,lno_cut=lno_crit)
        if var_sel != []:
            dfSel = dfCorr.loc[:,dfCorr.columns[var_sel]]
            dfSel.to_csv(out_directory+"/"+out_matrix,sep=';')
            cv = CrossValidation(dfSel.values,y)
            cv.saveParameters(out_directory+"/"+out_cv)      
            last_run_status = True
            last_run_cv = os.path.join(out_directory, out_cv)
        else:
            last_run_status = False
            last_run_cv = None
            print("y-randomization or LNO failed!")
    sendMail(0, 0, 0,last_run_status, last_run_cv, True)
