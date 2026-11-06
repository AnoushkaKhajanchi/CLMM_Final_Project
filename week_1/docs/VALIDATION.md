# Authoring validation

CUDA 13.0 repair: replaced bitsandbytes 0.46.1 with 0.50.2, whose stable documentation lists Linux CUDA 13.0 support. Added a real NF4 quantization/forward-pass preflight in the notebook and explicit session restart instructions. The preflight itself needs the user's GPU; it has not been executed locally.

Passed locally:

- Jupyter notebook schema validation and compilation of every code cell.
- CSV column consistency.
- Actual upstream memory insert/update/search/delete and checkpoint reconstruction, using a mock CPU embedding model.
- Lossless chunk boundaries, including whitespace and Unicode test inputs.
- Interrupted construction resumes without regenerating completed chunks or duplicating writes, using synthetic model output and the actual upstream parser/tool executor.
- Upstream normalized exact-match, substring-match, and accepted-alias scoring checks.

Not executed locally: GPU inference, actual model and embedding downloads, full notebook installation inside Colab, real model generation, or full benchmark evaluation. These are explicit Week 1 tasks; no measured model accuracy or GPU feasibility is claimed by this package.
