"""
Step 3: sound recipe -> actual audio (.wav file).

Uses simple oscillator synthesis with numpy (no external audio libs needed).
Each timbre is a different waveform shape / modulation:
- sine          : pure tone            -> used for linear/constant
- triangle      : softer, rounder tone -> used for quadratic
- vibrato_sine  : sine with a slow pitch wobble -> used for periodic

A short "tick" (a quick 1000 Hz click) is layered in at each root, so kids
learn to associate that click with "the graph crosses zero here."
"""

import numpy as np
from scipy.io.wavfile import write
from sound_mapping import build_sound_recipe

SR = 44100  # sample rate


def _phase_from_freq_contour(freq_contour, duration, sr):
    """Integrate instantaneous frequency into a phase array (avoids clicks
    from naive per-sample frequency changes)."""
    n_samples = int(duration * sr)
    # resample freq_contour (400 pts) onto n_samples
    t_src = np.linspace(0, duration, len(freq_contour))
    t_dst = np.linspace(0, duration, n_samples)
    freq_dense = np.interp(t_dst, t_src, freq_contour)
    phase = 2 * np.pi * np.cumsum(freq_dense) / sr
    return phase, t_dst


def render_waveform(recipe):
    phase, t = _phase_from_freq_contour(recipe['freq_contour'], recipe['duration'], SR)

    if recipe['timbre'] == 'sine':
        wave = np.sin(phase)

    elif recipe['timbre'] == 'triangle':
        # triangle wave via sine's sign-based approximation (smooth, no harsh harmonics)
        wave = (2 / np.pi) * np.arcsin(np.sin(phase))

    elif recipe['timbre'] == 'vibrato_sine':
        vibrato = 0.15 * np.sin(2 * np.pi * 5 * t)  # 5 Hz wobble, subtle
        wave = np.sin(phase + vibrato)

    else:
        wave = np.sin(phase)

    # fade in/out to avoid clicks at start/end (10ms each)
    fade_len = int(0.01 * SR)
    fade = np.ones_like(wave)
    fade[:fade_len] = np.linspace(0, 1, fade_len)
    fade[-fade_len:] = np.linspace(1, 0, fade_len)
    wave *= fade

    # layer in root "ticks"
    for tick_time in recipe['root_tick_times']:
        idx = int(tick_time * SR)
        tick_len = int(0.05 * SR)  # 50ms click
        if 0 <= idx < len(wave) - tick_len:
            tick_t = np.linspace(0, 0.05, tick_len)
            tick = 0.4 * np.sin(2 * np.pi * 1000 * tick_t) * np.exp(-tick_t * 40)
            wave[idx:idx + tick_len] += tick

    wave = 0.5 * wave / (np.max(np.abs(wave)) + 1e-9)  # normalize, leave headroom
    return wave


def save_sound(expr_str, out_path):
    recipe = build_sound_recipe(expr_str)
    wave = render_waveform(recipe)
    write(out_path, SR, (wave * 32767).astype(np.int16))
    print(f"Saved {out_path}  <-  {expr_str}  "
          f"(family={recipe['family']}, timbre={recipe['timbre']})")
    return recipe


if __name__ == '__main__':
    import os
    out_dir = os.path.join(os.path.dirname(__file__), "..", "examples")
    os.makedirs(out_dir, exist_ok=True)
    examples = {
        "2*x + 3": "linear_up.wav",
        "-x + 5": "linear_down.wav",
        "x**2 - 3*x + 2": "quadratic_valley.wav",
        "-x**2 + 9": "quadratic_hill.wav",
        "sin(x)": "periodic_sin.wav",
    }
    for expr, fname in examples.items():
        save_sound(expr, os.path.join(out_dir, fname))
