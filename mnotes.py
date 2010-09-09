#!/usr/bin/env python

# Setup:

import os,sys
sys.path.append("/workspace/pyTexNotes/")
TEMP_DIR = "/tmp/mnotes/"
PWD = os.getcwd()


print "Running mnotes script."

if __name__ != "__main__":
    print "Meant to be run as a script."



# Get command line options:
import optparse

optParser = optparse.OptionParser()

optParser.add_option("-i", "--input", action="store", type="string", dest="input_file", help="Input pretex notes file.")
optParser.add_option("-o", "--output", action="store", type="string", dest="output_file", help="Output pdf file.")

optParser.add_option("-d", action="store_true", dest="debug")


(options, args) = optParser.parse_args()

input_fname, output_fname = options.input_file, options.output_file
if None in [input_fname ]:
    print "Usage error, see help."
    sys.exit(2)


# Determine output pdf name, if not specified
tex_fname = output_fname
if output_fname is None:
    output_fname, dummy = os.path.splitext(input_fname)

    #stripping '.pre' if it exists at the end
    l = len(output_fname)
    if output_fname[l-4:l] == ".pre":
        output_fname = output_fname[0:l-4]
    
    tex_fname = output_fname + ".tex"
    output_fname += ".pdf"

output_fname_root, dummy = os.path.splitext(output_fname) 


# Parse to xml:

import genXml
import toolbox


input_file = toolbox.openAnything(input_fname)
input_lines = input_file.readlines()
input_file.close()

xml_lines, xml_line_numbers = genXml.to_xml(input_lines)

if options.debug is True:
    print "\n"
    for line in xml_lines:
        print line
    print "\n"


# Parse to tex

import xml2tex

to_tex = xml2tex.to_tex(xml_lines, aslines = True)
tex_lines = to_tex.process()


if options.debug is True:
    print "\n"
    for line in tex_lines:
        print line
    print "\n"


# Run pdflatex

os.chdir(TEMP_DIR)
texname = TEMP_DIR + "out.tex"
pdfname = TEMP_DIR + "out.pdf"
texout = open(texname, 'w')
for line in tex_lines:
    texout.write(line)
texout.close()

print "Running pdflatex...\n"
error = os.system("pdflatex " + texname)
os.chdir(PWD)
print ""

os.system("mv " + texname + " " + tex_fname)

if error != 0:
    print "Error from pdflatex detected, exiting."
    sys.exit(error)

else:
    print "Success."
    os.system("mv " + pdfname + " " + output_fname)
    
    print "Output written to", output_fname

