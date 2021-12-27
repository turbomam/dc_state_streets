.PHONY: clean all

clean:
	rm dc_state_streets.txt

dc_state_streets.txt:
	python dc_state_streets.py > $@

all: clean dc_state_streets.txt
