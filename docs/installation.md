# Installation

## Requirements

- **Python 3.10+**
- No third-party runtime dependencies

## pip

```bash
pip install csvdir
```

## From source

```bash
git clone https://github.com/eddiethedean/csvdir.git
cd csvdir
pip install -e .
```

### Development and documentation extras

```bash
pip install -e ".[dev]"    # pytest, ruff, mypy
pip install -e ".[docs]"   # Sphinx, Furo, MyST
```

## Verify

```python
import csvdir
print(csvdir.__version__)
```

## Optional: pandas

pandas is **not** required by csvdir. Install it only if you use {class}`~csvdir.CsvDirFile` with `pandas.read_csv`:

```bash
pip install pandas
```
