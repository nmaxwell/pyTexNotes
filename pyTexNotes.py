
import sys
import os
#import time
#from glob import iglob
#import shutil
#import getopt
import xml.parsers.expat

import tools
import genXml



def compile(xml_lines, xml_line_numbers, macro, preamble ):
    sys.stdout.write("Compiling...\t")
    print "\n"
    
    
    tex_lines=[]
    
    for line in preamble:
        tex_lines.append(line)
    
    for line in macro:
        tex_lines.append(line)
    
    tex_lines.append("\n\\begin{document}\n")
    
    p = xml.parsers.expat.ParserCreate()
    
    for line in xml_lines:
        print line
    
    
    
    tex_lines.append("\n\\end{document}\n")
    
    
    print ''
    sys.stdout.write("done.\n")
    return tex_lines






if __name__ == "__main__":
    
    args = sys.argv[1:]
    
    [input_args, output_args ] = tools.parse_args(args, [['-in','-i','-input','--input'], ['-out','-o','-output','--output'] ] )
    
    input = input_fname = None
    output = output_fname = None
    
    if len(input_args) == 0:
        print "error: no input files understood."
        quit()
    
    while len(output_args) < len(input_args):
        output_args.append('')
    
    for k,ofname in enumerate(output_args):
        if ofname in [ '', None ]:
            ifname = input_args[k]
            (name, in_ext) = os.path.splitext(ifname)
            if in_ext not in ['tex', '.tex' ]:
                output_args[k] = name + '.tex'
            else:
                output_args[k] = name + '.out' + '.tex'
    
    for num in range(len(input_args)):
    
        input_fname = input_args[k]
        output_fname = output_args[k]
        
        try:
            input = open( input_fname, 'r' )
        except:
            print "error: couldn't open input file: ", input_fname
            quit()
        
        try:
            output = open( output_fname, 'w' )
        except:
            print "error: couldn't open output file: ", output_fname
            quit()
        
        
        xml_lines, xml_line_numbers = genXml.to_xml(input)
        
        
        output.close()
        input.close()
        

