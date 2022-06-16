from argparse import ArgumentParser

def get_option():
    argparser = ArgumentParser()
    
    argparser.add_argument('path_to_wsi', help='Path to WSI file (.svs or .ndpi)') 
    argparser.add_argument('path_to_save_directory', help='root of output patches') 
    
    argparser.add_argument('--annotation_type', '-a', 
                            type=str,
                            default='ndpa',
                            help='file type of annotation (ndpa or qupath (GeoJSON(Pretty JSON)))')
    
    argparser.add_argument('--annotation_shape', '-s', 
                            type=str,
                            default='all',
                            help='annotation shape (all, line, area)')
    
    argparser.add_argument('--color', '-c', 
                            type=str,
                            default='',
                            help='used colors (white,black,red,green,blue,cyan,magenta,yellow) in annotation for ndpa or (None,Tumor,Stroma,Immune_cells,Necrosis,Other,Region,Ignore,Positive,Negative) for QuPath')
    
    argparser.add_argument('--line_as_area',  
                            action='store_true',
                            help='line annotation in ndpa file is treated as closed area')

    argparser.add_argument('--src_size', 
                            type=float,
                            default=512,
                            help='patch size in the original WSI')
    
    argparser.add_argument('--micrometer', '-m', 
                            action='store_true',
                            help='specify src_size in micrometer (default:pixels)')
    
    argparser.add_argument('--patch_size', 
                            type=int,
                            default=512,
                            help='output patch size')
    
    argparser.add_argument('--num_patch', 
                            type=int,
                            default=20,
                            help='number of patches for each annotation shape')

    argparser.add_argument('--nparent',
                            type=int,
                            default=0,
                            help='number of parent directories kept in the output')


    return argparser.parse_args(args=[])