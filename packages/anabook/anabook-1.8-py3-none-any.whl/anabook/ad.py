
import numpy as np

def mTratamientoAnomalias(df, dfx,campo):
    import scipy.stats as stats

    dfx['Flag'] = 0
    dfx['Z']=0.00
    dfx['Anom'] = 0
    nMean = 0.00
    nArray = stats.zscore(dfx[campo])
    dfx['Z'] = nArray
    # Se asumen normalidad de la variable
    # Aqui PARAMETRO
    dfx.loc[((abs(dfx['Z']) -3.0)>=1.5), 'Anom'] = 1
    nMean = np.mean(dfx[dfx.Anom==0][campo])
    dfx.loc[dfx['Anom'] == 1, campo] = nMean * 1.0
    df[campo] = dfx[campo]
    #---------------------
    mCalculaOutliersPorciento(dfx,campo)
    mImputaConMedia(df, dfx,campo)


def mCalculaOutliersPorciento(dfx,campo):

  Q1 = dfx.quantile(0.25)
  Q3 = dfx.quantile(0.75)
  IQR = Q3-Q1

  outlInferior = Q1 - 1.5 * IQR
  outlSuperior = Q3 + 1.5 *IQR

  dfx['Flag'] = 0
  dfx['Flag'] = np.where(((dfx[campo] < outlInferior[0]) | (dfx[campo] > outlSuperior[0])), 1,0)

  # Esta m�trica es referencial, ya que en el tratamiento de datos an�malos
  # se asume normalidad de la variable
  outlPorcien = len(dfx[(dfx.Flag==1)])/ len(dfx)
  return outlPorcien

def mImputaConMedia(df, dfx,campo):
    # nMean = np.mean(dfx[dfx.Flag==0][campo])
    nMean = np.mean(df[campo])
    dfx.loc[dfx['Flag'] == 1, campo] = nMean * 1.0
    df[campo] = dfx[campo]

def mTratamientoDeOutliers(df, dfx,campo):
  outlPorcien = mCalculaOutliersPorciento(dfx,campo)
  if (outlPorcien < 0.10):
    mImputaConMedia(df, dfx,campo)
    
