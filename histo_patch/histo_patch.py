from .annotation import *
from .scanner import *
from .utils import *
from .extract import *

import click
@click.command()
@click.argument(
        'path_to_wsi', 
) 
@click.argument(
        'path_to_save_directory', 
) 
@click.option(
        '--annotation_type', '-a', 
        type=click.Choice(['ndpa','qupath']),
        default='ndpa',
        help='file type of annotation (ndpa or qupath (GeoJSON(Pretty JSON)))',
)
@click.option(
        '--annotation_shape', '-s', 
        type=click.Choice(['all','line','area']),
        default='all',
        help='annotation shape (all, line, area)',
)
@click.option(
        '--color', '-c', 
        type=str,
        default='',
        help='used colors (white,black,red,green,blue,cyan,magenta,yellow) in annotation for ndpa or (None,Tumor,Stroma,Immune_cells,Necrosis,Other,Region,Ignore,Positive,Negative) for QuPath',
)
@click.option(
        '--line_as_area',  
        is_flag=True,
        help='line annotation in ndpa file is treated as closed area',
)
@click.option(
        '--src_size', 
        type=float,
        default=512,
        help='patch size in the original WSI',
)
@click.option(
        '--micrometer', '-m', 
        is_flag=True,
        help='specify src_size in micrometer (default:pixels)',
)
@click.option(
        '--patch_size', 
        type=int,
        default=512,
        help='output patch size',
)
@click.option(
        '--num_patch', 
        type=int,
        default=20,
        help='number of patches for each annotation shape',
)
@click.option(
        '--nparent',
        type=int,
        default=0,
        help='number of parent directories kept in the output',
)

def main(
    path_to_wsi,
    path_to_save_directory,
    annotation_type,
    annotation_shape,
    color,
    line_as_area, 
    src_size,
    micrometer,
    patch_size,
    num_patch,
    nparent,
):
    wsi_type = get_wsi_type(path_to_wsi)

    if wsi_type == 'ndpi':
        wsi = NDPI(path_to_wsi)
    elif wsi_type == 'svs':
        wsi = SVS(path_to_wsi)

    if color == "":
        used_color = None
    else:
        used_color = [x.replace(" ","") for x in color.split(",")]
        if annotation_type == 'ndpa':
            for c in used_color:
                if not c in ['white','black','red','green','blue','magenta','cyan','yellow']:
                    raise Exception('invalid color name %r' % c)
        elif annotation_type == 'qupath': 
            for c in used_color:
                if not c in ['None','Tumor','Stroma','Immune_cells','Necrosis','Other','Region','Ignore','Positive','Negative']:
                    raise Exception('invalid category name %r' % c)
        

    if annotation_type == 'ndpa':
        annotfile = path_to_wsi + '.ndpa' 
        annot = NDPA(annotfile, wsi, line_as_area, used_color)
    elif annotation_type == 'qupath': 
        annotfile = os.path.splitext(path_to_wsi)[0] + '.geojson' 
        annot = QUPATH(annotfile, wsi, line_as_area, used_color)


    annot.read()
    area_string, line_string = annot.annotation_to_string()

    #save_txt(annotations_string, args.path_to_openslide, args.path_to_save_directory)
    #extract
    outdir = path_to_save_directory

    # if keep parent directory structure
    if nparent > 0:
        outdir = os.path.join(outdir, *path_to_wsi.split("/")[-(1+nparent):-1])
    outdir = os.path.join(outdir, os.path.splitext(os.path.basename(path_to_wsi))[0])


    # if micrometer is used instead of pixel
    if micrometer:
        src_size = int(src_size / wsi.get_mpp())
    else:
        src_size = int(src_size)

    # line annotation for cystic lesion
    if line_string is not None and annotation_shape != 'area':
        gen = LineSlideGenerator(line_string,
                    path_to_wsi, 
                    src_size, 
                    patch_size,  
                    dump_patch=outdir)

        for i in range(num_patch):
            gen.get_example(i)

    # area annotation
    if area_string is not None and annotation_shape != 'line':
        gen = AreaSlideGenerator(area_string,
                    path_to_wsi, 
                    src_size, 
                    patch_size,  
                    dump_patch=outdir)

        for i in range(num_patch):
            gen.get_example(i)

if __name__ == '__main__':
   main() 