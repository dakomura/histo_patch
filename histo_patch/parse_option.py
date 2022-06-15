from argparse import ArgumentParser

def get_option():
    argparser = ArgumentParser()
    
    argparser.add_argument('path_to_wsi', help='Path to WSI file (.svs or .ndpi)') 
    argparser.add_argument('path_to_save_directory', help='root of output patches') 
    
    argparser.add_argument('--annotation_type', '-a', 
                            type=str,
                            default='ndpa',
                            help='file type of annotation (ndpa or QuPath)')
    
    argparser.add_argument('--src_size', 
                            type=int,
                            default=512,
                            help='patch size in the original WSI')
    
    argparser.add_argument('--micrometer', '-m', 
                            action='store_true'
                            help='specify origsize in micrometer (default:pixels)')
    
    argparser.add_argument('--patch_size', 
                            type=int,
                            default=512,
                            help='output patch size')
    
    argparser.add_argument('--num_patch', 
                            type=int,
                            default=512,
                            help='output patch size')
    

    argparser.add_argument('--color', '-c', 
                            type=str,
                            default='',
                            help='used color (ff0000, 00ff00)')

    argparser.add_argument('--nparent',
                            type=int,
                            default=0,
                            help='number of parent directories kept in the output')


    return argparser.parse_args()