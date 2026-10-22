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
import re
from parser_lib import *
from logger import *
from bus_defines import *
import csv
from package_defines import footprints
from pathlib import Path

import kicad_symbol_generator as kigen

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






class SymbolPin:
    pindrivers = kicad_drivers
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
        'dio' : 'bidirectional',
        'ci' : 'input',
        'co': 'output',
        'cio' : 'bidirectional',
    } | bus_pin_drivers

    powersymbols = ['+3v3', 'gnd', 'self', 'ext']
    term_subst = {
        'pf:':'e-12f:',
        'nf:':'e-9f:',
        'uf:':'e-6f:',
        'ph:':'e-12h:',
        'nh:':'e-9h:',
        'uh:':'e-6h:',
        'kr:':'e3r:',
        'gr:':'e9r:',
    }

    def __init__(self, ic_pin, unit, name, driver_raw, termination_str):
        self.ic_pin = ic_pin
        self.name = name
        self.unit = unit
        self.driver = ''
        self.driver_raw = driver_raw
        self.terminations = []
        self.connections = []
        self.hasExtTermination = False
        self.hasSelfTermination = False

        ## DRIVER STUFF

        # Add substitution for lazy driver keys
        # TODO: Remove backwards compatibility when finished with this here...
        driver = re.sub(r'\[[0-9]+\]', '', driver_raw).lower().replace('.', '_')
        found = False
        for key in self.driver_subst.keys():
            key_legacy = key.replace('.', '_')
            if driver == key_legacy:
                driver = self.driver_subst[key]
                found = True
                break

        if driver not in kicad_drivers:
            log(log_error, f"Undefined or missing PinDriver: '{driver}'! Name={name}; Block={unit}; PIN={ic_pin}")
            exit(1)
        self.driver = driver
        # self.terminations = terminations


        ## TERMINATION STUFF

        # For some weird reason there are some ticks in the excel stuff. Goddam excel...
        term_str = termination_str.lower().replace(' ', '').replace('"', '')
        for k, v, in self.term_subst.items():
            if term_str.find(k) != -1:
                log(log_note, f"Replace termination '{k}' with '{v}'")
                term_str = term_str.replace(k, v)


        for term in term_str.split(','):
            term = term.strip()
            if term == '':
                continue

            if term.lower().find(':') == -1:
                conn = term.lower()
                self.connections.append(conn)
                log(log_error, f"Simple connections are not allowed right now. Please use 0.0R Resistor ect to connect! Pin={self.ic_pin}")
                exit(-1)
            else:
                # Split termination Example: 20.0e+3R:+3v3
                try:
                    tmp, driver= term.lower().split(":")
                    float_raw = tmp[0:-1]
                    component = tmp[-1]
                    value = float(float_raw)
                except:
                    log(log_error, f"Could not extract data from Termination field: '{term}'. Pin='{self.ic_pin}', Driver={driver}")
                    exit(-1)


                # if (component not in ['C', 'L', 'R'])
                log(log_note, f"Termination: Type={component}; Value={value}; Driver={driver}")
                termination = [component, value, driver]
                if driver.lower() not in self.powersymbols:
                    log(log_note, f"Termination unknown: {driver}")
                    # print(f"Termination driver for pin {self.ic_pin} unkown: {driver}")

                    # exit(-1)
                self.terminations.append(termination)

        if ':self' in termination_str:
            self.hasSelfTermination = True
        else:
            self.hasSelfTermination = False

        if ':ext' in termination_str:
            self.hasExtTermination = True
        else:
            self.hasExtTermination = False


    def parse_label(self, index):

        if self.hasSelfTermination and self.hasExtTermination:
            labelname = '__' + self.name
        elif self.hasExtTermination or self.hasSelfTermination:
            labelname = '_' + self.name
        else:
            labelname = self.name
        labelpos = 2.54 * index
        # NOTE: Check, was 'right bottom'
        parsed = parse_label(labelname, 0.0, labelpos, 180, "right")
        return parsed

    def parse_connection(self, place_position_index, index, xoff):
        driver = self.connections[index].lower()

        # TODO: Recheck here. This might be wrong now...
        if self.hasSelfTermination:
            label = '_' + self.name
        else:
            label = '_' + self.name

        ypos = place_position_index * 2.54

        parsed = ''
        parsed = parsed + parse_label(driver, 5.08 + xoff, ypos, 0, "left")
        parsed = parsed + parse_wire(5.08 + xoff, ypos, 0.0, ypos)
        parsed = parsed + parse_label(label, 0.0 + xoff, ypos, 180, "right")

        return parsed

    def parse_termination(self, place_position_index, index, xoff = 0.0):
        driver = self.terminations[index][2].lower()
        value = self.terminations[index][1]
        device = "UNDEFINED"

        if self.hasExtTermination:
            label = '_' + self.name
        else:
            label = self.name



        if (driver == 'self') and self.hasExtTermination:
            driver = '__' + self.name
        elif (driver == 'self'):
            driver = '_' + self.name
        elif (driver == 'ext'):
            driver = self.name
        else:
            driver = self.terminations[index][2]

        component = self.terminations[index][0].upper()



        # if (component == "short"):
        #     device = "W_Small"
        ref_value = 99999
        if (component == 'R'):
            device = "R_Small"
            reference = f'R{ref_value}'
        elif (component == 'C') or (component == "F"):
            device = "C_Small"
            reference = f'C{ref_value}'
        elif (component == 'L') or (component == "H"):
            device = "L_Small"
            reference = f'L{ref_value}'
        elif (component == "X"):
            device = "FerriteBead_Small"
            reference = f'FB{ref_value}'
        else:
            log(log_error, f"Termination component unknown: Pin={self.ic_pin}; Component={component}!")
            exit(-1)
        ypos = place_position_index * 2.54

        parsed = ''
        parsed = parsed + parse_label(driver, 5.08 + xoff, ypos, 0, "left")
        # parsed = parsed + parse_hierarchical_label(driver, 5.08, ypos, 0)
        parsed = parsed + parse_schematic_symbol(device, 2.54 + xoff,  ypos, 270, value, reference)
        parsed = parsed + parse_label(label, 0.0 + xoff, ypos, 180, "right")

        return parsed

    def parse(self, pos):
        return parse_pin(self.name, self.driver, pos, self.ic_pin)


