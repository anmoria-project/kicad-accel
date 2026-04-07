import random


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
	
    	





def parse_hierarchical_label(name, xpos, ypos, rotation):
	parsed = f'''\
(hierarchical_label "{name}"
	(shape input)
	(at {xpos} {ypos} {rotation})
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
	(at {xpos} {ypos} {rotation})
	(effects
		(font (size 1.27 1.27))
		(justify {align})
	)
	(uuid "98da213c-75d0-49c4-be2f-abf6ce88cee6")
)
'''
	return parsed


def parse_wire(name, xpos1, ypos1, xpos2, ypos2):
	parsed = f'''\
(wire
	(pts
		(xy {xpos1} {ypos1}) (xy {xpos2} {ypos2})
	)
	(stroke (width 0) (type default))
	(uuid "db7b9210-9629-46ea-9e4f-90bda630665f")
)
'''
	return parsed

def parse_symbol(device, xpos, ypos, rotation, value):
	parsed = f'''\
(symbol
	(lib_id "Device:{device}")
	(at {xpos} {ypos} {rotation})
	(unit 1)
	(exclude_from_sim no)
	(in_bom yes)
	(on_board yes)
	(dnp no)
	(fields_autoplaced yes)
	(uuid "24b36077-41b9-424d-9cfb-461eded128a1")
	(property "Reference" "R2"
		(at {xpos} {ypos} 90)
		(effects
			(font (size 1.016 1.016))
			(hide yes)
		)
	)
	(property "Value" "{value}"
		(at {xpos} {ypos} 90)
		(effects
			(font (size 1.27 1.27))
			(hide yes)
		)
	)
	(property "Footprint" ""
		(at {xpos} {ypos} 0)
		(effects
			(font (size 1.27 1.27))
			(hide yes)
		)
	)
	(property "Datasheet" "~"
		(at {xpos} {ypos} 0)
		(effects
			(font (size 1.27 1.27))
			(hide yes)
		)
	)
	(property "Description" ""
		(at {xpos} {ypos} 0)
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
	(at {xpos} {ypos})
	(size 2.54 2.54)
	(stroke (width 0) (type default))
	(uuid "6f5e384e-5a9e-4fdc-8642-9701db9306b8")
)
'''

def parse_hierarchical_label(label, xpos, ypos, rotation = 180):
	parsed = '''\
(hierarchical_label "{label}"
	(shape input)
	(at {xpos} {ypos} {rotation})
	(effects
		(font (size 1.27 1.27))
		(justify right)
	)
	(uuid "4c0bf617-3b88-48c0-8c27-7bef631db9a0")
)
'''
	return parsed

def parse_bus(xpos1, ypos1, xpos2, ypos2):
	parsed = '''\
(bus
	(pts
		(xy {xpos1} {ypos1}) (xy {xpos2} {ypos2})
	)
	(stroke (width 0) (type default))
	(uuid "90fa7227-5737-479c-9573-d260690ffe83")
)
'''
	return parsed