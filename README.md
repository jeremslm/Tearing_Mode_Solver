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



$\textbf{EXAMPLE 1}$

In this example, the goal is to reproduce *Figure 3* of [1]. Let's consider a family of equilibria with a $q$ profile having the shape 

$q(r) = q_{0}\left[1+\left(\frac{r}{r_{0}}\right)^{2}\right]$, with $r_{0}=0.81$ and $q_{0}\in\[0.9, 1.6\]$

Then, by computing $\Delta'$ for a range of $q_{0}$, it's possible get the stable & unstable regimes 

![stability_regime](https://github.com/jeremslm/Tearing_Mode_Solver/assets/130314261/ee483fd4-31e7-452e-ad91-2d17e605e51c)

Here is the sketch to obtain the above plot

```
# Global parameters
T = 5 # ratio between the toroidal component and the major radius (see the def of q)
m = 2 # number of poloidal Fourier modes
n = 1 # number of toroidal Fourier modes
r_0 = 0.8164965809277261

# Creating the q_0 coeff as string in order to use delta_prime_solver() for each one
q_0_list = np.linspace(0.9, 1.6, 20)
q_0_list_str = [str(num) for num in q_0_list]

# Creating all q profile with the q_0s
q_profile_str_q_0 = []

for i in range(len(q_0_list_str)):
    q_profile_str_q_0.append(q_0_list_str[i]+'*(1+(r/0.81)**2)')

# Computing the delta_prime for each q profile
delta_primes_q_0 = []

for i in range(len(q_profile_str_q_0)):
    delta_primes_q_0.append(delta_prime_solver(T, m, n, q_profile_str_q_0[i]))

# We convert into array in order to multiply it by r_0 and have a unitless quantity plotted
delta_primes_q_0 = np.array(delta_primes_q_0)

# Plotting the delta_prime*r_0 as a function of q_0
plt.plot(q_0_list, delta_primes_q_0*r_0)
plt.axhline(0, linestyle='--', color='red')
plt.xlabel(r'$q_{0}$', fontsize=14)
plt.ylabel(r"$r_{0}\Delta'$", fontsize=14)
plt.xlim(0.9, 1.6)
plt.ylim(-15, 18)

```

[1] J. Loizu, D. Bonfiglio, *Nonlinear saturation of resistive tearing modes in a cylindrical tokamak with and without solving the dynamic*, J. Plasma Phys. (2023), vol. 89, 905890507, https://doi.org/10.1017/S0022377823000934

$\textbf{EXAMPLE 2}$

By taking the same shape of $q$ profile as above, but now with a fixed $q_{0} = 1.2$ and by considering a range $r_{0}\in\[0.2, 1.2\]$, the stable & unstable regimes can be observed

![stability_regime_2](https://github.com/jeremslm/Tearing_Mode_Solver/assets/130314261/4de99892-6ffe-4b43-9f83-cbb1f0716aaf)

Here is the sketch to obtain the above plot

```
# Global parameters
T = 5 # ratio between the toroidal component and the major radius (see the def of q)
m = 2 # number of poloidal Fourier modes
n = 1 # number of toroidal Fourier modes
q_0 = '1.2'

# Creating the r_0 coeff as string in order to use delta_prime_solver() for each one
r_0_list = np.linspace(0.2, 1.2, 100)
r_0_list_str = [str(num) for num in r_0_list]

# Creating all q profile with the r_0s
q_profile_str_r_0 = []

for i in range(len(r_0_list_str)):
    q_profile_str_r_0.append(q_0+'*(1+(r/'+r_0_list_str[i]+')**2)')

# Computing the delta_prime for each q profile
delta_primes_r_0 = []

for i in range(len(q_profile_str_r_0)):
    delta_primes_r_0.append(delta_prime_solver(T, m, n, q_profile_str_r_0[i]))

# Plotting the delta_prime  as a function of r_0
plt.plot(r_0_list, delta_primes_r_0)
plt.axhline(0, linestyle='--', color='red')
plt.xlabel(r'$r_{0}$', fontsize=14)
plt.ylabel(r"$\Delta'$", fontsize=14)
```

