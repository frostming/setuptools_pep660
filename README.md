# setuptools-pep660


This is a Python 2 compatible PEP 660 backend adapted from https://github.com/dholth/setuptools_pep660

Use as PEP 517 backend:

```toml
# pyproject.toml

[build-system]
requires = ["setuptools_pep660"]
build-backend = "setuptools_pep660"
```

See https://www.python.org/dev/peps/pep-0660/
