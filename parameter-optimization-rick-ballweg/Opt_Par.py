# -*- coding: utf-8 -*-
"""
Modified by Tongli on June 24 2019
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy import zeros_like
import glob
import os
from scipy.interpolate import interp1d
from scipy import optimize

def IntegrateModel(par,initial_cond,t):
	def ODEmodel(t,y):
		[CCT, ProSD, CDR, SurF,Resis,K,DCT] = par
		ode = zeros_like(y)
		S =y[0]
		R =y[1]
		D =y[2]
		k1=0.693/CCT
		k2=0.5*ProSD*k1
		k3=CDR*k2
		k4=0.5*ProSD*k1+(1-ProSD)*k1
		k5=0.693/DCT
    		
		###Define ODEs###
		ode[0]= k1*S*(1-(S+R)/K) + k2*R - k3*S
		ode[1]= k4*R*(1-(S+R)/K) - k2*R + k3*S
		ode[2]= -k5*D
		return ode

	TimeSeries = solve_ivp(ODEmodel,t,initial_cond,t_eval = np.arange(0,1,0.01),method = 'BDF')#integrate.odeint(funct,initial_cond,t) ##
	return (TimeSeries)
    ### here ends the integration definition 


def Treatment(Stanpar,Stanic,StanTimeLength):
  Stanall_data = np.empty((1,len(Stanic)))
  Stantimes =  np.array([])

  for StanDay in range (1,49):
      if StanDay == 1:
          Stanic[0] = 1- Stanpar[2]
          Stanic[1] = Stanpar[2]
      
      StanTS=IntegrateModel(Stanpar,Stanic,StanTimeLength)
      ### tumor growth simulation 
      StanEndDayState = StanTS.y[:,-1]
      StanSurF=Stanpar[3]
      Resis=Stanpar[4]
      ### RT or not 
      if np.any(Standays_off == StanDay) == False:
          StanEndDayState[0]=StanEndDayState[0]*StanSurF
          StanEndDayState[1]=StanEndDayState[1]*(1-Resis*(1-StanSurF))
          StanEndDayState[2]=StanEndDayState[2]+StanEndDayState[0]*(1-StanSurF)+StanEndDayState[1]*Resis*(1-StanSurF)
##          print('on'+ str(Day))
          
      Stanic = StanEndDayState
      Stanall_data = np.vstack((Stanall_data,np.transpose(StanTS.y)))
      Stantimes = np.append(Stantimes,StanTS.t+StanDay-1)
  Stanall_data = Stanall_data[1:len(Stanall_data),:]
  return(np.hstack((Stantimes.reshape((len(Stantimes),1)),Stanall_data)))

def score_opt(Bpar):
    SimData = Treatment(Bpar,ic,TimeLength)
    idx=np.unique(SimData[:,0],return_index = True)
    idx = idx[1]
    SimData = SimData[idx,:]
    spline = interp1d(SimData[:,0],np.sum(SimData[:,1:4],axis = 1),kind = 'cubic')
    score = np.sum((spline(train[:,0]) - (train[:,1]))**2) 
    return(score)


data = np.genfromtxt('HN09_data_2.txt')
data[:,1] = data[:,1]/np.max(data[:,1])
train = np.array_split(data,2)[0]
val = np.array_split(data,2)[1]

Standays_off = np.array([6,7,13,14,20,21,27,28,34,35,41,42,48,49])
Parnumber=7
VPpars = np.empty((1,Parnumber))

plt.figure(figsize = (7,5),dpi = 300)

bounds = ((1,10),(0,1),(0,0.2),(0.1,1),(0,0.5),(0,10),(0,10))


n = 5
ic =[1,0,0]
TimeLength =(0,1)
sims = np.zeros((4800,n))
opt_pars = np.zeros((n,len(bounds) + 1))
for i in range(0,n):
    res = optimize.differential_evolution(score_opt,bounds,disp = True,tol = 1e-6,maxiter = 5, popsize =1,polish = False)    
    SimData = Treatment(res.x,ic,TimeLength)
    print (SimData.shape)
    TumorSize=np.sum(SimData[:,1:4],axis = 1)
    sims[:,i] = TumorSize
    opt_pars[i,0] = res.fun
    opt_pars[i,1:len(bounds)+1] = res.x

plt.fill_between(SimData[:,0], np.mean(sims,axis = 1) - np.std(sims,axis = 1),np.mean(sims,axis = 1) + np.std(sims,axis = 1),color = 'b',alpha = 0.5,label = '+/- Std')
plt.plot(SimData[:,0], np.mean(sims,axis = 1),'b',label = 'Mean')        
plt.plot(train[:,0],train[:,1],'ro',mec = 'k',label = 'Train')
plt.plot(val[:,0],val[:,1],'go',mec = 'k',label = 'Val')
plt.legend()

plt.xlabel('Days')
plt.ylabel('Tumor Size')
plt.title('HN09')

#plt.ylim(0, 12)
plt.legend()
plt.savefig('HN09_Local_In.png')

np.savetxt('Opt_pars.txt',opt_pars)

    
