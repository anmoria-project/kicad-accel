#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Kicad symbol file generator (from .csv pinout)
# Copyright (C) 2026  Johann A. Sollacher <anmoria.project@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import os, sys
from symbols import *

version = "0.3.0"
C_INCH = 2.45

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.sub = []
        self.lastID = 0
    def add(self, node):
        self.sub.append(node)
        self.lastID = self.lastID + 1

class Vec3:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
    def parse(self):
        return f'{self.x} {self.y} {self.z}'



class SymbolPin:
    pindrivers = ['input','output','unspecified','power_in','power_out',
                  'open_collector','open_emitter','no_connect','free','tri_state','bidirectional']
    driver_subst = {
        'ai': 'input',
        'ao' : 'output',
        'di' : 'input',
        'do' : 'output',
        'pi' : 'power_in',
        'po' : 'power_out',
        'nc' : 'no_connect',
        'bi' : 'bidirectional',
        'bidir' : 'bidirectional',
        'ci' : 'input',
        'co': 'output'
    }
    powersymbols = ['+3v3', 'gnd', 'self', 'ext']
    term_subst = {
        'pf:':'e-12f:',
        'nf:':'e-9f:',
        'uf:':'e-6f:',
        'ph:':'e-12h:',
        'nh:':'e-9h:',
        'uh:':'e-6h:',
        'kr:':'e-3r:'
    }

    def __init__(self, ic_pin, unit, name, driver, termination_str):
        self.ic_pin = ic_pin
        self.name = name
        self.unit = unit
        self.driver = driver

        # Add substitution for lazy driver keys
        if driver.lower() in self.driver_subst.keys():
            driver = self.driver_subst[driver]

        if driver not in self.pindrivers:
            print(f"ERROR: Undefined or missing PinDriver: '{driver}'! Name={name}; Block={unit}; PIN={ic_pin}")
            exit(1)
        self.driver = driver
        # self.terminations = terminations
        self.terminations = []


        term_str = termination_str.lower().replace(' ', '')
        for k, v, in self.term_subst.items():
            if term_str.find(k) != -1:
                print(f"NOTE: Replace termination '{k}' with '{v}'")
                term_str = term_str.replace(k, v)


        for term in term_str.split(','):
            term = term.strip()
            if term == '':
                continue
            # Example: 20.0e+3R:+3v3
            tmp, driver= term.lower().split(":")
            float_raw = tmp[0:-1]



            value = float(float_raw)
            component = tmp[-1]
            # if (component not in ['C', 'L', 'R'])
            print(f"Termination: Type={component}; Value={value}; Driver={driver}")
            termination = [component, value, driver]
            if driver.lower() not in self.powersymbols:
                print(f"Termination driver for pin {self.ic_pin} unkown: {driver}")
                exit(-1)
            self.terminations.append(termination)
        if 'self' in termination_str:
            self.hasSelfTermination = True
        else:
            self.hasSelfTermination = False

    def parse_label(self, index):
        if self.hasSelfTermination:
            labelname = '__' + self.name
        elif len(self.terminations) > 0:
            labelname = '_' + self.name
        else:
            labelname = self.name
        labelpos = 2.54 * index
        # NOTE: Check, was 'right bottom'
        parsed = parse_label(labelname, 0.0, labelpos, 180, "right")
        return parsed

    def parse_termination(self, place_position_index, index):
        driver = self.terminations[index][2].lower()
        value = self.terminations[index][1]
        device = "UNDEFINED"

        if self.hasSelfTermination:
            label = '_' + self.name
        else:
            label = '_' + self.name

        if (driver == 'self'):
            driver = '__' + self.name
        elif (driver == 'ext'):
            driver = self.name
        else:
            driver = self.terminations[index][2]

        component = self.terminations[index][0].upper()

        # if (component == "short"):
        #     device = "W_Small"
        if (component == 'R'):
            device = "R_Small"
        elif (component == 'C') or (component == "F"):
            device = "C_Small"
        elif (component == 'L') or (component == "H"):
            device = "L_Small"
        else:
            print(f"ERROR: Termination component unknown: Pin={self.ic_pin}; Component={component}!")
            exit(-1)
        ypos = place_position_index * 2.54

        parsed = ''
        parsed = parsed + parse_label(driver, 5.08, ypos, 0, "left")
        # parsed = parsed + parse_hierarchical_label(driver, 5.08, ypos, 0)
        parsed = parsed + parse_symbol(device, 2.54,  ypos, 270, value)
        parsed = parsed + parse_label(label, 0.0, ypos, 180, "right")



        return parsed


    def parse(self, pos):
        parsed = f'\
(pin {self.driver} line\n\
\t(at {pos.parse()})\n\
\t(length 5.04)\n\
\t(name "{self.name}"\n\
\t\t(effects\n\
\t\t\t(font\n\
\t\t\t\t(size 1.27 1.27)\n\
\t\t\t)\n\
\t\t)\n\
\t)\n\
\t(number "{self.ic_pin}"\n\
\t\t(effects\n\
\t\t\t(font\n\
\t\t\t\t(size 1.27 1.27)\n\
\t\t\t)\n\
\t\t)\n\
\t)\n\
)\n\
'
        return parsed