class Symbol:

    def __init__(self, name):
        self.name = name
        self.pins = []
        self.unit_names = []
        self.meta = []

    def add_pins(self, pins):
        for pin in pins:
            if pin.unit not in self.unit_names:
                self.unit_names.append(pin.unit)
            self.pins.append(pin)

    def substitute_footprint(self):
        fp = self.meta['footprint']
        if not fp in footprints.keys():
            log(log_error, f"Footprint is not known! footprint={fp}! Please add footprint to package_defines.py!")
            exit(-1)
        self.meta['footprint'] = footprints[fp]['full_name']

    def add_meta(self, meta):
        keys_replace = {'package': 'footprint', 'component':'value'}
        keys_found = []
        meta_primary = {
            "footprint": "footprint-text",
            "value": "value-text"}
        meta_optional = {
            "datasheet" : "datasheet-text",
            "description": "description-text"}
        for key, val in meta.items():
            if key in keys_replace:
                key_old = key
                key = keys_replace[key]
                log(log_note, f"Replace 'meta' key '{key_old}' with '{key}'")
            if key in meta_primary.keys():
                meta_primary[key] = val
                log(log_debug, f"Add key '{key}' with value = '{val}' to meta_primary!")
            elif key in meta_optional.keys():
                meta_optional[key] = val
                log(log_debug, f"Add key '{key}' with value = '{val}' to meta_optional!")
            else:
                log(log_warn, f"Found key='{key}' in 'meta' which is unknown! Key will be ignored!")
            keys_found.append(key)
        for key in meta_primary.keys():
            if key not in keys_found:
                log(log_error, f"Missing meta-key='{key} in 'meta' row!")
                exit(-1)
        self.meta = meta_primary | meta_optional

        self.substitute_footprint()


    def compress_busnames(self, bussignals):
        busdict = {}
        for bs in bussignals:
            key = re.sub(r'\d+$', '', bs)
            val_raw = bs.replace(key, '')
            if val_raw.isdigit():
                val = int(val_raw)
            else:
                val = None
            if key not in busdict.keys():
                busdict[key] = []
            if val != None:
                busdict[key].append(val)

        compressed = ''
        for k, l in busdict.items():

            if len(l) == 0:
                compressed = compressed + f' {k}'
                continue
            else:
                l.sort()
                # While continous, add... otherwise add to bussignals
                last = None
                start = l[0]
                # compressed = compressed + f' {k}[{l[0]}'
                for i in l:

                    if l[-1] == i:
                        lastid = True
                    else:
                        lastid = False

                    if i-1 != last and last != None:
                        discontinuity = True
                    else:
                        discontinuity = False

                    if discontinuity:
                        if start == last:
                            compressed = compressed + f" {k}{last}"
                        else:
                            compressed = compressed + f" {k}[{start}..{last}]"
                        start = i
                    last = i
                if start == last:
                    compressed = compressed + f" {k}{last}"
                else:
                    compressed = compressed + f" {k}[{start}..{last}]"

        return compressed.strip(' ')

    def parse_busses(self, dirpath, filename):
        # TODO: Add some error check for double define bus signals ect.
        bus_drivers = {}
        for pin in self.pins:
            for bus in bus_list:
                for drivertype in bus:
                    busdriver = drivertype.name.replace('[x]', '').lower().replace('.', '_')
                    pindriver = re.sub(r'\[[0-9]+\]', '', pin.driver_raw).lower().replace('.', '_')
                    if pindriver == busdriver:
                        bus_drivers[pin.driver_raw] = pin.name
                    else:
                        # print(f"Missmatch: {pindriver}:{busdriver}")
                        pass

        xpos = 2.54 * 20
        ypos1 = 0 # actual
        ypos2 = 2.54 # next
        busname_tmp = ''
        bussignals = []
        bus_drivers = dict(sorted(bus_drivers.items()))
        parsed=''
        number_found_busses = 0
        last = False
        last_cnt = 0
        for buskey_raw, signal in bus_drivers.items():
            last_cnt  = last_cnt + 1
            if (last_cnt == len(bus_drivers)): last = True
            buskey = buskey_raw.replace('[', '').replace(']', '')
            # print(buskey)
            busname, bussignal = buskey.split('.')

            log(log_debug, f'Found bus: {busname} with pin {bussignal} with signal {signal}')

            is_new_bus = (busname != busname_tmp and not busname_tmp == '')
            if is_new_bus:
                number_found_busses = number_found_busses + 1
                # bussignalsstr = " ".join(bussignals)
                bussignalsstr = self.compress_busnames(bussignals)
                busname_full = busname_tmp + f'{{ {bussignalsstr} }}'
                # NOTE: Kicad needs additional space, otherwise the signals will be ignored
                parsed = parsed + parse_hierarchical_label(busname_full, xpos-2.54, ypos2, 180)
                bussignals = []
                ypos1 = ypos2 + 4*2.54
                ypos2 = ypos1 + 2.54
            if last:
                number_found_busses = number_found_busses + 1


            # bussignals = bussignals + ' ' + bussignal
            bussignals.append(bussignal)

            parsed = parsed + parse_label(buskey, xpos, ypos1, 0, 'left')
            parsed = parsed + parse_bus(xpos-2.54, ypos2, xpos-2.54, ypos2+2.54)
            parsed = parsed + parse_busentry(xpos-2.54, ypos2)

            # Also generate the wire mapping of the target bus and real signal name
            parsed = parsed + parse_label(signal, xpos - 16 * 2.54, ypos1, 180, 'right')
            parsed = parsed + parse_wire(xpos - 15 * 2.54, ypos1, xpos - 16 * 2.54, ypos1)
            parsed = parsed + parse_label(buskey, xpos - 15 * 2.54, ypos1, 0, 'left')

            ypos1 = ypos2
            ypos2 = ypos1 + 2.54
            busname_tmp = busname

        # bussignals = bussignals.strip(" ")
        if number_found_busses == 0:
            return



        bussignalsstr = bussignalsstr = self.compress_busnames(bussignals)
        busname_full = busname + f'{{ {bussignalsstr} }}'
        parsed = parsed + parse_hierarchical_label(busname_full, xpos-2.54, ypos2, 180)

        filepath = f"{dirpath}/{filename}.kicad_busses"
        log(log_note, f"Write file: {filepath}")

        fd = open(filepath, 'w+', encoding='utf-8')
        fd.write(parsed)
        fd.flush()
        fd.close()


    def parse_labels(self, dirpath, filename):
        unit_text_all = ""
        i_all = 0
        term_pos_index_all = 0
        term_index_all = 0
        conn_index_all = 0
        for unit in self.unit_names:
            i = 0
            if (term_pos_index_all < i_all) :
                term_pos_index_all = i_all
            unit_text = ""
            filepath = f"{dirpath}/{filename}_{unit}.kicad_labels"
            for pin in self.pins:
                if pin.unit != unit:
                    continue
                i = i + 1
                i_all = i_all + 1
                unit_text  = unit_text + "\n\n" + pin.parse_label(i)
                unit_text_all  = unit_text_all + "\n\n" + pin.parse_label(i_all)

            term_pos_index = 0

            for pin in self.pins:
                term_index = 0
                conn_index = 0
                if pin.unit != unit:
                    continue
                for id in range(0, len(pin.terminations)):
                    #     def parse_termination(self, place_position_index, index, label):
                    unit_text  = unit_text + "\n\n" + pin.parse_termination(term_pos_index, term_index, -30 * 2.54)
                    unit_text_all = unit_text_all + "\n\n" + pin.parse_termination(term_pos_index_all, term_index, -30 * 2.54)
                    term_pos_index = term_pos_index + 1
                    term_pos_index_all = term_pos_index_all + 1
                    term_index_all = term_index_all + 1
                    term_index = term_index + 1
                for id in range(0, len(pin.connections)):
                    unit_text  = unit_text + "\n\n" + pin.parse_connection(term_pos_index, conn_index)
                    unit_text_all  = unit_text_all + "\n\n" + pin.parse_connection(term_pos_index_all, conn_index_all)
                    term_pos_index = term_pos_index + 1
                    term_pos_index_all = term_pos_index_all + 1
                    conn_index = conn_index + 1
                    conn_index_all = conn_index_all + 1

            log(log_note, f"Write file: {filepath}")

            # filepath = f'./output/{filename}.kicad_labels'
            fd = open(filepath, 'w+', encoding='utf-8')
            fd.write(unit_text)
            fd.flush()
            fd.close()
            # unit_text_all = unit_text_all + unit_text
        filepath = f"{dirpath}/{filename}_allblocks.kicad_labels"
        fd = open(filepath, 'w+', encoding='utf-8')
        fd.write(unit_text_all)
        fd.flush()
        fd.close()

    def parse(self):

        return parse_symboleditor_symbol(self.name, self.unit_names, self.pins, self.meta)



