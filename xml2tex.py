
import sys
import os
import xml.parsers.expat
import tools




def to_tex(input ):
    
    #define handlers:
    
    class handler:
        token=None
        def __init__(self, token):
            self.token = token
    
    token_list=['theorem', 'document']
    handlers={}
    
    for token in token_list:    
        handlers[token]=handler(token)
    
    
    
    handlers[token].__call__
    
    
    
    
    
    
    
    
    return ([],[])









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
        
        tex_lines, tex_line_numbers = to_tex(input)
        
        for line in tex_lines:
            output.write(line + "\n" )
        
        output.close()
        input.close()
        





