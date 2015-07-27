NAME=mail1
VERSION=$(shell changelog release version)
BUILD_DIR=build

YELLOW=\033[1m\033[93m
CYAN=\033[1m\033[96m
CLEAR=\033[0m

.PHONY: env test

help:
	@echo "$(CYAN)init$(CLEAR)     Build virtualenv"
	@echo "$(CYAN)clean$(CLEAR)    Clean generated files"
	@echo "$(CYAN)check$(CLEAR)    Check Python code"
	@echo "$(CYAN)test$(CLEAR)     Run unit tests"
	@echo "$(CYAN)package$(CLEAR)  Build package"
	@echo "$(CYAN)release$(CLEAR)  Release project"

init:
	@echo "$(YELLOW)Building virtualenv$(CLEAR)"
	rm -rf env
	virtualenv env
	. env/bin/activate && pip install -r etc/requirements.txt

clean:
	@echo "$(YELLOW)Cleaning generated files$(CLEAR)"
	rm -rf $(BUILD_DIR)
	rm -f `find $(NAME) -name "*.pyc"`

check:
	@echo "$(YELLOW)Checking Python code$(CLEAR)"
	. env/bin/activate && pylint --rcfile=etc/pylint.cfg $(NAME)

test: check
	@echo "$(YELLOW)Running unit tests$(CLEAR)"
	. env/bin/activate && python $(NAME)/test_$(NAME).py

package: test clean
	@echo "$(YELLOW)Building package$(CLEAR)"
	mkdir -p $(BUILD_DIR)
	cp etc/setup.py $(BUILD_DIR)/
	sed -i -e "s/VERSION/$(VERSION)/" $(BUILD_DIR)/setup.py
	pandoc -f markdown -t rst README.md > $(BUILD_DIR)/README.rst
	cp -r LICENSE.txt etc/MANIFEST.in $(NAME) $(BUILD_DIR)/
	cd $(BUILD_DIR) && python setup.py sdist -d .

release: package
	@echo "$(YELLOW)Releasing project$(CLEAR)"
	cd $(BUILD_DIR) && python setup.py sdist -d . register upload
	release