class Library:
    def __init__(self, name, filepath, use_simple_paths):
        self.name = name
        self.symbols = []
        self.filepath = filepath
        self.use_simple_paths = use_simple_paths

    def add_symbols(self, symbols):
        for symbol in symbols:
            self.symbols.append(symbol)

    def parse_labels(self):
        for symbol in self.symbols:
            dirpath = Path(self.filepath).parent.name
            if self.use_simple_paths:
                filename = symbol.name
            else:
                filename = self.name + "__" + symbol.name
            symbol.parse_labels(dirpath, filename)
            symbol.parse_busses(dirpath, filename)

    def parse(self):
        return parse_library(self.symbols)

    def prepare_kigen_pins(self, Pins):
        PinList = []
        Units = {}
        for pin in Pins:
            if not pin.unit in Units.keys():
                Units[pin.unit] = len(Units)
            PinList.append([pin.name, pin.driver, Units[pin.unit]])
        PinList.sort(key=lambda x:x[2])
        return PinList


    def gen_file_kigen(self):
        filepath = self.filepath

        for symbol in self.symbols:
            pin_list = self.prepare_kigen_pins(symbol.pins)
            kigen.update_symbol(symbol.name, pin_list, filepath)
        log(log_note, "Write file: " + filepath)

    ## Deprecated: Marked for removal
    # def gen_file_old(self):
    #     filepath = f'./output/{self.name}.kicad_sym'
    #     f_lib = open(filepath, 'w+', encoding='utf-8')
    #     f_lib.write(self.parse())
    #     f_lib.flush()
    #     f_lib.close()
    #     log(log_note, "Generated file: " + filepath)


    def gen_file(self):
        self.gen_file_kigen()


