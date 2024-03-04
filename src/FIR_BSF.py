# Created by Shahrokh Hamidi
# PhD., Electrical & Computer Engineering, University of Waterloo
# Waterloo, ON., Canada




import numpy as np 
import matplotlib.pyplot as plt
import sys
import cvxpy as cp
import matplotlib
import warnings
warnings.filterwarnings('ignore')



#%matplotlib qt


class Params:
    
    
    N  = 256
    Fs = 40
    fs1 = 4/Fs
    fs2 = 7/Fs
    fp1 = 2/Fs
    fp2 = 9/Fs
    filter_order = 15
    delta = 0.5
    freq = np.linspace(0,1,N)
    def __init__(self):
        
        pass

        
       
    
    
    
class  Opt(Params):
    
    def __init__(self):
        
        super(Opt, self).__init__()
        self.utils()
    
    
    def utils(self):
        
        A = 2*np.cos(2*np.pi*Params.freq.reshape(-1,1)*np.arange(0,Params.filter_order))
        index_s = np.where(((Params.fs1<Params.freq) & (Params.freq<Params.fs2)))[0].tolist()
        index_p1 = np.where(((0<Params.freq) & (Params.freq<Params.fp1)))[0].tolist()
        index_p2 = np.where(((Params.fp2<Params.freq) & (Params.freq<1/2.)))[0].tolist()
        index_p = np.hstack((index_p1, index_p2))
        A[:,0] = 1
        self.Ap = A[index_p,:]  
        self.As = A[index_s,:] 

        
        
    def _cost(self, hp):
        
        cost = cp.max(cp.abs(self.As@hp))
        return cost
    
    def _constr(self, hp):
        
        constr = []
        constr += [10**(-Params.delta/20) <= self.Ap @ hp]
        constr += [self.Ap @ hp  <=  10**(Params.delta/20)]
        
        return constr
    
    
    def _run(self):

        hp = cp.Variable(Params.filter_order)    
        prob = cp.Problem(cp.Minimize(self._cost(hp)), self._constr(hp))
        prob.solve()
        
        return hp.value

    
class Filter(Params):
    
    def __init__(self):
        pass
    
    
    @staticmethod
    def impulse_response(h):
        
        h = np.hstack((h[:0:-1], h))
        
        return Filter.frequency_response(h)
    
    def frequency_response(h):
        
        H = np.fft.fft(h, Params.N)
        
        return h, H
    
    
     
class Display:
    
    
    def __init__(self, H, h, msg):
    
        self.msg = msg
        self.display_IPR(h)
        self.display_IPR_H(H)
        self.display_phase(H)
        
    def display_IPR(self, h):
        
        plt.figure()
        plt.stem(h)
        plt.plot(h, 'r--')
        plt.grid()
        plt.xlabel('$Samples$', fontsize = 16)
        plt.ylabel('$IPR$', fontsize = 16)
        matplotlib.rc('font', size=16)
        matplotlib.rc('axes', titlesize = 16)
        #plt.rcParams['figure.dpi'] = 300
        #plt.rcParams['savefig.dpi'] = 300
        plt.title(f'$FIR\;\;{msg}\; Pass\; Filter, \;\;\;\; n = {Params.filter_order}$')
        #plt.savefig('FIR_LPF.png')
        plt.tight_layout()
        plt.show()
        
    def display_IPR_H(self, H):
    
        H = abs(H)
        plt.figure()
        plt.plot(Params.freq*Params.Fs, 20*np.log10(H), 'k', lw = 3)
        #plt.plot(Params.freq*Params.Fs, 0.5*np.ones(len(H)), 'r--', lw = 1)
        #plt.plot(Params.freq*Params.Fs, -0.5*np.ones(len(H)), 'r--', lw = 1)
        plt.grid()
        plt.xlabel('$Frequency\;\; [Hz]$', fontsize = 16)
        plt.ylabel('$20\;log\;|H(f)|\;\;[dB]$', fontsize = 16)
        matplotlib.rc('font', size=16)
        matplotlib.rc('axes', titlesize = 16)
        #plt.rcParams['figure.dpi'] = 300
        #plt.rcParams['savefig.dpi'] = 300
        plt.title(f'$FIR\;\;{msg}\; Pass\; Filter, \;\;\;\; n = {Params.filter_order}$')
        plt.xlim(0,Params.Fs//2)
        #plt.savefig('FIR_LPF.png')
        plt.tight_layout()
        plt.show()
        
        
    
    def display_phase(self, H):
    
        plt.figure()
        plt.plot(Params.freq*Params.Fs, np.unwrap(np.angle(H)), 'k', lw = 3)
        #plt.plot(Params.freq*Params.Fs, 0.5*np.ones(len(H)), 'r--', lw = 1)
        #plt.plot(Params.freq*Params.Fs, -0.5*np.ones(len(H)), 'r--', lw = 1)
        plt.grid()
        plt.xlabel('$Frequency\;\; [Hz]$', fontsize = 16)
        plt.ylabel('$Phase\;\;[rad]$', fontsize = 16)
        matplotlib.rc('font', size=16)
        matplotlib.rc('axes', titlesize = 16)
        #plt.rcParams['figure.dpi'] = 300
        #plt.rcParams['savefig.dpi'] = 300
        plt.title(f'$FIR\;\;{self.msg}\; Pass\; Filter, \;\;\;\; n = {Params.filter_order}$')
        plt.xlim(0,Params.Fs//2)
        #plt.savefig('FIR_LPF.png')
        plt.tight_layout()
        plt.show()
    
    
    
    
if __name__ == '__main__':

    msg = 'Band-Stop'
    Params()
    opt = Opt()
    h = opt._run()
    h, H = Filter.impulse_response(h)
    
    Display(H, h, msg)