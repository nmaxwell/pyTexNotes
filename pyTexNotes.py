
import sys
import os
import time
from glob import iglob
import shutil
import getopt


class document:
    n_secions=0
    input_file=None
    
    
def parse(input ):
    print "parsing..."
    
    
    
    
    for number, line in enumerate(input):
        if line == "%<<setup>>":
            n1 = number
            for k in range(n1,len(input)):
                if line == "%<</setup>>":
                
    
    
    
    
    
    
    
    doc = document()
    doc.input_file=input
    
    return doc


def compile(doc, output, macro, preamble ):
    print "compiling..."
    
    out_file = open(output_fname, 'w')
    
    for line in preamble:
        out_file.write(line)
    
    for line in macro:
        out_file.write(line)
    
    out_file.write("\n\\begin{document}\n")
    
    for line in doc.input_file:
        out_file.write(line)
    
    out_file.write("\n\\end{document}\n")
    out_file.close()



def parse_args(args, opts):
    
    values = [ [] for opt in opts ]
    flat_opts = []
    for opt in opts:
        if isinstance(opt,list):    
            flat_opts.extend(opt)
        else:
            flat_opts.append(opt)
    
    for arg_number, arg in enumerate(args):
        for opt_number, opt in enumerate(opts):
            if arg in opt and len(args) > arg_number+1 and args[arg_number+1] not in flat_opts:
                values[opt_number].append(args[arg_number+1])
    
    return values



if __name__ == "__main__":
    
    args = sys.argv[1:]
    
    [input_args, output_args, macro_args, preamble_args] = parse_args(args, [['-in','-i','-input','--input'], ['-out','-o','-output','--output'], ['-m','-macros','--macros'],['-p','-pa','-preamble','--preamble'] ] )
    
    input = input_fname = None
    output = output_fname = None
    macro = macro_fname = None
    preamble = preamble_fname = None
    
    if len(input_args) == 0:
        print "error: no input files understood."
        quit()
    
    try:
        if len(output_args) == 0:
            output_fname = 'out.tex'
        else:
            output_fname = output_args[0]
        output = open( output_fname, 'w' )
    except:
        print "error: couldn't open output file: ", output_fname
    
    try:
        if len(macro_args) == 0:
            macro_fname = 'std_macros.tex'
        else:
            macro_fname = macro_args[0]
        macro = open( macro_fname, 'r' )
    except:
        print "error: couldn't open macro file: ", macro_fname
    
    try:
        if len(preamble_args) == 0:
            preamble_fname = 'std_preamble.tex'
        else:
            preamble_fname = preamble_args[0]
        preamble = open( preamble_fname, 'r' )
    except:
        print "error: couldn't open preamble file: ", preamble_fname
    
    
    for input_fname in input_args:
        
        try:    
            input = open( input_fname, 'r' )
        except:
            print "error: couldn't open input file: ", input_fname
            quit()
        
        
        doc = parse(input)
        compile(doc, output, macro, preamble )
        input.close()
        
        time.sleep(0.1)        
        os.system( "pdflatex " + output_fname )
        basename, extension = os.path.splitext(output_fname)
        os.system( "rm " + basename + '.log' )
        basename, extension = os.path.splitext(output_fname)
        os.system( "rm " + basename + '.aux' )
