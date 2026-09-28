"""
Quick manual test: generate and save a sound for any function you type.

Usage:
    python3 try_it.py "x**2 - 4"
    python3 try_it.py "3*x + 1" my_test.wav
"""

import sys
from synthesize import save_sound

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 try_it.py "<function>" [output.wav]')
        sys.exit(1)

    expr = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "test_output.wav"
    save_sound(expr, out_path)
