# class for scanner (Hamamatsu ndpi or Aperio svs)
import tifffile as t

class WSI:
    def __init__(self, wsifile):
        self.wsifile = wsifile
        self.set_metadata()

    def get_mpp(self):
        return self.metadata['mpp_x']
    
    def get_mpp_x(self):
        return self.metadata['mpp_x']
    
    def get_mpp_y(self):
        return self.metadata['mpp_y']


class SVS(WSI):
    def __init__(self, wsifile):
        super().__init__(wsifile)

    def set_metadata(self):
        self.metadata = {}
        with t.TiffFile(self.wsifile) as svs:
            description = svs.series[0].keyframe.tags['ImageDescription'].value
            metadata_base = {x.split(" = ")[0]:x.split(" = ")[1] for x in description.split("|")[1:]}
            self.metadata['mpp_x'] = float(metadata_base['MPP'])
            self.metadata['mpp_y'] = float(metadata_base['MPP'])
            self.metadata['width'] = int(metadata_base["OriginalWidth"])
            self.metadata['height'] = int(metadata_base["OriginalHeight"])

    def get_pos(self, x, y):
        mpp_x = self.metadata['mpp_x']
        mpp_y = self.metadata['mpp_y']
        x_pixels_from_topleft = int(x // (1000 * mpp_x))
        y_pixels_from_topleft = int(y // (1000 * mpp_y))

        return x_pixels_from_topleft, y_pixels_from_topleft 



class NDPI(WSI):
    def __init__(self, wsifile):
        super().__init__(wsifile)

    def set_metadata(self):
        self.metadata = {}
        with t.TiffFile(self.wsifile) as ndpi:
            self.metadata['x_offset'] = ndpi.series[0].keyframe.ndpi_tags['XOffsetFromSlideCenter']
            self.metadata['y_offset'] = ndpi.series[0].keyframe.ndpi_tags['YOffsetFromSlideCenter']
            self.metadata['mpp_x'] = 10000/ndpi.series[0].keyframe.tags['XResolution'].value[0]
            self.metadata['mpp_y'] = 10000/ndpi.series[0].keyframe.tags['YResolution'].value[0]
            self.metadata['width'] = ndpi.series[0].keyframe.tags['ImageWidth'].value
            self.metadata['height'] = ndpi.series[0].keyframe.tags['ImageLength'].value

    def get_pos(self, x, y):
        mpp_x = self.metadata['mpp_x']
        mpp_y = self.metadata['mpp_y']
        x_nm_from_center = x - self.metadata['x_offset']
        y_nm_from_center = y - self.metadata['y_offset']
        x_nm_from_topleft = x_nm_from_center + self.metadata['width'] * mpp_x * 1000 // 2
        y_nm_from_topleft = y_nm_from_center + self.metadata['height'] * mpp_y * 1000 // 2
        x_pixels_from_topleft = int(x_nm_from_topleft // (1000 * mpp_x))
        y_pixels_from_topleft = int(y_nm_from_topleft // (1000 * mpp_y))

        return x_pixels_from_topleft, y_pixels_from_topleft 


