from sklearn.model_selection import LeaveOneOut
from sklearn.cross_decomposition import PLSRegression
import numpy as np
import pandas as pd
from math import sqrt
from sklearn.preprocessing import scale
from calculate_parameters import calcPress, calcR2, calcRMSE, calcR
from plsbdg import PLSBidiag

# def ssy(y):
# 	ssy = sum((y-np.mean(y)*np.ones(np.shape(y)))**2)
# 	return ssy

# def calcPress(yreal,ypred):
# 	press = sum((yreal-ypred)**2)
# 	return press

# def calcR2(yreal,ypred):
# 	ssy1 = ssy(yreal)
# 	R2 = 1-(calcPress(yreal,ypred)/ssy1)
# 	return R2

# def calcRMSE(yreal,ypred):
# 	RMSE = sqrt(calcPress(yreal,ypred)/len(yreal))
# 	return RMSE

# def calcR(yreal,ypred):
# 	r = np.dot(scale(yreal),scale(ypred))/(len(yreal))
# 	return r

class CrossValidation(object):

	def __init__(self,X,y,nLVMax = None,scale=True):
		self.X = X
		self.y = y
		if nLVMax == None:
			self.nLVMax = int(len(y)/5)
		else:
			self.nLVMax = nLVMax
		nLVMax = self.nLVMax
		#cross_validation
		ycv = np.zeros((len(y),nLVMax))
		loo = LeaveOneOut()
		for train, test in loo.split(X):
			pls = PLSBidiag(n_components=nLVMax)
			pls.fit(X[train,:],y[train])
			ycv[test,:] = pls.predict(X[test])

		# calibration
		ycal = np.zeros((len(y),nLVMax))
		pls = PLSBidiag(n_components=nLVMax)
		pls.fit(X,y)
		#ycal[:,i-1] = np.reshape(pls.predict(X),len(y))
		ycal = pls.predict(X)

		self.ycv = ycv
		self.ycal = ycal

	def press(self):
		return [calcPress(self.y[:,0],self.ycal[:,i]) for i in range(self.nLVMax)]

	def R2(self):
		return [calcR2(self.y[:,0],self.ycal[:,i]) for i in range(self.nLVMax)]

	def RMSEC(self):	
		return [calcRMSE(self.y[:,0],self.ycal[:,i]) for i in range(self.nLVMax)]

	def rcal(self):
		return [calcR(self.y[:,0],self.ycal[:,i]) for i in range(self.nLVMax)]

	def presscv(self):
		return [calcPress(self.y[:,0],self.ycv[:,i]) for i in range(self.nLVMax)]

	def Q2(self):
		return [calcR2(self.y[:,0],self.ycv[:,i]) for i in range(self.nLVMax)]

	def RMSECV(self):
		return [calcRMSE(self.y[:,0],self.ycv[:,i]) for i in range(self.nLVMax)]

	def rcv(self):
		return [calcR(self.y[:,0],self.ycv[:,i]) for i in range(self.nLVMax)]

	def returnParameters(self,nLV = None):
		if nLV == None:
			nLV = np.argmax(self.Q2())+1		
		press_value = calcPress(self.y[:,0],self.ycal[:,nLV-1])
		R2_value = calcR2(self.y[:,0],self.ycal[:,nLV-1])
		RMSEC_value = calcRMSE(self.y[:,0],self.ycal[:,nLV-1])
		rcal_value = calcR(self.y[:,0],self.ycal[:,nLV-1])
		presscv_value = calcPress(self.y[:,0],self.ycv[:,nLV-1])
		Q2_value = calcR2(self.y[:,0],self.ycv[:,nLV-1])
		RMSECV_value = calcRMSE(self.y[:,0],self.ycv[:,nLV-1])
		rcv_value = calcR(self.y[:,0],self.ycv[:,nLV-1])
		scaledy = (self.y[:,0]-min(self.y[:,0]))/(max(self.y[:,0])-min(self.y[:,0]))
		scaledycal = (self.ycal[:,nLV-1]-min(self.y[:,0]))/(max(self.y[:,0])-min(self.y[:,0]))
		scaled_k = sum(scaledy*scaledycal)/sum(scaledycal**2)
		scaled_k1 = sum(scaledy*scaledycal)/sum(scaledy**2)
		scaled_yr0 = scaled_k*scaledycal
		scaled_y1r0 = scaled_k1*scaledy
		scaled_R02 = calcR2(scaledy,scaled_yr0)
		scaled_R102 = calcR2(scaledycal,scaled_y1r0)
		r2cal = (calcR(np.reshape(scaledy,len(scaledy),1),np.reshape(scaledycal,len(scaledy),1)))**2
		rm2 = r2cal*(1-sqrt(abs(r2cal-scaled_R02)))
		rm12 = r2cal*(1-sqrt(abs(r2cal-scaled_R102)))
		avgrmcal = (rm2+rm12)/2
		deltarmcal = abs(rm2-rm12)		
		scaledycv = (self.ycv[:,nLV-1]-min(self.y[:,0]))/(max(self.y[:,0])-min(self.y[:,0]))
		scaled_k = sum(scaledy*scaledycv)/sum(scaledycv**2)
		scaled_k1 = sum(scaledy*scaledycv)/sum(scaledy**2)
		scaled_yr0 = scaled_k*scaledycv
		scaled_y1r0 = scaled_k1*scaledy
		scaled_R02 = calcR2(scaledy,scaled_yr0)
		scaled_R102 = calcR2(scaledycv,scaled_y1r0)
		r2cv = (calcR(np.reshape(scaledy,len(scaledy),1),np.reshape(scaledycv,len(scaledy),1)))**2
		rm2 = r2cv*(1-sqrt(abs(r2cv-scaled_R02)))
		rm12 = r2cv*(1-sqrt(abs(r2cv-scaled_R102)))
		avgrmcv = (rm2+rm12)/2
		deltarmcv = abs(rm2-rm12)		
		F = (np.shape(self.X)[0]-nLV-1)*R2_value/(nLV*(1-R2_value))	
		param = [press_value,R2_value,RMSEC_value,rcal_value,avgrmcal,deltarmcal,presscv_value,Q2_value,
		RMSECV_value,rcv_value,avgrmcv,deltarmcv,F,nLV]
		dfcv = pd.DataFrame(index = ["PRESS","R2","RMSEC","rcal","avgRmcal","deltaRmcal","PRESSCV","Q2",
			"RMSECV","rcv","avgRmcv","deltaRmcv","F","nLV"],
			data=np.array(param))
		return dfcv

	def saveParameters(self,fileName,nLV = None):
		df = self.returnParameters(nLV)
		df.to_csv(fileName, sep =',', header=False)