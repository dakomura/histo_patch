def main():
    args = get_option()

    wsi_type = get_wsi_type(args.path_to_wsi)

    if wsi_type == 'ndpi':
        wsi = NDPI(args.path_to_wsi)
    elif wsi_type == 'svs':
        wsi = SVS(args.path_to_wsi)

    if args.annotation_type == 'ndpa':
        annotfile = args.path_to_wsi + '.ndpa' 
        annot = NDPA(annotfile, wsi)
    elif args.annotation_type == 'qupath': 
        annotfile = args.path_to_wsi + '.xml' 
        annot = QuPath(annotfile, wsi)

    annotations = annot.read()
    area_string, line_string = annotations.annotation_to_string()

    #save_txt(annotations_string, args.path_to_openslide, args.path_to_save_directory)
    #extract
    outdir = args.path_to_save_directory

    # if keep parent directory structure
    if args.nparent > 0:
        outdir = os.path.join(outdir, *args.path_to_wsi.split("/")[-(1+args.nparent):-1])


    # if micrometer is used instead of pixel
    if args.micrometer:
        src_size = args.src_size / wsi.get_mpp() 
    else:
        src_size = args.src_size


    # area annotation
    if area_string is not None:
        gen = AreaSlideGenerator(area_string,
                    args.path_to_wsi, 
                    src_size, 
                    args.patch_size,  
                    dump_patch=outdir)

        for i in range(args.num_patch):
            gen.get_example(i)

    # line annotation for cystic lesion
    if line_string is not None:
        gen = LineSlideGenerator(line_string,
                    args.path_to_wsi, 
                    src_size, 
                    args.patch_size,  
                    dump_patch=outdir)

        for i in range(args.num_patch):
            gen.get_exampl