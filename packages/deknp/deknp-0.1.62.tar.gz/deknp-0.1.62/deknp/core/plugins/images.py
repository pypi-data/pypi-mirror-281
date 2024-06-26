import os
import fitz
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from dektools.file import sure_dir
from .base import Plugin


def write_image(input_img, output_img, w, h, dpi):
    drawing = svg2rlg(input_img)
    pdf = renderPDF.drawToString(drawing)
    doc = fitz.Document(stream=pdf)
    pix = doc.load_page(0).get_pixmap(alpha=True, dpi=dpi)
    dir_target = os.path.dirname(output_img)
    sure_dir(dir_target)
    pix.pil_save(output_img, sizes=[(w, h)])


class PluginImages(Plugin):
    dek_key_images = 'images'

    default_image_size = 256
    default_image_dpi = 96

    def run(self):
        images = self.merge_from_key(self.dek_key_images)
        for s, dll in images.items():
            src = os.path.join(self.project_dir, s)
            if os.path.isfile(src):
                if dll:
                    for d, dl in dll.items():
                        if dl is not None:
                            if len(dl) > 0:
                                w = dl[0]
                                if len(dl) > 1:
                                    h = dl[1]
                                else:
                                    h = w
                            else:
                                w = h = self.default_image_size
                            dest = os.path.join(self.project_dir, d)
                            write_image(src, dest, w, h, self.default_image_dpi)
