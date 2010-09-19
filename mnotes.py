#!/usr/bin/env python

# Setup:

import os,sys,subprocess
sys.path.append("/workspace/pyTexNotes/")
TEMP_DIR = "/tmp/mnotes/"
PWD = os.getcwd()
logfile = "log"

print "Running mnotes script."

if __name__ != "__main__":
    print "Meant to be run as a script."

os.system("mkdir " + TEMP_DIR)


# Get command line options:
import optparse

optParser = optparse.OptionParser()

optParser.add_option("-i", "--input", action="store", type="string", dest="input_file", help="Input pretex notes file.")
optParser.add_option("-o", "--output", action="store", type="string", dest="output_file", help="Output pdf file.")

optParser.add_option("-d", "--debug-xml", default=False, action="store_true", dest="debug_xml")
optParser.add_option("-l", "--log", default=False, action="store_true", dest="log")
optParser.add_option("-x", "--debug-latex", default=False, action="store_true", dest="debug_latex")

(options, args) = optParser.parse_args()

input_fname = options.input_file
output_fname = options.output_file

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

if options.debug_xml is True:
    print "\n"
    for num, line in enumerate(xml_lines):
        print str(num+1) + ': ', line
    print "\n"


# Parse to tex

import xml2tex

to_tex = xml2tex.to_tex(xml_lines, aslines = True)
tex_lines = to_tex.process()

if options.debug_latex is True:
    print "\n"
    for line in tex_lines:
        print line,
    print "\n"


# Run pdflatex

os.chdir(TEMP_DIR)
texname = TEMP_DIR + "out.tex"
pdfname = TEMP_DIR + "out.pdf"
texout = open(texname, 'w')
for line in tex_lines:
    texout.write(line)
texout.close()

print "Running pdflatex..."

error = os.system("pdflatex " + texname + " >> " + PWD + '/' +  logfile)

if options.log is False:
    os.system("rm " + PWD + '/' + logfile)
os.chdir(PWD)

os.system("mv " + texname + " " + tex_fname)

if error != 0:
    print "Error from pdflatex detected, exiting."
    sys.exit(error)

else:
    print "Success."
    os.system("mv " + pdfname + " " + output_fname)
    
    print "Output written to", output_fname

