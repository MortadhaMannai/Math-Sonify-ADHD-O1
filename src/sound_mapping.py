"""
Step 2: features -> sound recipe.

Design rules (the pedagogical core):
- PITCH CONTOUR literally traces the shape of the graph. A line going up
  sounds like a rising tone. A downward parabola sounds like a rise-then-fall.
  This way the sound and the visual graph reinforce the SAME mental image.
- TIMBRE encodes the FAMILY, consistently, every time:
    linear    -> pure sine (clean, simple)
    quadratic -> soft triangle wave (a bit "rounder")
    periodic  -> vibrato sine (audibly wavering, matches "it repeats")
- A short double "tick" marks each ROOT (zero-crossing) as the contour
  passes through it -- an audible landmark tied to a visual one.
- Duration is short (1.5-2.5s) and fixed range, on purpose: predictability
  and low sensory surprise matter more than "richness" for this use case.
"""

from features import extract_features
import numpy as np
import sympy as sp

x = sp.symbols('x')

TIMBRES = {
    'linear': 'sine',
    'constant': 'sine',
    'quadratic': 'triangle',
    'periodic': 'vibrato_sine',
    'other': 'triangle',
}

BASE_FREQ = 300      # Hz, floor of the pitch range
FREQ_RANGE = 350     # Hz, how much pitch can swing (300-650 Hz: safely audible, not shrill)
DURATION = 2.0        # seconds, fixed on purpose (predictability)
X_LO, X_HI = -6, 6    # the x-window we sonify, matches a typical school-graph window


def build_sound_recipe(expr_str):
    feats = extract_features(expr_str)
    f = feats['sympy_expr']

    # Sample y-values across the x-window to build the pitch contour
    xs = np.linspace(X_LO, X_HI, 400)
    f_lamb = sp.lambdify(x, f, 'numpy')
    try:
        ys = f_lamb(xs)
        ys = np.nan_to_num(ys, nan=0.0, posinf=0.0, neginf=0.0)
    except Exception:
        ys = np.zeros_like(xs)

    # Normalize y-values to 0..1 so ANY function maps into our safe freq range
    y_min, y_max = ys.min(), ys.max()
    if y_max - y_min < 1e-6:
        norm_ys = np.full_like(ys, 0.5)
    else:
        norm_ys = (ys - y_min) / (y_max - y_min)

    freq_contour = BASE_FREQ + norm_ys * FREQ_RANGE

    # Where do roots fall in the x-window, as a fraction of duration (for tick placement)
    root_times = [
        (r - X_LO) / (X_HI - X_LO) * DURATION
        for r in feats['roots'] if X_LO <= r <= X_HI
    ]

    recipe = {
        'expr': feats['expr'],
        'family': feats['family'],
        'timbre': TIMBRES.get(feats['family'], 'triangle'),
        'direction': feats['direction'],
        'symmetric': feats['symmetric'],
        'freq_contour': freq_contour,     # array, one freq per time-sample
        'duration': DURATION,
        'root_tick_times': root_times,    # seconds into the clip
    }
    return recipe


if __name__ == '__main__':
    for expr in ["2*x + 3", "x**2 - 3*x + 2", "sin(x)"]:
        r = build_sound_recipe(expr)
        print(f"{expr:20s} -> family={r['family']:10s} timbre={r['timbre']:12s} "
              f"root_ticks={[round(t,2) for t in r['root_tick_times']]} "
              f"freq_range=({r['freq_contour'].min():.0f},{r['freq_contour'].max():.0f})")
