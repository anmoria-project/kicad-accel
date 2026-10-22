from kiutils.symbol import SymbolLib, Symbol
from kiutils.items.common import Position, Stroke
from kiutils.items.syitems import SyRect, Fill
from kiutils.symbol import SymbolPin

from logger import *

from pathlib import Path

def generate_lib1():

    lib = SymbolLib(
        version = "20250114",
        generator="kicad_symbol_generator",
    )

    # Create symbol and default props
    symbol = Symbol.create_new(
        id = "Symbol1",
        reference="U",
        value="Value1"
    )

    # Kicad symbol normally contains child unit called 'MyComponent_0_1' (graphics and pins)
    # unit=symbol.units[0]

    unit = Symbol(
        entryName="Symbol1",
        unitId=0,
        styleId=1,
    )
    symbol.units.append(unit)

    # Draw
    unit.graphicItems.append(
        SyRect(
            start=Position(X=-2.54, Y=2.54),
            end=Position(2.54, 2.54),
            stroke=Stroke(width=0, type="default"),
            fill=Fill(type="background"),
            )
    )


    # Add two pins
    unit.pins.extend([
        SymbolPin(
            electricalType="input",
            graphicalStyle="line",
            position=Position(5.08, 0.0, angle=0),
            length=2.54,
            name="IN",
            number="1",

        ),
    SymbolPin(
            electricalType="output",
            graphicalStyle="line",
            position=Position(2*5.08, 0.0, angle=0),
            length=2.54,
            name="OUT",
            number="2",
        ),
    ])

    lib.symbols.append(symbol)
    lib.to_file("Lib1.kicad_sym")

def generate_lib():

    lib = SymbolLib(
        version = "20250114",
        generator="kicad_symbol_generator",
    )
    return lib

def add_symbol(name, num_units, value = "Value1"):

    # Create symbol and default props
    symbol = Symbol.create_new(
        id = name,
        reference="U",
        value=value
    )
    units = []
    if num_units > 1:
        offset = 1
    else:
        offset = 0
    for i in range(0, num_units):
        unit = Symbol(
            entryName=name,
            unitId=i + offset, # NOTE: Kicad is strange, zero means only 1 unit, 1:N means more units
            styleId=1,
        )
        symbol.units.append(unit)
        units.append(unit)

    return symbol, units

def draw_rect(units, uid, start, end):
    # Draw
    units[uid].graphicItems.append(
        SyRect(
            start=start,
            end=end,
            stroke=Stroke(width=0, type="default"),
            fill=Fill(type="background"),
            )
    )


def add_pins(units, pin_list):
    # Add two pins

    offset_id = 0
    pin_id = 1
    uid_old = 0
    for pinname, driver, uid in pin_list:
        if uid != uid_old:
            uid_old = uid
            offset_id = 0
        units[uid].pins.extend([
            SymbolPin(
                electricalType=driver,
                graphicalStyle="line",
                position=Position(0.0, -1.0 * (1.27 + 2.54 * offset_id), angle=0),
                length=2.54,
                name=pinname,
                number=f"{pin_id}",

            ),
        ])
        pin_id = pin_id + 1
        offset_id  = offset_id + 1

def store(lib, symbol, path):
    lib.symbols.append(symbol)
    lib.to_file(path)


def update_symbol(symbol_name, pin_list, path="./Lib1.kicad_sym"):

    file = Path(path).resolve()
    dir = file.parent
    if not dir.exists():
        log(log_error, f"Directory does not exist! Directory: {dir}")
        exit(1)
    elif file.exists():
        log(log_note, f"Library exists: Open: {file}!")
        lib = SymbolLib.from_file(file)
    else:
        log(log_note, f"Library did not exist. Create: {file}!")
        lib = generate_lib()

    for sym  in lib.symbols:
        log(log_note, f"Found symbol: {sym.entryName}")
        if symbol_name == sym.entryName:
            log(log_note, f"Symbol already existed. Override: {symbol_name}!")
        else:
            log(log_note, f"Symbol did not exist. Create: {symbol_name}!")
    # Remove library
    lib.symbols = [s for s in lib.symbols if s.entryName != symbol_name]

    # log(log_note, f"Create new symbol: {symbol_name}")
    num_units = 0

    for pinname, driver, uid in pin_list:
        num_units = max(uid, num_units)
    num_units  = num_units + 1
    symbol, units = add_symbol(symbol_name, num_units)
    add_pins(units, pin_list)

    num_max_chars = max(len(pin[0]) for pin in pin_list)
    # TODO: Optimize for rect size...
    rect_x_end = max(4*2.54, num_max_chars * 0.6 * 2.54 + 1.27)

    for uid in range(0, num_units):
        uid_num_of_pins = len([pin for pin in pin_list if pin[2] == uid])

        rect_y_end = -1.0 * (uid_num_of_pins * 2.54 +  0.0)
        draw_rect(units, uid,
                  Position(2.54, 0),
                  Position(rect_x_end, rect_y_end))
        for prop in symbol.properties:
            if prop.key == "Reference":
                prop.position.X = rect_x_end
                prop.position.Y = - 1.27
                prop.effects.justify.horizontally = "left"
            if prop.key == "Value":
                prop.position.X = rect_x_end
                prop.position.Y = -3.84
                prop.effects.justify.horizontally = "left"

    store(lib, symbol, path)

def testing():
    PinList = [["Pin1", "input", 0],
            ["Pin2", "output", 0],
            ["Pin3", "input", 0],
            ["Pin4", "input", 0],
            ["Pin5", "input", 1],
            ["Pin6", "input", 1],
            ["Pin7", "input", 1],
            ["Pin8", "input", 1],
                ["Pin9", "input", 1],
            ]
    # PinList = [["Pin1", "input", 0],
    #            ["Pin2", "output", 0],
    #            ["Pin3", "input", 0],
    #]
    update_symbol(path="./Lib1.kicad_sym", symbol_name="Symbol2", pin_list=PinList)

# testing()