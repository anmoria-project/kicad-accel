import random

class Vec3:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
    def parse(self):
        return f'{self.x} {self.y} {self.z}'

def get_rand():
    # Example: 98da213c-75d0-49c4-be2f-abf6ce88cee6
	rand_str = ''
	for i in range(0, 6):
		num = random.randint(0, 2**32-1)
		if i == 0:
			rand_str = f"{num:08x}"[-9:-1]
		elif i == 1:
			rand_str = rand_str + "-" + f"{num:04x}"[-5:-1]
		elif i == 2:
			rand_str = rand_str + "-" + f"{num:04x}"[-5:-1]
		elif i == 3:
			rand_str = rand_str + "-" + f"{num:04x}"[-5:-1]
		elif i == 4:
			rand_str = rand_str + "-de" + f"{num:08x}"[-9:-1]
	return rand_str
	
    	

def indent(string, num_spaces):
    ret_str = ""
    for line in string.splitlines() :
        ret_str = ret_str + '\t' * num_spaces + line + '\n'
    return ret_str



def parse_hierarchical_label(name, xpos, ypos, rotation):
	parsed = f'''\
(hierarchical_label "{name}"
	(shape input)
	(at {xpos:.2f} {ypos:.2f} {rotation})
	(effects
		(font (size 1.27 1.27))
		(justify left)
	)
	(uuid "98da213c-75d0-49c4-be2f-abf6ce88cee6")
)
'''
	return parsed

def parse_label(name, xpos, ypos, rotation, align="right"):
	parsed = f'''\
(label "{name}"
	(at {xpos:.2f} {ypos:.2f} {rotation})
	(effects
		(font (size 1.27 1.27))
		(justify {align})
	)
	(uuid "98da213c-75d0-49c4-be2f-abf6ce88cee6")
)
'''
	return parsed


def parse_wire(xpos1, ypos1, xpos2, ypos2):
	parsed = f'''\
(wire
	(pts
		(xy {xpos1:.2f} {ypos1:.2f}) (xy {xpos2:.2f} {ypos2:.2f})
	)
	(stroke (width 0) (type default))
	(uuid "db7b9210-9629-46ea-9e4f-90bda630665f")
)
'''
	return parsed

def parse_schematic_symbol(device, xpos, ypos, rotation, value):
	parsed = f'''\
(symbol
	(lib_id "Device:{device}")
	(at {xpos:.2f} {ypos:.2f} {rotation})
	(unit 1)
	(exclude_from_sim no)
	(in_bom yes)
	(on_board yes)
	(dnp no)
	(fields_autoplaced yes)
	(uuid "24b36077-41b9-424d-9cfb-461eded128a1")
	(property "Reference" "R2"
		(at {xpos:.2f} {ypos:.2f} 90)
		(effects
			(font (size 1.016 1.016))
			(hide yes)
		)
	)
	(property "Value" "{value}"
		(at {xpos:.2f} {ypos:.2f} 90)
		(effects
			(font (size 1.27 1.27))
			(hide yes)
		)
	)
	(property "Footprint" ""
		(at {xpos:.2f} {ypos:.2f} 0)
		(effects
			(font (size 1.27 1.27))
			(hide yes)
		)
	)
	(property "Datasheet" "~"
		(at {xpos:.2f} {ypos:.2f} 0)
		(effects
			(font (size 1.27 1.27))
			(hide yes)
		)
	)
	(property "Description" ""
		(at {xpos:.2f} {ypos:.2f} 0)
		(effects
			(font (size 1.27 1.27))
			(hide yes)
		)
	)
	(pin "2"
		(uuid "797aac82-9cef-47da-9779-e734b0ccadb2")
	)
	(pin "1"
		(uuid "0f63ff17-2eab-4a06-9601-d66a851c0ccf")
	)
	(instances
		(project "design1"
			(path ""
				(reference "R2")
				(unit 1)
			)
		)
	)
)
'''
	return parsed

def parse_busentry(xpos, ypos):
	parsed = f'''\
(bus_entry
	(at {xpos:.2f} {ypos:.2f})
	(size 2.54 2.54)
	(size 2.54 -2.54)
	(stroke (width 0) (type default))
	(uuid "6f5e384e-5a9e-4fdc-8642-9701db9306b8")
)
'''
	return parsed

def parse_hierarchical_label(label, xpos, ypos, rotation = 180):
	parsed = f'''\
(hierarchical_label "{label}"
	(shape input)
	(at {xpos:.2f} {ypos:.2f} {rotation})
	(effects
		(font (size 1.27 1.27))
		(justify right)
	)
	(uuid "4c0bf617-3b88-48c0-8c27-7bef631db9a0")
)
'''
	return parsed

def parse_bus(xpos1, ypos1, xpos2, ypos2):
	parsed = f'''\
(bus
	(pts
		(xy {xpos1:.2f} {ypos1:.2f}) (xy {xpos2:.2f} {ypos2:.2f})
	)
	(stroke (width 0) (type default))
	(uuid "90fa7227-5737-479c-9573-d260690ffe83")
)
'''
	return parsed

def parse_symboleditor_symbol(symbol_name, unit_names, pins):

	max_char = 0
	for pin in pins:
		if max_char < len(pin.name):
			max_char = len(pin.name)
	if max_char < 10: max_char = 10
	rect_x = (max_char + 1) * 2.54 * 0.7
	
	parsed = f'''\
(symbol "{symbol_name}"
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
	(symbol "{symbol_name}_0_1"
		(text "{symbol_name}"
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


	if len(unit_names) > 1:
		unit_id = 0
		for unit_name in unit_names:
			num_unit_pins = 0
			for pin in pins:
				if pin.unit == unit_name:
					num_unit_pins = num_unit_pins + 1
			unit_id = unit_id + 1
			parsed = parsed + f'''
	(symbol "{symbol_name}_{unit_id}_1"
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
			for pin in pins:
				if unit_name != pin.unit:
					continue
				pin_pos = Vec3(0, -1.27 + unit_pin_id * -2.54, 0)
				parsed = parsed + indent(pin.parse(pin_pos), 2)
				unit_pin_id = unit_pin_id + 1
			parsed = parsed + '\t)'

	return parsed

def parse_library(symbols):
	parsed = f'''
(kicad_symbol_lib
	(version 20241209)
	(generator "kicad_symbol_editor")
	(generator_version "9.0")
'''
	for symbol in symbols:
		parsed = parsed + indent(symbol.parse(), 1)
	parsed = parsed + f'\
\t\t(embedded_fonts no)\n\
\t)\n\
)\n\
\n'
	return parsed

def parse_pin(name, driver, pos, ic_pin):
	parsed = f'\
(pin {driver} line\n\
\t(at {pos.parse()})\n\
\t(length 5.04)\n\
\t(name "{name}"\n\
\t\t(effects\n\
\t\t\t(font\n\
\t\t\t\t(size 1.27 1.27)\n\
\t\t\t)\n\
\t\t)\n\
\t)\n\
\t(number "{ic_pin}"\n\
\t\t(effects\n\
\t\t\t(font\n\
\t\t\t\t(size 1.27 1.27)\n\
\t\t\t)\n\
\t\t)\n\
\t)\n\
)\n\
'
	return parsed