# WebCase file monitor

Simple package to handle app files changes.

## Installation

```sh
pip install wc-django-filemonitor
```

```python
INSTALLED_APPS = [
  'wcd_filemonitor',

  # Submodule that updates app's translations data if translation 
  # files changed:
  'wcd_filemonitor.contrib.translations',
]
```
