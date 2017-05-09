r"""
Solve biharmonic equation in 1D

    u'''' + a*u'' + b*u = f,

Use Shen's Biharmonic basis.

"""
import sys
import importlib
from sympy import symbols, cos, sin, exp, lambdify
import numpy as np
import matplotlib.pyplot as plt
from shenfun import inner, Dx, TestFunction, TrialFunction

# Collect basis and solver from either Chebyshev or Legendre submodules
basis = sys.argv[-1] if len(sys.argv) == 2 else 'chebyshev'
shen = importlib.import_module('.'.join(('shenfun', basis)))
Basis = shen.bases.ShenBiharmonicBasis
Solver = shen.la.Biharmonic

# Use sympy to compute a rhs, given an analytical solution
x = symbols("x")
ue = sin(np.pi*x)*(1-x**2)

k = 8
nu = 1./590.
dt = 5e-5
a = -(k**2+nu*dt/2*k**4)
b = 1.0
c = -nu*dt/2.
fe = a*ue.diff(x, 4) + b*ue.diff(x, 2) + c*ue

# Lambdify for faster evaluation
ul = lambdify(x, ue, 'numpy')
fl = lambdify(x, fe, 'numpy')

# Size of discretization
N = 32

SD = Basis(N, plan=True)
X = SD.mesh(N)
u = TrialFunction(SD)
v = TestFunction(SD)

# Get f on quad points
fj = fl(X)

# Compute right hand side of biharmonic equation
f_hat = inner(v, fj)

# Get left hand side of biharmonic equation (no integration by parts)
S = inner(v, Dx(u, 0, 4))
A = inner(v, Dx(u, 0, 2))
B = inner(v, u)

# Create linear algebra solver
H = Solver(S, A, B, a, b, c)

# Solve and transform to real space
u_hat = np.zeros(N)           # Solution spectral space
u_hat = H(u_hat, f_hat)       # Solve
u = SD.backward(u_hat)

# Compare with analytical solution
uj = ul(X)
print(abs(uj-u).max())
assert np.allclose(uj, u)

plt.figure()
plt.plot(X, u)

plt.figure()
plt.plot(X, uj)

plt.figure()
plt.plot(X, u-uj)
plt.title('Error')
#plt.show()
