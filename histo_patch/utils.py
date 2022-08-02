import os   

# get WSI type(.svs or .ndpi)
def get_wsi_type(wsifile):
    ex = os.path.splitext(wsifile)[1]
    if not ex in ['.svs', '.ndpi']:
        raise Exception('invalid file format %r' % ex)
    return ex[1:]