def indent(string, num_spaces):
    ret_str = ""
    for line in string.splitlines() :
        ret_str = ret_str + '\t' * num_spaces + line + '\n'
    return ret_str

class Symbol:

    def __init__(self, name):
        self.name = name
        self.pins = []
        self.unit_names = []

    def add_pins(self, pins):
        for pin in pins:
            if pin.unit not in self.unit_names:
                self.unit_names.append(pin.unit)
            self.pins.append(pin)


    def parse_labels(self, prefix):
        for unit in self.unit_names:
            i = 0
            unit_text = ""
            filepath = f"./build/{prefix}_{unit}.kicad_labels"
            for pin in self.pins:
                if pin.unit != unit:
                    continue
                i = i + 1
                unit_text  = unit_text + "\n\n" + pin.parse_label(i)

            term_pos_index = i + 4
            for pin in self.pins:
                term_index = 0
                if pin.unit != unit:
                    continue
                for id in range(0, len(pin.terminations)):
                    #     def parse_termination(self, place_position_index, index, label):
                    unit_text  = unit_text + "\n\n" + pin.parse_termination(term_pos_index, term_index)
                    term_pos_index = term_pos_index + 1
                    term_index = term_index + 1

            print(f"Write file: {filepath}")

            # filepath = f'./build/{filename}.kicad_labels'
            fd = open(filepath, 'w+', encoding='utf-8')
            fd.write(unit_text)
            fd.flush()
            fd.close()


    def parse(self):

        max_char = 0
        for pin in self.pins:
            if max_char < len(pin.name):
                max_char = len(pin.name)

        rect_x = max_char * 2.54 * 0.7

        parsed = f'''
(symbol "{self.name}"
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(property "Reference" "U"
			(at {rect_x} -1.27 0)
			(do_not_autoplace)
			(effects
				(font
					(size 1.27 1.27)
				)
				(justify left)
			)
		)
		(symbol "{self.name}_0_1"
			(text "{self.name}"
				(at {rect_x} -3.81 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
		)
		(property "Value" "value-text"
			(at {rect_x} -8.89 0)
			(do_not_autoplace)
			(effects
				(font
					(size 1.27 1.27)
				)
				(justify left)
			)
		)
		(property "Footprint" "footprint-text"
			(at {rect_x} -11.43 0)
			(do_not_autoplace)
			(effects
				(font
					(size 1.27 1.27)
				)
				(justify left)
				(hide yes)
			)
		)
		(property "Description" "description-text"
			(at {rect_x} -13.97 0)
			(do_not_autoplace)
			(effects
				(font
					(size 1.27 1.27)
				)
				(justify left)
				(hide yes)
			)
		)
		(property "Datasheet" "datasheet-text"
			(at {rect_x} -16.51 0)
			(do_not_autoplace)
			(effects
				(font
					(size 1.27 1.27)
				)
				(justify left)
				(hide yes)
			)
		)

'''

# TODO: Fix this...
#         if len(self.unit_names) == 1:
#             num_pins = len(self.pins)

