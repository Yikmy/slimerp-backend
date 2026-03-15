# Tasks
- [x] Task 1: Environment Setup
  - [x] Install `django` and `djangorestframework` via pip
  - [x] Create `requirements/` directory
  - [x] Run `pip freeze > requirements/base.txt`
  - [x] Create `requirements/dev.txt` (include base.txt) and `requirements/prod.txt` (include base.txt)

- [x] Task 2: Initialize Django Project
  - [x] Run `django-admin startproject config .` to generate files in current directory
  - [x] Move `config/settings.py` to `config/settings/base.py`
  - [x] Create `config/settings/__init__.py`, `dev.py`, `prod.py`
  - [x] Update `manage.py` to point to `config.settings.dev`
  - [x] Update `config/wsgi.py` and `config/asgi.py` to point to `config.settings.prod` (or base/dev as appropriate)
  - [x] Fix `BASE_DIR` in `config/settings/base.py` to point to the project root

- [x] Task 3: Create Skeleton Directories
  - [x] Create `kernel/__init__.py`
  - [x] Create `apps/__init__.py`
  - [x] Create `README.md` (if not exists) with basic project info

- [x] Task 4: Verification
  - [x] Run `python manage.py check` to verify configuration
  - [x] Verify directory structure against `ERP_Tree_Frozen_Annotated_v2.md`
