# TODO: maybe add all source files as dependeencies and so on...
#
all:
	@echo "nothing here yet"

test:
	nosetests -vvs --with-coverage --cover-html

clean:
	rm -rvf cover/

.PHONY: all test clean

