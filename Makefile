# Makefile for project continuum
# See make-tools at https://github.com/c4s4/make-tools

# Parent makefiles at https://github.com/c4s4/make
include .make/help.mk
include .make/python.mk
include .make/git.mk
include ~/.make/make.mk

MAKE_ID=c8addc1e47e6469c2f4629495fd15c79603de483
PYTHON_ENV=~/.env/email.env
PYTHON_ITG=. $(PYTHON_ENV) && venv/bin/python mail1/test_mail1.py
