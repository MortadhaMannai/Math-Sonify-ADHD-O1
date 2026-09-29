"""
Step 1: Turn a math function string into a small dict of features
that a primary-school kid would actually recognize:
- family: 'constant' | 'linear' | 'quadratic' | 'periodic' | 'other'
- direction: 'increasing' | 'decreasing' | 'both' (for non-periodic)
- roots: list of real x-values where f(x) = 0 (if any, in a sane range)
- symmetric: 'even' | 'odd' | None
- coeffs: raw coefficients we'll need for sound mapping later
"""

import sympy as sp

x = sp.symbols('x')


def parse_function(expr_str):
    """Turn a string like 'x**2 - 3*x + 2' into a sympy expression."""
    return sp.sympify(expr_str)


def classify_family(f):
    """Decide which 'family' the function belongs to, primary-school style."""
    poly = sp.Poly(f, x) if f.is_polynomial(x) else None

    if poly is not None:
        degree = poly.degree()
        if degree == 0:
            return 'constant', poly.all_coeffs()
        elif degree == 1:
            return 'linear', poly.all_coeffs()   # [m, b]
        elif degree == 2:
            return 'quadratic', poly.all_coeffs()  # [a, b, c]
        else:
            return 'other', poly.all_coeffs()

    # crude periodic check: does sin/cos appear anywhere in the expression?
    if f.has(sp.sin) or f.has(sp.cos):
        return 'periodic', None

    return 'other', None


def get_direction(f, family, coeffs):
    """For linear/quadratic: does it go up, down, or both (dip/peak)?"""
    if family == 'linear':
        m = float(coeffs[0])
        return 'increasing' if m > 0 else 'decreasing' if m < 0 else 'constant'
    if family == 'quadratic':
        a = float(coeffs[0])
        return 'upward' if a > 0 else 'downward'  # opens up = valley, opens down = hill
    return 'both'  # periodic / other: treat as oscillating


def get_symmetry(f):
    """Even: f(-x) == f(x). Odd: f(-x) == -f(x). Else None."""
    f_neg = sp.simplify(f.subs(x, -x))
    if sp.simplify(f_neg - f) == 0:
        return 'even'
    if sp.simplify(f_neg + f) == 0:
        return 'odd'
    return None


def get_real_roots(f, lo=-10, hi=10):
    """Real roots within a sane range for a primary-school plot window."""
    try:
        roots = sp.solve(sp.Eq(f, 0), x)
        real_roots = [float(r) for r in roots if r.is_real and lo <= r <= hi]
        return sorted(real_roots)
    except Exception:
        return []


def extract_features(expr_str):
    f = parse_function(expr_str)
    family, coeffs = classify_family(f)
    direction = get_direction(f, family, coeffs)
    symmetry = get_symmetry(f)
    roots = get_real_roots(f)

    return {
        'expr': str(f),
        'family': family,
        'coeffs': [float(c) for c in coeffs] if coeffs else None,
        'direction': direction,
        'symmetric': symmetry,
        'roots': roots,
        'sympy_expr': f,  # kept for step 2 (sampling y-values for the pitch contour)
    }


if __name__ == '__main__':
    tests = ["2*x + 3", "-x + 5", "x**2 - 4", "-x**2 + 9", "sin(x)", "x**2 - 3*x + 2"]
    for t in tests:
        feats = extract_features(t)
        printable = {k: v for k, v in feats.items() if k != 'sympy_expr'}
        print(f"{t:20s} -> {printable}")
