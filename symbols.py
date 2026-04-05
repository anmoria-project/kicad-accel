

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