# def gen_labels_file(self):

def apply_shared_terminations(Pins):
    term_dict_self = {}
    term_dict_ext = {}
    ProcessedPins = []
    for pin in Pins:

        if not pin.name in term_dict_self.keys():
            term_dict_self[pin.name] = False

        if not pin.name in term_dict_ext.keys():
            term_dict_ext[pin.name] = False

        if pin.hasSelfTermination :
            term_dict_self[pin.name] = True

        if pin.hasExtTermination:
            term_dict_ext[pin.name] = True

    # Apply terminations for all same ned pins...
    for pin in Pins:
        if term_dict_self[pin.name]:
            pin.hasSelfTermination = True
        if term_dict_ext[pin.name]:
            pin.hasExtTermination = True
        ProcessedPins.append(pin)
    return ProcessedPins

def check_sanity_csv(text, seperator = ";"):
    cnt_semi = text.count(';')
    cnt_comma = text.count(',')
    cnt_tab = text.count('\t')

    log(log_debug, f"Count semi={cnt_semi}, comma={cnt_comma}, tabs={cnt_tab}")

    if cnt_semi > cnt_comma and cnt_semi > cnt_tab:
        seperator = ';'
    elif cnt_comma > cnt_tab:
        seperator = ','
    else:
        seperator = '\t'

    if seperator == ',':
        log(log_error, "CSV uses seperator ',' which is forbidden! Please change the CSV to ';' or tab as seperator!")
        exit(-1)
    log(log_note, f"Selected seperator for .csv file: '{seperator}'")




