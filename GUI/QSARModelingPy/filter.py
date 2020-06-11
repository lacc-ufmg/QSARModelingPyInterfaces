import numpy as np
import pandas as pd
from sklearn.preprocessing import scale as autoscale

def variance_cut(X,cut):
    v = np.var(X,0,ddof=1)
    indCut = [i for i in range(len(v)) if v[i] >= cut]
    return indCut

def autoscale1(X):
    m,n = np.shape(X)
    means = np.mean(X,0)
    stds = np.std(X,0,ddof=1)
    #stds = [x for x in stds if x!=0 else float("inf")]
    Xm = X-np.ones((m,1))*means
    Xa = np.divide(Xm,np.ones((m,1)))
    return Xa

def correlation_cut(X,y,cut):
    corr = abs(np.dot(np.transpose(autoscale(X)),autoscale(y))/(len(y)-1))
    indCut = [i for i in range(len(corr)) if corr[i] >= cut]
    return indCut

def autocorrelation_cut(X,y,cut):
    # Xcorr = (1/(X.shape[0]))*autoscale(X).T.dot(autoscale(X))
    Xcorr = np.corrcoef(X.T)
    m,n = X.shape
    var_filtered = []
    for i in range(n):
        for j in range(i+1,n):
            # corr = (1/m)*autoscale(X[:,i]).T.dot(autoscale(X[:,j]))
            corr = Xcorr[i,j]
            if corr > cut:
                corr_i = abs(np.dot(np.transpose(autoscale(X[:,i])),autoscale(y))/(m-1))
                corr_j = abs(np.dot(np.transpose(autoscale(X[:,j])),autoscale(y))/(m-1))
                if corr_i < corr_j:
                    if i not in var_filtered:
                        var_filtered.append(i)
                else:
                    if j not in var_filtered:
                        var_filtered.append(j)
    var = [i for i in range(n) if i not in var_filtered]
    return var