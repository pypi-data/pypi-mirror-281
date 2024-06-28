import sympy as sp
import sympy.printing as printing

from .IntegralMonomial import IM
from .utils import is_float 


class IntegralPolynomial(): 
 
    def __init__(self, 
                P,  
                copy=False):  
        if type(P) == dict:
            self.dict = {} 
            if not copy:  
                for M, coeff in P.items(): 
                    coeff = sp.cancel(coeff)
                    if coeff != 0:
                        self.dict[M] = coeff 
            else:
                for k,coeff in P.items():
                    self.dict[k] = coeff
        elif isinstance(P, sp.Expr):
            self.dict = dict(P.as_coefficients_dict(IM))
        elif P == 0:
            self.dict = {}
        else:
            raise SyntaxError

    def get_sympy_repr(self):
        L = self.dict.items()
        sympy_repr = sp.Add(*[coeff*M for M,coeff in L]) 
        return sympy_repr
    
    def add_alpha_M(self, alpha, M):
        if M in self.dict:
            new_coeff = sp.cancel(alpha + self.dict[M])
            if new_coeff !=0:
                self.dict[M] = new_coeff
            else:
                del self.dict[M]
        else:
            self.dict[M] = alpha
  
    def is_zero(self):
        return len(self.dict) ==0
    
    def __repr__(self):
        return f"IntegralPolynomial({self.get_sympy_repr()})"
    
    def repr_display_math(self):
        return '{}'.format(printing.latex(self.get_sympy_repr()))

    def _repr_latex_(self):  
        return '${}$'.format(printing.latex(self.get_sympy_repr()))

    def copy(self):
        # d = copy.deepcopy(self.dict)
        d = self.dict
        #avoid sp simplify on coeff when copy
        return IntegralPolynomial(d, copy=True) 
     
    def cut_P(self, cut_type: str):
        """
        Definition 8 of Contribution to Integral Elimination
        We simply extend the cut method of the Integral Monomial class to 
        integral polynomials 
        
        Disclaimer: this method will throw an error if you use it on 
        polynomial that can't be cutted 
        for exemple, trying to cut a pol with monomials of depth < 2 will 
        throw an error if you cut using i2+
        """
        P_cutted = {}
        P = self.dict.items() 
        for M,coeff in P:
            M_cutted = M.cut(cut_type) 
            if P_cutted.get(M_cutted) is None:
                P_cutted[M_cutted] = coeff 
            else:
                P_cutted[M_cutted] += coeff 
        return IntegralPolynomial(P_cutted)
    
    def get_P_I(self): 
        P_I = {}
        P = self.dict.items()
        for M,coeff in P: 
            M0 = M.cut("0") 
            if M.get_nb_int() >= 1 and M0 == IM(1):
                if M not in P_I:
                    P_I[M] = coeff
                else:
                    # we are not supposed to have this case
                    raise ValueError 
        # we avoid the simplification process of the coeffs
        # by using copy=True
        return  IntegralPolynomial(P_I, copy=True)

    def get_P_N(self): 
        P_N = {}
        P = self.dict.items()
        for M,coeff in P:  
            M0 = M.cut("0")
            if M==IM(1): #cst
                P_N[M] = coeff
            elif M0 != IM(1):
                if M not in P_N:
                    P_N[M] = coeff
                else:
                    # we are not supposed to have this case
                    raise ValueError 
        # we avoid the simplification process of the coeffs
        # by using copy=True
        return  IntegralPolynomial(P_N, copy=True)
    
    def get_cst_terms(self):
        CST = {}
        P = self.dict.items()
        for M,coeff in P:  
            if M == IM(1):
                if M in CST:
                    CST[M] += coeff 
                else:
                    CST[M] = coeff 
        return  IntegralPolynomial(CST)
    
    def get_time_dependant_functions(self):
        """
        example: if you have 
        P = IntegralPolynomial(IM(x(t)) - x(0)*IM(1) 
                        - theta*IM(1,x(t)*y(t)**2) - IM(1,y(t)))
        it will return {x,y}
        """
        res = set()
        for f in self.get_sympy_repr().atoms(sp.Function):
            if f.func != IM and not is_float(f.args[0]):
                res.add(f) 
        return res