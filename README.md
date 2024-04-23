# tm_solver
This git contains the package tm_solver allowing the use of the function delta_prime_solver() that gives the stability of resistive tearing modes $\Delta'$. 
In order to use it, write on your terminal the following steps :
1. [Copy the gitclone link in your terminal](https://github.com/jeremslm/Tearing_Mode_Solver.git)
2. cd Tearing/Mode/Solver
3. pip install . 

Here is an example of how to use this function. 

```
import tm_solver.solver as solver
f = solver.delta_prime_solver

# function parameters
T = 5 # ratio between the toroidal component and the major radius (see the def of q)
m = 2 # number of poloidal Fourier modes
n = 1 # number of toroidal Fourier modes
q = '1.2*(1+(r/0.81)**2)' # q profile

# Computing delta_prime
delta_prime = f(T, m, n, q) 
```
