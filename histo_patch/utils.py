import os   

def get_wsi_type(wsifile):
    ex = os.path.splittext(wsifile)[1]
    if not ex in ['svs', 'ndpi']:
        raise Exception('invalid file format %r' % wsifile)
    return ex