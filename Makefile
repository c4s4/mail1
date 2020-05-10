# Makefile for project continuum

# Parent makefiles at https://github.com/c4s4/make
include ~/.make/Python.mk

PYTHON_ENV=~/.env/email.env
PYTHON_ITG=. $(PYTHON_ENV) && venv/bin/python mail1/test_mail1.py
