"""
File Name: delta_prime.py
Written by : Salm Jérémy, EPFL (jeremy.salm@epfl.ch)
Date Created: April 2024
"""
# Libraries
import numpy as np
from scipy.integrate import solve_bvp
import matplotlib.pyplot as plt
import sympy as sym

__all__ = ["delta_prime_solver"]

def delta_prime_solver(T, m, n, q_string):
    """  Parameters
          - T : ratio between the toroidal component and the major radius
          - m : number of poloidal Fourier modes
          - n : number of toroidal Fourier modes
          - q_string : q profile as a string variable
         Returns
          - delta_prime : stability of the input equilibrium

         Example : delta_prime_test = delta_prime_solver(T=1, m=2, n=1, q_string='1.2*(1+(r/0.81)**2)')
                   For more explicit example, SEE explicit_delta_prime_solver.ipynb
    """  

    # q profile as SymPy expression
    def q_sym(q_string, numerical=False):
        """  Parameters
          - q_string : string expression of q profile
          - numerical : if False, return SymPy expr, if True return associated numerical expr
         Returns
          - q_ : q profile as SymPy or numerical expr
        """  
        r, f_ = sym.symbols('r, f')
        q_ = sym.sympify(q_string)

        if(numerical==True):
            return sym.lambdify(r, q_) # q as numerical expression
        else:
            return q_ # q as SymPy expression
    
    #####################
    
    # Poloidal magnetic profile as SymPy expression
    def B_theta_sym(T_, q_):
        """ Parameters
            - T_ : ratio between the toroidal component and the major radius
            - q_ : q profile as SymPy (symbolic) expr
            Returns
            - B_theta_ : poloidal magnetic profile as SymPy or numerical expr
        """  
        r, f_ = sym.symbols('r, f')
        B_theta_string = (T_*r)/q_
        B_theta_ = sym.sympify(B_theta_string) # B_theta as SymPy expression

        return B_theta_
    
    #####################
    
    # dj_phi_dr as SymPy expression
    def dj_phi_dr_sym(B_theta_):
        """ Parameters
            - B_theta_ : ratio between the toroidal component and the major radius
            Returns
            - dj_phi_dr_sym, j_phi_sym : dj_phi_dr_sym, j_phi_sym as SymPy or numerical expr
        """ 
        r, f_ = sym.symbols('r, f')
        max_term = r*B_theta_ # from Maxwell equation
        max_term_sym = sym.sympify(max_term)
        j_phi_sym = sym.diff(max_term_sym)/r

        dj_phi_dr_sym = sym.diff(j_phi_sym, r) # dj_phi_dr as SymPy expression
    
        return dj_phi_dr_sym, j_phi_sym
    
    #####################

    # Factor in front of y_1 in the 2D system 
    def c_sym(q_, dj_phi_dr_, B_theta_):
        """ Compute the term in front of y_1 in the expression of y_2  
        Parameters
            - q_ : q profile as SymPy (symbolic) expr
            - dj_phi_dr_ : radial derivative of the current density profile as SymPy expr
        Returns
            -  : factor c as numerical expr
        """
        r, f_ = sym.symbols('r, f')
        c_str = (m**2/r**2)+dj_phi_dr_/((B_theta_)*(1-(n*q_)/m))
        c_ = sym.sympify(c_str)
        
        return sym.lambdify(r, c_) # c(r) as numerical expression
    
    #####################

    # Computing SymPy expressions with q profile input
    q_profile_sym = q_sym(q_string)
    q_profile_num = q_sym(q_string, numerical=True)
    B_theta_profile_sym = B_theta_sym(T, q_profile_sym)
    dj_phi_dr_profile_sym, j_phi_profile_sym = dj_phi_dr_sym(B_theta_profile_sym)
    c_num = c_sym(q_profile_sym, dj_phi_dr_profile_sym, B_theta_profile_sym)

    ##################### Creating functions in order to use scipy.integrate.solve_bvp()
    # system of ODE
    def fun(r, y):
        """  Parameters
            r : spatial mesh 
            y : y[0] contains y_1 and y[1] contains y_2  
            Returns
            dxdr : the system of first order ODE contained in sequence vertically
        """
        dxdr = np.vstack((y[1], c_num(r)*y[0]-y[1]/r))
        
        return dxdr
    
    # Boundary conditions for left part
    def bc_left(ya, yb): 
        """  Parameters
            x : ya[0] correspond to the value of the solution at the left boundary
            y : yb[0] correspond to the value of the solution at the right boundary  
            Returns
            bc_ : Gives the left boundary conditions
        """
        bc_ = np.array([ya[0], yb[0]-1]) # ensure that the solution is 0 at x=a and 1 at x=b
        return bc_
    
    # Boundary conditions for right part
    def bc_right(ya, yb):
        """  Parameters
            x : ya[0] correspond to the value of the solution at the left boundary
            y : yb[0] correspond to the value of the solution at the right boundary  
            Returns
            bc_ : Gives the right boundary conditions
        """
        bc_ = np.array([ya[0]-1, yb[0]]) # ensure that the solution is 1 at x=a and 0 at x=b
        return bc_
    
    # Space discretization
    def discretization(m_, n_, delta, a=0.01, b=1):
        """ Generate the left/right part of the interval, given the Fourier modes   
        Parameters
            - m_ : number of poloidal Fourier modes
            - n_ : number of toroidal Fourier modes
            - delta : spacing interval between points
            - a : interval initial point
            - b : interval final point
            Returns
            r_array_left, r_array_right, sol : interval on the left/right of the singularity & the r value of the singularity
        """
        def q_discr(r):
            return q_profile_num(r)-m_/n_ # will be used below in root_scalar()
        
        from scipy import optimize
        
        # Computing the r-value for which we have a singularity, i.e solving q(r) - m/n = 0
        comput_sol = optimize.root_scalar(q_discr, bracket=[a, b], method='brentq') 
        sol = comput_sol.root

        # print(sol)
        # Creating the left/right interval w.r.t the singularity 
        eps = 1e-8
        r_left=np.linspace(0.01, sol-eps, 100, endpoint=True)
        r_right=np.linspace(sol+eps, 1, 100, endpoint=True)

        #r_left = np.arange(0.01, sol+delta-eps, delta)
        #r_right = np.arange(sol+eps, 1, delta)

        return r_left, r_right, sol
    
    # Constructing the mesh on the left/right of the singularity
    r_array_left_, r_array_right_, sing = discretization(m, n, 1e-5)

    # Defining the intial guess for the solution
    y_left_ = np.random.rand(2, r_array_left_.size)
    y_right_ = np.random.rand(2, r_array_right_.size)

    # line
    y_left_[0] = (1/sing)*r_array_left_
    y_left_[1] = y_left_[0]

    y_right_[0] = (1/(sing-1))*r_array_right_+(1/(1-sing))*np.ones(r_array_right_.size)
    y_right_[1] = y_right_[0]

    # Solving for left & right sides
    sol_left_ = solve_bvp(fun, bc_left, r_array_left_, y_left_, max_nodes=1000)
    sol_right_ = solve_bvp(fun, bc_right, r_array_right_, y_right_, max_nodes=1000)

    # solution to be plotted
    sol_left_plot = sol_left_.sol(r_array_left_)[0]
    sol_right_plot = sol_right_.sol(r_array_right_)[0]

    # Computation of delta_prime
    delta_prime = (sol_right_.yp[0][0]-sol_left_.yp[0][-1])/sol_right_plot[0]
    
    return delta_prime
    

