FZPZF
=========

FZPZF is a little python script that creates chip-definitions for 
fritzing. it is a quick hack, so you don't have to use illustrator
or inkscape if you want to add a microcontroller to your fritzing
library.
licensed under mit license

to create your part you can follow these three steps

## 1. create a .part file 
just look at the files `parts/16f688.part` or `parts/max232`.
they should illustrate how to create your own file.
instead, you can also follow this mini-tutorial. just open your
favourite text-editor. and create the file `12f629.part` in the parts
folder.

first you need some meta data: the name of the part and it's keywords.

    *NAME PIC12F629
    *TAGS pic, microchip, 8bit

the asterix(\*) tells the script a new section in the file follows.
Keywords are comma seperated.

The most important part are the pins:

    *PINS
    $1 VDD    2.0V-5V
    $2 GP5    GP5 T1CKI OSC1 CLKIN
    $3 GP4    GP4 T1G OSC2 CLKOUT
    $4 GP3    GP3 MCLR VPP
    $5 GP2    GP2 TOCKI INT COUT
    $6 GP1    GP1 CIN- IICSPCLK
    $7 GP0    GP0 CIN+ ICSPDAT
    $8 VSS    0V

we need to tell the parser, that pins will be defined next,
so we write `*PINS`.
pins start with a dollar sign. when redefining pins for extra packages
this will be easier to read and write. the pin number is followed by
some whitespace, and after that the pin name is written down.
if you want to add a pin description, you can add more whitespace
(a single space, or a tab will be possible, too) and a pin-description.

we also need to tell the script that it should create a
schematic-graphic.

    *SCHEMATIC

but sometimes you want to reorder the pins for the schematic-graphic:

    *SCHEMATIC
    T ,$1,$8,
    L ,$7,$6,$5
    R ,$4,$3,$2
T,L,R and B (not used here) are the sides of the schematic-graphic
in order: Top, Bottom, Right, Left. now you can decide where you want
to add the pin. the additional commas are for formatting purposes,
to avoid overlaps in the text.

if you just define the R and L side, you also need to define the top
side (T) with commas `,,,,`  to receive a good result.

now we have a chip and it's pins, but we also need the physical
dimensions.

    *PACKAGE DIL
    *PACKAGE microchip/SOIC
    *PACKAGE microchip/DFN-S

same syntax we've seen before. as i learned, the packages slightly
differ depending on what manufacture you use.
if you are lucky all packages will be already defined, but as this is
an example, the DFN-S-package is not defined yet.
otherwise we could directly jump to step 3

## 2. create a package-file

the files `DIL` and `microchip/QFN-4mm-16` have some comments.
let's create a file named exactly like we used it for the \*PACKAGE.
so in our case we navigate to the microchip folder and
create a file named `DFN-S`

same thing as before: we need a name first:

    *NAME DFN-S

this appears to be  the name of the 6x5mm body,
so we don't need to put the dimensions in the name

now we have to tell the script what size and what type the pin are of.
there are simple PADs but also THTs you can choose from. the syntax
slightly differs. for the THT we need to write smth. like:

    *PIN THT <diameter hole>, <width>, <height>

if width and height are not equal, the pin will have
a rect shape with a center hole. if width matches height, a circle
will be produced.
but as we try to make a smd package, we need to define a smd pin:

    *PIN PAD 0.45mm, 1.10mm

you could also use inch, pt or mils as dimensions.
next step is to specify the grid. we need the space between the pins
(e.g. distance between pin 1 and 2)

    *E 1.27mm

and also the distance in the other direction,
(distance between pin 1 and 8 in our example):

    *C 5.6mm

a picture is worth a thousand words:

        ____ ____
       |    U    |
    ###|1       8|### --|
       |         |      c
    ###|2       7|### --|
       |         |
    ###|3       6|###
       |         |
    ###|4       5|###
       |_________|

     |------e------|


if we would have a smd part where the pins are all around the chip, 
we would just define CH, and the script would do the rest. see 
`microchip/QFN-4mm-16` as an example

## 3. let python do the rest
that's it. everything else should be done by the script.
open a terminal window, cd to the folder you downloaded this
sourcecode to and execute `python fzdzf.py`
now the out folder shout be filled with \*.fzdz files.
you can also check the temp folder, to see if you like the svg
graphics, this should be faster then importing the .fzdzf files,
look at them, and deleting them again.

