def main():
    args = get_option()

    wsi_type = get_wsi_type(args.path_to_wsi)

    if wsi_type == 'ndpi':
        wsi = NDPI(args.path_to_wsi)
    elif wsi_type == 'svs':
        wsi = SVS(args.path_to_wsi)

    if args.color == "":
        used_color = None
    else:
        used_color = [x.replace(" ","") for x in used_color.split(",")]
        if args.annotation_type == 'ndpa':
            for color in used_color:
                if not color in ['white','black','red','green','blue','magenta','cyan','yellow']:
                    raise Exception('invalid color name %r' % color)
        elif args.annotation_type == 'qupath': 
            for color in used_color:
                if not color in ['None','Tumor','Stroma','Immune_cells','Necrosis','Other','Region','Ignore','Positive','Negative']:
                    raise Exception('invalid category name %r' % color)
        

    if args.annotation_type == 'ndpa':
        annotfile = args.path_to_wsi + '.ndpa' 
        annot = NDPA(annotfile, wsi, args.line_as_area, used_color)
    elif args.annotation_type == 'qupath': 
        annotfile = os.path.splitext(args.path_to_wsi)[0] + '.geojson' 
        annot = QUPATH(annotfile, wsi, args.line_as_area, used_color)
    else:
        raise Exception('invalid annotation type %r' % args.annotation_type)


    if not args.annotation_shape in ['all', 'line', 'area']:
        raise Exception('invalid annotation shape %r' % args.annotation_shape)



    annot.read()
    area_string, line_string = annot.annotation_to_string()

    #save_txt(annotations_string, args.path_to_openslide, args.path_to_save_directory)
    #extract
    outdir = args.path_to_save_directory

    # if keep parent directory structure
    if args.nparent > 0:
        outdir = os.path.join(outdir, *args.path_to_wsi.split("/")[-(1+args.nparent):-1])
    outdir = os.path.join(outdir, os.path.splitext(os.path.basename(args.path_to_wsi))[0])


    # if micrometer is used instead of pixel
    if args.micrometer:
        src_size = int(args.src_size / wsi.get_mpp())
    else:
        src_size = int(args.src_size)

    # line annotation for cystic lesion
    if line_string is not None and args.annotation_shape != 'area':
        gen = LineSlideGenerator(line_string,
                    annot.get_total_len(),
                    args.path_to_wsi, 
                    src_size, 
                    args.patch_size,  
                    dump_patch=outdir)

        for i in range(args.num_patch):
            gen.get_example(i)

    # area annotation
    if area_string is not None and args.annotation_shape != 'line':
        gen = AreaSlideGenerator(area_string,
                    args.path_to_wsi, 
                    src_size, 
                    args.patch_size,  
                    dump_patch=outdir)

        for i in range(args.num_patch):
            gen.get_example(i)

if __name__ == '__main__':
   main() 