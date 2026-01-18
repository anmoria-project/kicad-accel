# README (Kicad-Accel)

Kicad-Accellerators are scripts that acellerate some aspects of the Kicad PCB design flow.

There are the following accellerators: 

1. symbol-generator.py: Generates a new symbol ('kicad_sym') from a CSV list
1. kicad-devops(TBD): A generator flow and cheatsheet (tips and tricks) on how to use kicad with version control and review processes
1. subsheet-placer.py (TBD): Places previously designed 'kicad_pcb' as is into a parent placement design.
1. kicad-diff(TBD): A diff-tool for kicad to compare different branches/commits 

NOTE: This is right now a Hack-It-Together project without any claim or warranty on production readyness or clean-coding. The reason I publish this project is because I think it can help some people and I like to hack around such projects. 

Can you generate this with an AI/LLM? Most likely. If you like to have undeterministic boilerplate code that changes every time you regenerate it. Code that no one understands or ever reviews.. This project is all about the idea to simplify workflows and learn something on the way.

If there is interest I will continue the work. If you have any suggestions on other accellerators lets chat!

## Kicad-Devops

A generator flow and cheatsheet (tips and tricks) on how to use kicad with version control and review processes. 

The overall goal is to enable Kicad for dev-ops pipelines and review processes:

1. Version control kicad projects (f.e. GIT)
1. Re-generate output products (f.e. Gerber files) instead of zipping them
1. Enable compare of different version (Diff-tools)
1. Enable Review-processes like in Software for revisions.

While kicad source files are (almost all) Version-controllable (Human readable text-files instead of binaries like in other prducts), some special processes must be followed to not kill the advantage of Version-controlling.

TBD

## Symbol-Generator

This is a stupid (as in KISS aka Keep It Simple, Stupid) Symbol generator for kicad from a simple CSV list.

Motivation: In certain projects I had the rather timeconsuming challenge to create symbols in tools like kicad. While this is easy for an ne555 chip with a handful of pins, its not so funny with an fpga with 400 pins. The process of manually configuring this components from scratch is unnecessary and very error prone overhead. In almost all projects we had some kind of excel list with pinouts. Those list had to be converted per hand multiple times in the project. 
Instead I started to create generators wich reduces the error rate from 'N * num_pins' to '1 * num_pins'.
Missing was an generator for the kicad libraries. This is exactly that. Have one pinout .csv that is the single source of truth and generate all your project data.

Usecase1: An example of a usecase might be you miss a compnent in the kicad library and have to create a new one. You have a .csv list of pins (Which can easily be generated per LLM from datasheets, or copied if you have luck). With this generator you simply can generate the kicad symbol with one program execution.

Usecase2: You want a production pipeline that will automatically update your kicad projects whenever some pinouts changes. F.e. your FPGA pinout will change its drivers. Some 'inputs' will become 'outputs' or vice-versa and you want to use the Rule-Checker in the FPGA Tool (very recommended!). Your .csv will be the single truth to generate to multiple departments without overhead or error-prone manual labor.

Steps to create the symbol:

1. Get CSV list with all pins
1. Execute the generator
1. Import library to your schematic editor


### Create CSV list

Create a CSV list that looks like this: 

```csv
IC-PIN,Unit,Name,Driver,Notes
A1,bank1,SomePinXY1,input,
A8,bank1,SomePinXY2,input,
A9,bank1,SomePinXY3,input,
A2,bank1,SomePinXY4,input,
C19,power,vcc3v3,output,
D10,power,vcc1v8,output,
A7,power,gnd,output,
C10,power,gnd,output,
```
NOTE: There are some example .csv files in the ./test/ folder!

The CSV must be a comma seperated file with ',' as delimiter in 'utf-8' format. Make sure you save it as .csv file. Check with 'sh> cat componet1.sh'!

The First row will be ignored in the CSV! Name it as you want. The order is important: 

1. ID-PIN: The Pin of the IC! Match this to the package (f.e. '0, 1, ...' or 'a10, b9, ...')
1. Unit/Bank/Block: Every Unit gets its own Symbol-Unit. If you only want one Unit, use always the same UnitName!
1. Name: The signal/Pin name. 
1. Driver: The driver type. Possible types are: [input, output, bidirectional, tri_state, free, unspecified, power_in, power_out]
1. Notes: Only for internal notes. The tool will ignore them right now.

Naming rules are kicad-specific! Do follow the naming-rules!

The generator does not sort the pins! They will be added to the specific block as ordered in the .csv file!

The name of the .csv file is the name of the library and component!

Do not add rows with additional content below, do not add empty rows. Every row with content must have valid pin data!

### Generate

Install Python3 on your linux like bash terminal (or Windows try to include a better OS like Linux called WSL..)

To generate execute the following script: 

```bash
    # Execute in bash!
    # Generate the symbol library
    python3 symbol-generator.py ./test/multi_unit_test.csv

    # Check if the file was generated
    cat build/multi_unit_test.kicad_sym

```

In kicad symbol-editor use 'Add library' and add the generated library in the ./buid/ directory! 

If you want to change/update some .csv data, simply regenerate the library. Kicad will auto-update the symbol in the symbol editor. To update the library in your schematics/placements, please check the appropriate docu of kicad.

If you want to modify the library, simply copy it in the symbol-editor into your production-library and modify it. 

### Troubleshoot

Issue1: Kicad tells you that you already have a library with that name. Even when library is locally and globally removed...

    Solution: Remove the library from the library tree. Open the Kicad-project editor. Got to 'Preferences - Manage Symbol Libraries', search in local/global libraries for the name of your component and remove the library!

Issue2: Kicad fails to load the library or crashes..

    Solution: Check the .csv file for bad input data. The generator does not check all forbidden characters yet. Its simple: If something is forbidden in kicad symbol editor, it is logically also forbidden in the .csv file! 

Issue3: The component that is generated looks very ugly and is one-sided. 

    Soluton: This is on purpose. The library symbols are 'stackable'. Which means you can put multiple unit-blocks over each other and press the 'insert' key to autogenerate labels/signals with offset of 2.54mm. That is also the reason the library is not double sided. In theory you can create a connector and simply put it on the component without any labels or crossing signals! The component is therefore optimized for Generation. If you want to change your component you simply can copy the symbol to your own library and modify it as needed!

Issue4: The pins are NOT sorted in ascenting order. 

    Solution: This is on purpose! With this method the creator of the .csv file can control which pins are on which position on the Unit. Simply sort your .csv and the order will be also sorted in the Unit!

## Subsheet-Placer

TBD: This component is not yet designed!

The subsheet-placer places previously placed '.kicad_pcb' as is into a parent placement design. This allows for one-time placement and reuse of already proven placement designs. This also allows to enable testing for placement designs like in software and makes dev-ops engineering with kicad possible!

This project is not yet implemented.

