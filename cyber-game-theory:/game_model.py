import numpy as np
from scipy.optimize import linprog
DEFAULT_ATTACKS=["Web server targeting","Phishing attempt","Denial of service"]
DEFAULT_DEFENSES=["Firewall","Multi-factor authentication","Monitoring"]
DEFAULT_PAYOFF=np.array([[-2,4,1],[5,-3,2],[3,2,-4]],dtype=float)
def solve_zero_sum_game(payoff):
    A=np.asarray(payoff,dtype=float)
    if A.ndim!=2 or not np.isfinite(A).all(): raise ValueError("payoff must be a finite 2D matrix")
    shift=max(0.0,1.0-float(A.min())); B=A+shift; m,n=B.shape
    ar=linprog(-np.ones(m),A_ub=B.T,b_ub=np.ones(n),bounds=[(0,None)]*m,method="highs")
    if not ar.success: raise RuntimeError(ar.message)
    x=ar.x; p=x/x.sum(); value=1.0/x.sum()-shift
    dr=linprog(np.ones(n),A_ub=-B,b_ub=-np.ones(m),bounds=[(0,None)]*n,method="highs")
    if not dr.success: raise RuntimeError(dr.message)
    y=dr.x; q=y/y.sum()
    return {"p":p,"q":q,"value":float(value)}
def pure_saddle_point(payoff,tol=1e-9):
    A=np.asarray(payoff,dtype=float); rowmins=A.min(axis=1); colmaxs=A.max(axis=0)
    lo=rowmins.max(); hi=colmaxs.min()
    if abs(lo-hi)<=tol:
        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                if abs(A[i,j]-lo)<=tol and abs(rowmins[i]-lo)<=tol and abs(colmaxs[j]-hi)<=tol:return int(i),int(j),float(A[i,j])
    return None