#             parsed = parsed + f'''
#         (symbol "{self.name}_0_1"
#             (rectangle
#                 (start 5.04 0)
#                 (end {rect_x} {-num_pins*2.54})
#                 (stroke
#                     (width 0)
#                     (type default)
#                 )
#                 (fill
#                     (type none)
#                 )
#             )
#         )
#         (symbol "{self.name}_1_1"
# '''
#             unit_pin_id = 0
#             for pin in self.pins:
#                 pin_pos = Vec3(0, -1.27 + unit_pin_id * -2.54, 0)
#                 parsed = parsed + indent(pin.parse(pin_pos), 2)
#                 unit_pin_id = unit_pin_id + 1
#             parsed = parsed + '\t)'


        if len(self.unit_names) > 1:
            unit_id = 0
            for unit_name in self.unit_names:
                num_unit_pins = 0
                for pin in self.pins:
                    if pin.unit == unit_name:
                        num_unit_pins = num_unit_pins + 1
                unit_id = unit_id + 1
                parsed = parsed + f'''
        (symbol "{self.name}_{unit_id}_1"
            (rectangle
                (start 5.04 0)
                (end {rect_x} {-num_unit_pins*2.54 - 0.0})
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
			(text "{unit_name}"
				(at {rect_x} -6.35 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
'''
                unit_pin_id = 0
                for pin in self.pins:
                    if unit_name != pin.unit:
                        continue
                    pin_pos = Vec3(0, -1.27 + unit_pin_id * -2.54, 0)
                    parsed = parsed + indent(pin.parse(pin_pos), 2)
                    unit_pin_id = unit_pin_id + 1
                parsed = parsed + '\t)'

        return parsed



class Library:
    def __init__(self, name):
        self.name = name
        self.symbols = []

    def add_symbols(self, symbols):
        for symbol in symbols:
            self.symbols.append(symbol)

    def parse_labels(self):
        for symbol in self.symbols:
            symbol.parse_labels(self.name)

    def parse(self):

        parsed = ""
        parsed = f'''
(kicad_symbol_lib
	(version 20241209)
	(generator "kicad_symbol_editor")
	(generator_version "9.0")
'''
        for symbol in self.symbols:
            parsed = parsed + indent(symbol.parse(), 1)
        parsed = parsed + f'\
\t\t(embedded_fonts no)\n\
\t)\n\
)\n\
\n'
        return parsed

    def gen_file(self):
        filepath = f'./build/{self.name}.kicad_sym'
        f_lib = open(filepath, 'w+', encoding='utf-8')
        f_lib.write(self.parse())
        f_lib.flush()
        f_lib.close()
        print("Generated file: " + filepath)

# def gen_labels_file(self):


