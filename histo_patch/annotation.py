import math
import os
import xml.etree.ElementTree as ET 
import json


class Annotation:
    def __init__(self, annotfile, wsi):
        self.annotfile = annotfile
        self.annotations = {}
        self.wsi = wsi
        self.line_as_area = False

    def annotation_to_string(self):
        area_string = '@\n'
        line_string = f'@{int(self.total_len)}\n'
        
        idx_area = idx_line = 0

        for color, annot_type, li in self.annotations.values():
            length=len(li)
            if annot_type == self.OPEN_ANNOT and not self.line_as_area:
                line_string += f'0 {idx_line} {length}\n'
                for ((px, py), (x, y)) in li:
                    line_string += f'{px} {py} {x} {y}\n'

                idx_line += 1

            else:
                area_string += f'0 {idx_area} {length}\n'
                for (x,y) in li:
                    area_string += f'{x} {y}\n'

                idx_area += 1

        #if the annotations do not exist
        if area_string == '@\n':
            area_string = None
        if len(line_string.split("\n")) <= 2:
            line_string = None

        return area_string, line_string


class NDPA(Annotation):
    def __init__(self, annotfile, wsi, line_as_area, used_color):
        super().__init__(annotfile, wsi)
        self.line_as_area = line_as_area
        self.used_color = used_color
        self.OPEN_ANNOT = 'AnnotateFreehandLine'
        self.COLOR_CODE = {'#ffffff': 'white',
                    '#404040': 'gray',
                    '#000000': 'black',
                    '#ff0000': 'red',
                    '#00ff00': 'green',
                    '#0000ff': 'blue',
                    '#ff00ff': 'magenta',
                    '#00ffff': 'cyan',
                    '#ffff00': 'yellow'}

    def read(self):
        tree = ET.parse(self.annotfile) 
        mpp_x = self.wsi.get_mpp_x()
        mpp_y = self.wsi.get_mpp_y()

        self.total_len = 0

        prev_x_pixels_from_topleft, prev_y_pixels_from_topleft = 0, 0

        for idx,ndpviewstate in enumerate(tree.iter('ndpviewstate')):
            annot_type = ndpviewstate.find('annotation').get('displayname')
            color = ndpviewstate.find('annotation').get('color')
            if self.used_color is not None and not self.COLOR_CODE[color] in self.used_color:
                continue
            self.annotations[idx]=(self.COLOR_CODE[color], annot_type, [])

            for i, point in enumerate(ndpviewstate.find('annotation').find('pointlist')):
                x=int(point[0].text)
                y=int(point[1].text)        
                x_pixels_from_topleft, y_pixels_from_topleft = self.wsi.get_pos(x, y)

                if annot_type == self.OPEN_ANNOT and not self.line_as_area: #not closed => cyst
                    if i > 0:
                        self.annotations[idx][2].append(((prev_x_pixels_from_topleft,
                                                    prev_y_pixels_from_topleft),
                                                    (x_pixels_from_topleft,
                                                    y_pixels_from_topleft)))

                        self.total_len += math.sqrt(
                            (prev_x_pixels_from_topleft - x_pixels_from_topleft) ** 2 + \
                            (prev_y_pixels_from_topleft - y_pixels_from_topleft) ** 2)

                    prev_x_pixels_from_topleft = x_pixels_from_topleft
                    prev_y_pixels_from_topleft = y_pixels_from_topleft
                    #meningioma pattern 

                else:
                    self.annotations[idx][2].append((x_pixels_from_topleft,y_pixels_from_topleft))

class QUPATH(Annotation):
    
    def __init__(self, annotfile, wsi, line_as_area, used_color):
        super().__init__(annotfile, wsi)
        self.line_as_area = line_as_area
        self.COLOR_CODE = {'Tumor': 'Tumor',
                        'Stroma': 'Stroma',
                        'Immune_cells': 'Immune cells',
                        'Necrosis': 'Necrosis',
                        'Other': 'Other',
                        'Region': 'Region*',
                        'Ignore': 'Ignore*',
                        'Positive': 'Positive',
                        'Negative': 'Negative'}
        self.used_color = used_color
        if self.used_color is not None:
            self.used_color = [self.COLOR_CODE[x] for x in self.used_color]
        
        self.OPEN_ANNOT = 'LineString'

    def read(self):
        with open(self.annotfile) as f:
            data = json.load(f)

        self.total_len = 0

        prev_x_pixels_from_topleft, prev_y_pixels_from_topleft = 0, 0

        if type(data) == dict:
            data = [data] # if there is only 1 annotation
        for idx, d in enumerate(data):
            annot_type = d["geometry"]['type']
            try:
                color = d["properties"]['classification']['name']
            except:
                color = "None"

            if self.used_color is not None and not color in self.used_color:
                continue

            self.annotations[idx]=(color, annot_type, [])
            coordinates = d["geometry"]['coordinates']
            if annot_type != self.OPEN_ANNOT:
                coordinates = coordinates[0]

            for i, point in enumerate(coordinates):
                x=int(point[0])
                y=int(point[1])        
                x_pixels_from_topleft, y_pixels_from_topleft = x, y

                if annot_type == self.OPEN_ANNOT and not self.line_as_area: #not closed => cyst
                    if i > 0:
                        self.annotations[idx][2].append(((prev_x_pixels_from_topleft,
                                                    prev_y_pixels_from_topleft),
                                                    (x_pixels_from_topleft,
                                                    y_pixels_from_topleft)))

                        self.total_len += math.sqrt(
                            (prev_x_pixels_from_topleft - x_pixels_from_topleft) ** 2 + \
                            (prev_y_pixels_from_topleft - y_pixels_from_topleft) ** 2)

                    prev_x_pixels_from_topleft = x_pixels_from_topleft
                    prev_y_pixels_from_topleft = y_pixels_from_topleft
                    #meningioma pattern 

                else:
                    self.annotations[idx][2].append((x_pixels_from_topleft,y_pixels_from_topleft))
