# Importing libraries
import numpy as np
import pandas as pd
from validacao_externa import ExternalValidation
from cross_validation_class import CrossValidation
from kennardstonealgorithm import kennardstonealgorithm
import lj_cut as lj
import os

if __name__=='__main__':
	# Open configuration file in order to look for the matrices and the parameters to run
	# external validation
	dfConf = pd.read_csv("/home/helitonmrf/OneDrive/Documentos/QSAR/Amostragem por Fecho Convexo/Descritores 4D/matrizes_C_LJ/confExtVal.csv",header=None)
	for runIndex in range(1, dfConf.shape[1]):
		print("Starting external validation {} of {}.".format(runIndex, (dfConf.shape[1]-1)))
		directory = dfConf[runIndex][0]
		Xfile = dfConf[runIndex][1]
		yfile = dfConf[runIndex][2]
		nLV = None if dfConf.isnull()[1][4] else int(dfConf[runIndex][4])
		out_directory = dfConf[runIndex][5]
		ext_val_file = dfConf[runIndex][6]
		cv_file = dfConf[runIndex][7]
		Xtrain_file = dfConf[runIndex][8]
		ytrain_file = dfConf[runIndex][9]
		Xtest_file = dfConf[runIndex][10]
		ytest_file = dfConf[runIndex][11]
		autoscale = dfConf[runIndex][12].upper() == "YES"
		y = pd.read_csv(os.path.join(directory,yfile),sep=';',header=None).values
		dfX = pd.read_csv(os.path.join(directory,Xfile),sep=';',index_col=0)
		dfX = lj.transform(dfX) if dfConf[runIndex][13].upper() == "YES" else dfX
		X = dfX.values
		type_ext_val = int(dfConf[runIndex][14])
		if type_ext_val == 1: # manual selection
			test_set = dfConf[runIndex][3]
			test = [int(i)-1 for i in test_set.split(',')]
			train = [j for j in range(len(y)) if j not in test]
		elif type_ext_val == 2: # Kennard-Stone
			size_test_set = int(dfConf[runIndex][3])
			train,test = kennardstonealgorithm(dfX,len(dfX)-size_test_set) # parameter is the size of training set
		else: # Random selection    
			pass
		ext = ExternalValidation(X,y,nLV)
		ext.extVal(train,test,nLV)
		ext.saveExtVal(train,test,out_directory+"/"+ext_val_file)
		cv = CrossValidation(X[train,:],y[train],nLVMax = nLV,scale=True)
		cv.saveParameters(os.path.join(out_directory,cv_file))
		dfXtrain = dfX.loc[dfX.index[train],dfX.columns]
		dfXtrain.to_csv(os.path.join(out_directory,Xtrain_file), sep =';')
		dfytrain = pd.DataFrame(y[train])
		dfytrain.to_csv(os.path.join(out_directory,ytrain_file), sep =',', header=False)
		dfXtest = dfX.loc[dfX.index[test],dfX.columns]
		dfXtest.to_csv(os.path.join(out_directory,Xtest_file), sep =';')
		dfytest = pd.DataFrame(y[test])
		dfytest.to_csv(os.path.join(out_directory,ytest_file), sep =',', header=False)