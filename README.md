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

$\textbf{Definition}$

Recall that $\Delta'$ is obtained thanks to the perturbed flux function and its radial derivative, $\psi$ & $\psi'$. It reads 

$\Delta' = \lim_{\epsilon \to 0^{+}} \frac{\psi'(r_{s}+\epsilon)-\psi'(r_{s}-\epsilon)}{\psi(r_{s})}$

where $r_{s}$ is the resonant surface.

$\textbf{PERTURBED FLUX FUNCTION SOLVING}$

The code that perform this plot can be found in the file "perturbed_flux_function.ipynb", in the folder "examples".

As shown above, $\Delta'$ depends on the perturbed flux function and its radial derivative, $\psi$ & $\psi'$. $\psi$ can be computed numerically by solving the differential equation given by 

$\frac{1}{r}\frac{d}{dr}(r\frac{d\psi}{dr})-\frac{m^{2}}{r^{2}}\psi-\frac{dj_{\phi}/dr}{\frac{B_{\theta}}{\mu_{0}}(1-\frac{nq}{m})}\psi=0$

Using the following inputs :

```
# Global parameters
T = 1 # ratio between the toroidal component and the major radius (see the def of q)
m = 2 # number of poloidal Fourier modes
n = 1 # number of toroidal Fourier modes

# q parameters
q_0 = 1.2
r_0 = 0.8164965809277261
r_mesh = np.linspace(0.01, 1, 2000)

```
and with the $q$ profile given by $q(r) = q_{0}\left[1+\left(\frac{r}{r_{0}}\right)^{2}\right]$, the solution $\psi(r)$ has the form in the below plot


![perturbed_flux_function](https://github.com/jeremslm/Tearing_Mode_Solver/assets/130314261/c7cfd189-4727-42c9-b3c7-3eb68a1b7e72)


$\textbf{EXAMPLE 1}$

The code that perform this plot can be found in the file "example_1.ipynb", in the folder "examples".

In this example, the goal is to reproduce *Figure 3* of [1]. Let's consider a family of equilibria with a $q$ profile having the shape 

$q(r) = q_{0}\left[1+\left(\frac{r}{r_{0}}\right)^{2}\right]$, with $r_{0}=0.81$ and $q_{0}\in\[0.9, 1.6\]$

Then, by computing $\Delta'$ for a range of $q_{0}$, it's possible get the stable & unstable regimes 

![stability_regime](https://github.com/jeremslm/Tearing_Mode_Solver/assets/130314261/ee483fd4-31e7-452e-ad91-2d17e605e51c)

[1] J. Loizu, D. Bonfiglio, *Nonlinear saturation of resistive tearing modes in a cylindrical tokamak with and without solving the dynamic*, J. Plasma Phys. (2023), vol. 89, 905890507, https://doi.org/10.1017/S0022377823000934

$\textbf{EXAMPLE 2}$

The code that perform this plot can be found in the file "example_2.ipynb", in the folder "examples".

By taking the same shape of $q$ profile as above, but now with a fixed $q_{0} = 1.2$ and by considering a range $r_{0}\in\[0.2, 1.2\]$, the stable & unstable regimes can be observed

![stability_regime_2](https://github.com/jeremslm/Tearing_Mode_Solver/assets/130314261/4de99892-6ffe-4b43-9f83-cbb1f0716aaf)

