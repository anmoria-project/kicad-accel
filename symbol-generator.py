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

version = "0.1.0"
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
    def __init__(self, ic_pin, unit, name, driver):
        self.ic_pin = ic_pin
        self.name = name
        self.unit = unit
        self.driver = driver
        if driver not in self.pindrivers:
            print(f"ERROR: Undefined PinDriver: {driver}! Name={name}; Block={unit}; PIN={ic_pin}")
            exit(1)
        self.driver = driver


    def parse_label(self, index):
        labelname = self.name
        labelpos = 2.54 * index
        parsed = f'''
(label "{labelname}"
	(at 0.0 {labelpos} 180)
	(effects
		(font (size 1.27 1.27))
		(justify right bottom)
	)
	(uuid "56f4fb89-7b4a-4f69-8ef8-85994935da29")
)
'''
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

            print(f"Write file: {filepath}")

            # filepath = f'./build/{filename}.kicad_labels'
            fd = open(filepath, 'w+', encoding='utf-8')
            fd.write(unit_text)
            fd.flush()
            fd.close()

        #         unit_list.append(pin.unit)
        #         unit_list[pin.unit] = ""
        #     else:
        #         unit_list[pin.unit] = unit_list[pin.unit] + '; ' + pin.name

        # for unit_name in unit_list:
        #     
        #     print(f"TEST: Unit_name: {filename}")
                
#                 parsed = f'''
# (label "{labelname}"
# 	(at {labelpos} 0.0 180)
# 	(effects
# 		(font (size 1.27 1.27))
# 		(justify right bottom)
# 	)
# 	(uuid "56f4fb89-7b4a-4f69-8ef8-85994935da29")
# )
#         '''


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
    f = open (filepath, 'r', encoding='utf-8')
    text = f.read()
    f.close()
    i = 0
    Pins = []
    for line in text.splitlines():
        if i == 0:
            i = 1
            continue
        # if line.strip(';').strip() == "":
        #     continue
        splits = line.split(';')
        # Excel structure to parse:
        if (len(splits) < 14) : 
            print("ERROR: Excel list must be of format:")
            print("block; pin_id; pin_prefix; function0(system); direction0; function1; direction1; function2; direction2; function3; direction3; voltage; capabilities; original_name;	info")
            exit(-1)

        function = []
        driver = []
        # print("line={}".format(line))
        # for s in splits:
        #     print("\t{}".format(s))
        block = splits[0].strip()
        pin_id = splits[1].strip()
        pin_prefix = splits[2].strip()
        function.append(splits[3].strip())
        driver.append(splits[4].strip())
        function.append(splits[5].strip())
        driver.append(splits[6].strip())
        function.append(splits[7].strip())
        driver.append(splits[8].strip())
        function.append(splits[9].strip())
        driver.append(splits[10].strip())
        voltage = splits[11].strip()
        capabilities  = splits[12].strip()
        orig_name = splits[13].strip()
        info = splits[14].strip()



        name = pin_prefix.lower()
        for f in function[1:]:
            if f != "":
                if name == "":
                    name += f.lower()
                else:
                    name += "_" + f.lower()
        if function[0] != "":
            if name == "":
                name += function[0].lower()
            else:
                name += '_' + function[0].lower()
        
        # take the first driver found for time being!
        driver_full = ""
        for d in driver:
            if d != "":
                driver_full = d.lower()
                break
        
        if (name == "" and block == "" and pin_id == ""):
            continue
        print("pin_id={}; block={}; name={}; driver={}".format( pin_id, block, name, driver))
        pin = SymbolPin(pin_id, block, name, driver_full)
        i = i + 1
        Pos = Vec3(-2.54, -1.27 + i* -2.54, 0)
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



if __name__ == "__main__":
    main()

