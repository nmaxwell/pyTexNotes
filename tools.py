



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