def csv2kv(filepath, column_name, seperator = ";"):

    keys_found = {}

    with open (filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=seperator)
        # print(f"DBG: Fieldnames: [{reader.fieldnames}]")
        if not column_name in reader.fieldnames:
            log(log_error, f"CSV does not have column named '{column_name}'")
            exit(-1)
        meta_cells = [row[column_name] for row in reader]

        for cell in meta_cells:
            if cell.strip() == '':
                continue
            if  cell.count("=") == 0:
                log(log_error, "Entry in 'meta' row does not have proper 'key=value' pair!")
            key_value = cell.split("=", 1)
            key = key_value[0].strip()
            val = key_value[1].strip()
            if key in keys_found.keys():
                log(log_error, "Found double defined key in 'meta' row!")
            keys_found[key] = val

    return keys_found


def csv2pins(filepath, seperator = ";"):
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
                    "notes": -1,
                    "meta": -1
    }


    f = open (filepath, 'r', encoding='utf-8')
    text = f.read()
    f.close()
    i = 0
    Pins = []
    line_id = 0
    lines = text.split('\n')

    check_sanity_csv(text, seperator)

    # NOTE: Autodetect column position
    col_id = 0
    for key in lines[0].split(seperator):
        key = key.strip()
        if key == '': continue
        # print(f"Found key: {key}")
        if key in cols_primary.keys():
            log(log_note, f"KEY '{key}' found in primary keys!")
            if cols_primary[key] != -1:
                log(log_error, f"Column '{key}' is already defined!")
                exit(1)
            cols_primary[key] = col_id
        elif key in cols_optional:
            if cols_optional[key] != -1:
                log(log_error, f"Column '{key}' is already defined!")
                exit(1)
            log(log_note, f"KEY '{key}' found in optional keys!")
            cols_optional[key] = col_id
        else:
            log(log_warn, f"Column '{key}' is unknown and will be ignored: {key}")
        col_id  = col_id +1

    # NOTE: Check for missing keys
    for key, val in cols_primary.items():
        if val == -1:
            log(log_error, f"Column '{key}' is missing!")
            exit(-1)



    col_ids = {}
    col_ids.update({k: v for k, v in cols_primary.items() if v != -1})
    col_ids.update({k: v for k, v in cols_optional.items() if v != -1})


    used_function_keys = []
    for k, v in col_ids.items():
        if k.startswith('function') and v > 0:
            used_function_keys.append(k)
    used_function_keys.sort()

    used_blocks = []

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

        # Lets add the function0 stuff on the back, so main functionality is centered!
        for fkt in used_function_keys:
            if fkt == 'function0':
                continue
            subfkt = splits[col_ids[fkt]].strip()
            if subfkt == '':
                continue
            if name == '':
                name = subfkt
            else:
                name = name + '__' + subfkt
        subfkt0 = splits[col_ids['function0']].strip()
        if name == '':
            name = subfkt0
        else:
            name = name + "__" + subfkt0 if (subfkt0 != '') else name


        # NOTE: Driver1 overrides driver0. This must be changed in kicad source code to support multiple drivers!
        driver = ''
        if splits[col_ids['driver1']].strip() != '' :
            driver = driver + splits[col_ids['driver1']].strip()
        elif splits[col_ids['driver0']].strip() != '' :
            driver = driver + splits[col_ids['driver0']].strip()

        if (name == "" and block == "" and pin_id == ""):
            continue
        log(log_debug, "pin_id={}; block={}; name={}; driver={}".format( pin_id, block, name, driver))
        pin = SymbolPin(pin_id, block, name, driver, termination_str)
        if block not in used_blocks:
            used_blocks.append(block)
        i = i + 1
        # Pos = Vec3(-2.54, -1.27 + i* -2.54, 0)
        Pins.append(pin)
    if len(used_blocks) < 2:
        log(log_error, "Number of used blocks must be at least 2! Please add another block (f.e. split function and power)")
        exit(-1)

    # Check if connector have multiple same pins. Activate Terminations
    ProcessedPins = apply_shared_terminations(Pins)

    return ProcessedPins


