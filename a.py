import sympy as sy
from sympy.abc import *
eq1 =sy.Eq(3+x,y)
eq2 = sy.Eq(2*y,3)
sy.solve([eq1,eq2],[x,y])