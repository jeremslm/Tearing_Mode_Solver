# tm_solver
This git contains the package tm_solver allowing the use of the function delta_prime_solver() that gives the stability of resistive tearing modes $\Delta'$. 
In order to use it, write on your terminal the following steps :
1. git clone https://github.com/jeremslm/Tearing_Mode_Solver.git
2. cd Tearing_Mode_Solver
3. pip install . 

Here is a sketch of how to use this function. 

```
import tm_solver.solver as solver
f = solver.delta_prime_solver

# function parameters
T = 5 # ratio between the toroidal component and the major radius
m = 2 # number of poloidal Fourier modes
n = 1 # number of toroidal Fourier modes
q = '1.2*(1+(r/0.81)**2)' # q profile

# Computing delta_prime
delta_prime = f(T, m, n, q) 
```

$\textbf{EXAMPLE 1}$

Let's consider a family of equilibria with a $q$ profile having the shape 

$q(r) = q_{0}\left[1+\left(\frac{r}{r_{0}}\right)^{2}\right]$, with $r_{0}=0.81$ and $q_{0}\in\[0.9, 1.6\]$

Then, by computing $\Delta'$ for a range of $q_{0}$, it's possible get the stable & unstable regimes 

![stability_regime](https://github.com/jeremslm/Tearing_Mode_Solver/assets/130314261/ee483fd4-31e7-452e-ad91-2d17e605e51c)

$\textbf{EXAMPLE 2}$

By taking the same shape of $q$ profile as above, but now with a fixed $q_{0} = 1.2$ and by considering a range $r_{0}\in\[0.2, 1.2\]$, the stable & unstable regimes can be observed

![stability_regime_2](https://github.com/jeremslm/Tearing_Mode_Solver/assets/130314261/4de99892-6ffe-4b43-9f83-cbb1f0716aaf)



