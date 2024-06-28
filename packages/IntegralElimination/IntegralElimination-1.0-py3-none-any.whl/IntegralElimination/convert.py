import sympy as sp
from ordered_set import OrderedSet

from .utils import expr_has_symbol
from .IntegralMonomial import IM
from .IntegralPolynomial import IntegralPolynomial


def first_order_ODE_to_IntegralPolynomial(
                                        expr:sp.Expr, 
                                        var=sp.Symbol("t")
                                        ) -> IntegralPolynomial:
        expr = sp.expand(expr)
        dict_coeff = dict(expr.as_coefficients_dict(var))
        P = IntegralPolynomial(0)
        if expr_has_symbol(expr, sp.Integral): raise ValueError
        expr_has_der = expr_has_symbol(expr,sp.Derivative)
        for mons, coeff in dict_coeff.items():
            if mons.func == sp.Derivative : 
                assert mons.args[1][1] == 1 
                m = mons.args[0]
                CI = sp.Symbol(f"{m.func}0")
                M = IM(m)
                P.add_alpha_M(coeff, M)
                P.add_alpha_M(-CI,IM(1))
            else:
                if expr_has_der:
                    M = IM(1,mons)
                    P.add_alpha_M(coeff,M)
                else:
                    M = IM(mons)
                    P.add_alpha_M(coeff,M)
        return P

def ODE_sys_to_Integral_sys(sys: list[sp.Expr]
                            ) -> OrderedSet[IntegralPolynomial]:
    sys = OrderedSet([first_order_ODE_to_IntegralPolynomial(eq) for eq in sys])
    return  sys