def print_license_short():
    license = f'''
Symbol-generator v{version}
Copyright (C) 2026  Johann A. Sollacher
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
'''
    print(license)

import argparse

def parse_args():

    parser = argparse.ArgumentParser(
        description='''
Kicad-Accel[erator] Symbol Generator/Parser
Generate .csv files into kicad symbol and schematic components''',
        epilog='''
Example: ./symbol-generator.py a.csv b.csv -o lib.kicad_sym

Notes:
    - Libraries are appended, not overwritten. Compiling one .csv at a time is recommended!
    - Use Makefile/C-like style for compilation!
    - For license information execute -v!

WARN:
    - Library compile can fail and destroy handwritten content in same library.
    - Do source-control your libraries (handwritten) and input sources (.csv)!
    - Keep generated and handwritten libraries strictly seperate!
    - Clean/remove and regenerate your libraries often!
''',
    formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "inputs", nargs="+", help="One or multiple "
    )
    parser.add_argument(
        "-o", required=True, help="Output: Kicad library .kicad_sym"
    )
    parser.add_argument("-v", help="Print License information")


    parser.add_argument(
        "--simple-paths", action = "store_true", help="Do NOT extend .kicad_bus and .[all]blocks with library name"
    )

    args = parser.parse_args()

    if args.v:
        print_license_short()
        exit(0)


    LibPath = Path(args.o)

    if not re.fullmatch("[a-zA-Z0-9_/-]+.kicad_sym", LibPath.name):
        log(log_error, "Bad Argument '-o'! Symbol/Filename must end with .kicad_sym!")
        exit(1)

    if not LibPath.parent.is_dir():
        log(log_error, f"Bad Argument '-o'! Directory must exist: {LibPath.parent}")
        exit(1)
    LibPath = LibPath.resolve()


    inputFilepaths = []

    for fp in args.inputs:
        if not Path(fp).is_file() or not fp.endswith(".csv"):
            log(log_error, f"Input file needs to exist and end with .csv: {fp}!")
            exit(-1)
        log(log_note, f"Found file for processing: {fp}")
        inputFilepaths.append(Path(fp).resolve())

    return LibPath, inputFilepaths, args.simple_paths


def main():
    # TODO: Add switch for argument...
    global log_level_system
    log_level_system = log_note
    # DO NOT REMOVE!
    print("\n###\nSymbol-generator (Kicad-Accel): For version or license use '-v'. For help use '-h'\n###\n")

    LibPath, InFilepaths, useSimplePaths = parse_args()

    LibName = LibPath.name.replace('.kicad_sym', '')

    lib = Library(LibName, str(LibPath), useSimplePaths)
    SymbolList = []
    for fp in InFilepaths:
        sym_name = os.path.basename(fp).split('.')[0]
        sym = Symbol(sym_name)
        pins = csv2pins(fp)
        sym.add_pins(pins)
        SymbolList.append(sym)

    lib.add_symbols(SymbolList)
    lib.gen_file()
    lib.parse_labels()


if __name__ == "__main__":
    main()