def csv2pins(filepath):
    seperator = ';'
    cols_primary = {"block": -1,
                    "pin_id": -1,
                    "function0": -1,
                    "driver0": -1,
                      "function1" : -1,
                      "driver1" : -1
                      }
    cols_optional = {
                    "pin_prefix": -1,
                    "function2": -1,
                    "driver2": -1,
                    "function3": -1,
                    "driver3": -1,
                    "voltage": -1,
                    "termination": -1,
                    "capabilities": -1,
                    "origin_pin_name": -1,
                    "notes": -1
    }


    f = open (filepath, 'r', encoding='utf-8')
    text = f.read()
    f.close()
    i = 0
    Pins = []
    line_id = 0
    lines = text.split('\n')

    cnt_semi = text.count(';')
    cnt_comma = text.count(',')
    cnt_tab = text.count('\t')

    print(f"Count semi={cnt_semi}, comma={cnt_comma}, tabs={cnt_tab}")

    if cnt_semi > cnt_comma and cnt_semi > cnt_tab:
        seperator = ';'
    elif cnt_comma > cnt_tab:
        seperator = ','
    else:
        seperator = '\t'

    print(f"NOTE: Selected seperator for .csv file: '{seperator}'")

    # NOTE: Autodetect column position
    col_id = 0
    for key in lines[0].split(seperator):
        key = key.strip()
        if key == '': continue
        # print(f"Found key: {key}")
        if key in cols_primary.keys():
            print(f"KEY '{key}' found in primary keys!")
            if cols_primary[key] != -1:
                print(f"ERROR: Column '{key}' is already defined!")
                exit(1)
            cols_primary[key] = col_id
        elif key in cols_optional:
            if cols_optional[key] != -1:
                print(f"ERROR: Column '{key}' is already defined!")
                exit(1)
            print(f"KEY '{key}' found in optional keys!")
            cols_optional[key] = col_id
        else:
            print(f"WARNING: Column '{key}' is unknown and will be ignored: {key}")
        col_id  = col_id +1

    # NOTE: Check for missing keys
    for key, val in cols_primary.items():
        if val == -1:
            print(f"ERROR: Column '{key}' is missing!")
            exit(-1)



    col_ids = {}
    col_ids.update({k: v for k, v in cols_primary.items() if v != -1})
    col_ids.update({k: v for k, v in cols_optional.items() if v != -1})


    used_function_keys = []
    for k, v in col_ids.items():
        if k.startswith('function'):
            used_function_keys.append(k)
    used_function_keys.sort()

    for line in lines[1:-1]:

        splits = line.split(seperator)

        function = []
        driver = []

        block = splits[col_ids['block']].strip()
        pin_id = splits[col_ids['pin_id']].strip()

        pin_prefix = ''
        if 'pin_prefix' in col_ids.keys():
            pin_prefix = splits[col_ids['pin_prefix']].strip()

        termination_str = splits[col_ids['termination']].strip()


        # Assemble name from all specified functionalities
        name = pin_prefix if pin_prefix != '' else ''

        for fkt in used_function_keys:
            subfkt = splits[col_ids[fkt]].strip()
            if subfkt == '':
                continue
            if name == '':
                name = subfkt
            else:
                name = name + '__' + subfkt

        # NOTE: Driver1 overrides driver0. This must be changed in kicad source code to support multiple drivers!
        driver = ''
        if splits[col_ids['driver1']].strip() != '' :
            driver = driver + splits[col_ids['driver1']].strip()
        elif splits[col_ids['driver0']].strip() != '' :
            driver = driver + splits[col_ids['driver0']].strip()

        # # Resolve termination stuff:
        # for term in termination_str.split(','):

        #     exit(1)


        if (name == "" and block == "" and pin_id == ""):
            continue
        print("pin_id={}; block={}; name={}; driver={}".format( pin_id, block, name, driver))
        pin = SymbolPin(pin_id, block, name, driver, termination_str)
        i = i + 1
        # Pos = Vec3(-2.54, -1.27 + i* -2.54, 0)
        Pins.append(pin)

    return Pins


def print_help():
    helpstr = '''
Usage: [python3] system-generator.py [Options] FILE

Options:
    -v, --version   Print license and version
    -h, --help      Print this help

Example:

    python3 symbol-generator.py ./test/multi_unit_test.csv

    ./symbol-generator.py ./test/single_unit_test.csv

Build output will be in the './build/' folder.
Read the README.md for more information!
Example input files are in folder ./test/*.csv
'''
    print(helpstr)

def print_license_short():
    license = f'''
Symbol-generator v{version}
Copyright (C) 2026  Johann A. Sollacher
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
'''
    print(license)

def main():
    # DO NOT REMOVE!
    print("Symbol-generator: For version or license use '--version'. For help use '--help'")

    if '-v' in sys.argv or '--version' in sys.argv:
        print_license_short()
        exit(0)

    if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) != 2:
        print_license_short()
        print_help()
        exit(0)

    path = sys.argv[-1]
    # path = "/home/yoctouser/scm/pcb-bricks/kicad-accel/test/multi_unit_big_test.csv"
    if not os.path.isfile(path):
        print("ERROR: File does not exist! Please specify a file as argument!")
        exit(1)
    sym_name = os.path.basename(path).split('.')[0]
    lib_name = sym_name

    sym1 = Symbol(sym_name)
    pins = csv2pins(path)
    sym1.add_pins(pins)
    lib1 = Library(lib_name)
    lib1.add_symbols([sym1])
    lib1.gen_file()
    lib1.parse_labels()
    print("WARNING: Before using Termination, first add some dummy components from library: L_Small, C_Small, R_Small! Otherwise Kicad will crash!")


if __name__ == "__main__":
    main()

print("Test")

