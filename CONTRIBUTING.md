# Contributing

This project needs testers and critical listeners as much as it needs code.

## If you're testing it (no coding required)

1. Run `synthesize.py` and listen to the example sounds, or use `try_it.py`
   with your own functions.
2. Open a GitHub Issue titled `[Testing] <what you tried>` and tell us:
   - What function(s) you tried
   - What you (or the kid you tested with) actually heard/noticed
   - Whether it helped, distracted, or made no difference
   - Age/context of the person you tested with, if applicable

Negative or inconclusive results are genuinely useful — please share them
even if "it didn't seem to help."

## If you're contributing code

1. Fork the repo, create a branch (`feature/your-idea`)
2. Keep the same design pattern: `features.py` → `sound_mapping.py` →
   `synthesize.py`. New function families should:
   - Get a clear entry in `classify_family()`
   - Get an explicit, consistent timbre in `TIMBRES`
   - Come with a one-line explanation in a comment of *why* that sound choice
     makes sense for the target age group
3. Open a PR describing what you changed and, ideally, what you tested it
   against.

## Code style

Plain, readable Python. No dependencies beyond `sympy`, `numpy`, `scipy`
unless there's a strong reason — this should stay easy for teachers/parents
with basic Python knowledge to read and modify.
