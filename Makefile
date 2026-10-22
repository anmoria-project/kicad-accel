
# SRCS:=$(wildcard test/*.csv)
# TARGETS:=$(subst interfaces,build,$(SRCS:.csv=.kicad_sym))
# TARGET:=adapter-som-40p.kicad_sym

# INPUTS = test/stm32g031_a.csv test/stm32g031_b.csv
# OUTPUTS = $(patsubst test/%.csv,build/%.kicad_sym,$(INPUTS))
SHELL := /bin/bash

.PHONY: testlib


CC:=./symbol-generator.py
CCFLAGS:=--simple-paths

lib: build/stm32g031_a.kicad_busses build/stm32g031_b.kicad_busses
	@echo "Try to build targets: $<"

testlib:
	export LIB_NAME=build/testlib.kicad_sym && make 

build/%.kicad_busses: test/%.csv
ifdef LIB_NAME
	@echo "Try to build [single-lib] $@"
	source init.sh && ${CC} ${CCFLAGS} -o $(LIB_NAME) $<
else
	@echo "Try to build [multi-lib] $@"
	source init.sh && ${CC} ${CCFLAGS} -o $(@:.kicad_busses=.kicad_sym) $<
endif

clean:
	rm ./build/*.kicad_sym
	rm ./build/*.kicad_labels
	rm ./build/*.kicad_busses

