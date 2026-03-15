# ERP Backend

This project is the backend for the ERP system, built with Django.

## Structure

- `manage.py`: Django project management entry point.
- `requirements/`: Dependency lists.
- `config/`: Django project configuration.
- `kernel/`: Frozen kernel modules (auth, audit, etc.).
- `apps/`: Business modules (customer, material, accounting, etc.).
- `docs/`: Documentation.

## Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements/dev.txt
   ```

3. Run the server:
   ```bash
   python manage.py runserver
   ```
