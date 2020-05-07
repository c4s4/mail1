# Makefile for project continuum
# See make-tools at https://github.com/c4s4/make-tools

# Parent makefiles at https://github.com/c4s4/make
include .make/help.mk
include .make/python.mk
include .make/git.mk
include ~/.make/make.mk

MAKE_ID=d6f2d484487c3a245a8665a78e3a63810e3ec30b
PYTHON_ENV=~/.env/email.env
PYTHON_ITG=. $(PYTHON_ENV) && venv/bin/python mail1/test_mail1.py
