# class for annotaion (Hamamatsu NDPView (.ndpa) or QuPath (.xml))

import math
import os
import xml.etree.ElementTree as ET 

OPEN_ANNOT = 'AnnotateFreehandLine'

class Annotation:
    def __init__(self, annotfile, wsi):
        self.annotfile = annotfile
        self.annotaions = {}
        self.wsi = wsi

    def annotation_to_string(self):
        area_string='@\n'
        line_string = ""
        
        idx = 0

        for color, annot_type, li in annotations.values():
            if annot_type == OPEN_ANNOT:
                pass

            else:
                length=len(li)
                area_string += f'0 {idx} {length}\n'
                for (x,y) in li:
                    area_string += f'{x} {y}\n'

                idx += 1

        #if the area annotations do not exist
        if area_string == '@\n':
            area_string == None

        return area_string, line_string


class NDPA(Annotation):
    def __init__(self, annotfile, wsi):
        super().__init__(annotfile, wsi)

    def read(self):
        used_color = args.color
        openslide_path = args.path_to_openslide
        annotation_file = "{}.ndpa".format(openslide_path)
        wsi=openslide.OpenSlide(openslide_path)

        tree = ET.parse(annotation_file) 
        mpp_x=float(wsi.properties['openslide.mpp-x'])
        mpp_y=float(wsi.properties['openslide.mpp-y'])

        total_len = 0

        annotations={}

        prev_x_pixels_from_topleft, prev_y_pixels_from_topleft = 0, 0

        for idx,ndpviewstate in enumerate(tree.iter('ndpviewstate')):
            annot_type = ndpviewstate.find('annotation').get('displayname')
            color = ndpviewstate.find('annotation').get('color')
            annotations[idx]=(color, annot_type, [])

            for i, point in enumerate(ndpviewstate.find('annotation').find('pointlist')):
                x=int(point[0].text)
                y=int(point[1].text)        
                x_pixels_from_topleft, y_pixels_from_topleft = wsi.get_pos(x, y)

                if annot_type == OPEN_ANNOT: #not closed => cyst
                    if i > 0:
                        annotations[idx][2].append((prev_x_pixels_from_topleft,
                                                    prev_y_pixels_from_topleft),
                                                    (x_pixels_from_topleft,
                                                    y_pixels_from_topleft))

                        total_len += math.sqrt(
                            (prev_x_pixels_from_topleft - x_pixels_from_topleft) ** 2 + \
                            (prev_y_pixels_from_topleft - y_pixels_from_topleft) ** 2)

                    prev_x_pixels_from_topleft = x_pixels_from_topleft
                    prev_y_pixels_from_topleft = y_pixels_from_topleft
                    #meningioma pattern 

