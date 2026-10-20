# Repository Guidelines

## Project Structure & Module Organization

This workspace currently has no source files, tests, or build configuration. As material is added, use `docs/` for definitions, proofs, and references; `scripts/` for reproducible computations; `tests/` for automated checks; and `assets/` for figures. Create directories only when needed. Keep generated output separate from source material and document how to regenerate it.

## Build, Test, and Development Commands

No project-wide build or test command is configured. Available local math tools are Mathematica 12.1 and MATLAB R2020a:

- `wolframscript -code 'Print[2 + 2]'` — check Mathematica execution.
- `wolframscript -file scripts/example.wl` — run a Wolfram Language script once added.
- `WolframKernel -noprompt -run 'Get["scripts/example.wl"]; Quit[]'` — run through the kernel directly.
- `matlab -batch "disp(2 + 2)"` — check MATLAB execution.
- `matlab -batch "run('scripts/example.m')"` — run a MATLAB script once added.

Mathematica requires network access to its MathLM licence server. Record dependencies and exact reproduction commands alongside new computations.

## Coding Style & Naming Conventions

Use four spaces for indentation in new scripts. Choose descriptive filenames such as `check_small_cases.wl` or `check_small_cases.m`; keep MATLAB function names aligned with filenames. Define mathematical notation before use and explain non-obvious transformations. No formatter or linter is configured; follow surrounding style as the project develops.

## Testing Guidelines

No testing framework or coverage threshold is established. Add small, deterministic checks for computational claims, including boundary cases and known examples. Use descriptive test names such as `test_small_cases.m`, explicit assertions, and fixed random seeds when applicable. Document each check's command and expected result. Distinguish proved statements, finite verification, and conjectures; numerical agreement alone is not a proof.

## Commit & Pull Request Guidelines

No usable Git history is available to establish existing conventions. Use concise, imperative commit subjects, such as `Add small-case verification script`, and keep changes focused. Pull requests should explain the mathematical or implementation change, link relevant issues or sources, and list validation commands and outcomes. Include rendered previews when changing figures or formatted documents.
