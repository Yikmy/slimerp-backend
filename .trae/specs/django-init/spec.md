# Django Project Initialization Spec

## Why
To establish the foundational Django project structure according to the frozen ERP architecture, enabling further development of kernel and business modules.
The current environment is missing Django and Django Rest Framework, which are prerequisites.

## What Changes
- Install `Django` and `djangorestframework`.
- Create `requirements/` directory and `base.txt` from installed packages.
- Initialize Django project with configuration in `config/`.
- Set up `config/settings/` with `base.py`, `dev.py`, `prod.py`.
- Create `manage.py` in the root.
- Create empty `kernel/` and `apps/` directories with `__init__.py`.
- **BREAKING**: None (New project setup).

## Impact
- Affected specs: None
- Affected code: `backend/` root directory structure.

## ADDED Requirements
### Requirement: Environment Setup
- Install necessary packages: `Django`, `djangorestframework`.
- Generate `requirements/base.txt` containing these packages.

### Requirement: Project Structure
The system SHALL follow the directory structure defined in `ERP_Tree_Frozen_Annotated_v2.md` lines 10-32.
- `manage.py` in root.
- `requirements/` directory for dependencies.
- `config/` directory for Django settings and entry points.
- `kernel/` and `apps/` placeholders.
