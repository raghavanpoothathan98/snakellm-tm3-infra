# snakellm-tm3-infra

Infra layer for SnakeLLM pipeline specs:
- validates JSON specs (strict schema)
- generates conda env files
- generates a SLURM Snakemake profile
- bundles artifacts into zip files

## Repo layout
- `specs/` pipeline JSON specs
- `scripts/` validation + generators
- `envs/` generated conda env yaml files
- `profiles/slurm/` generated Snakemake SLURM profile
- `dist/` bundled zip artifacts

## Usage (local)
```bash
sudo apt update && sudo apt install -y make python3-pip
python3 -m pip install -r requirements.txt
make all

“Download artifacts from Actions → latest run → Artifacts → bundled-pipelines.”