from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
import subprocess
import tempfile
import shutil
import cv2
import os

from pytesseract.pytesseract import TesseractNotFoundError

class PDF2Text:
    def __init__(self, pdf_file: str) -> None:
        """
        pdf_file: str -> path from de PDF file
        """
        self.__validate_tesseract()

        self._pdf_path = pdf_file
        self._tmpdir = tempfile.mkdtemp(
            dir=os.path.dirname(os.path.realpath(__file__))
            )
        self._convert_to_image()

    def __del__(self) -> None:
        shutil.rmtree(self._tmpdir, ignore_errors=True)

    def __validate_tesseract(self) -> None:
        tess = subprocess.run(
            ['which', 'tesseract'],
            stdout=subprocess.PIPE
        ).stdout.decode('utf-8')
        if not tess: raise TesseractNotFoundError()

    def _convert_to_image(self) -> None:
        self._img_path = os.path.join(self._tmpdir, 'img.jpg')

        image = convert_from_bytes(
            open(self._pdf_path, 'rb').read(),
            dpi=350,
            single_file=True
        )[0]
        image.save(self._img_path, 'JPEG')

    def draw_lines(self, *args, thickness=5, color=(0,0,255)) -> None:
        """
        args -> initial coordinate and final coordinate formatted like this ((X_tl, Y_tl), (X_br, Y_br)), 
                you should pass all pair of coordinates you want to draw

        thickness: int -> line thickness in pixels
        color: tuple -> (Blue, Green, Red)
        """
        image = cv2.imread(self._img_path)

        for coordinates in args:
            initial, final = coordinates
            cv2.line(image, initial, final, color, thickness)

        cv2.imwrite(self._img_path, image)

    def draw_rectangles(self, *args, thickness=5, color=(0,0,255)) -> None:
        """
        args -> top-left corner and bottom-right corner of rectangle formatted like this ((X_tl, Y_tl), (X_br, Y_br)), 
                you should pass all pair of coordinates you want to draw

        thickness: int -> line thickness in pixels
        color: tuple -> (Blue, Green, Red)
        """
        image = cv2.imread(self._img_path)

        for coordinates in args:
            top_left, bottom_right = coordinates
            cv2.rectangle(image, top_left, bottom_right, color, thickness)

        cv2.imwrite(self._img_path, image)

    def extract_text(self, lang: str='eng') -> str:
        """
        Returns text from the pdf

        lang: str -> default 'eng'
        """
        return pytesseract.image_to_string(
                Image.open(self._img_path),
                timeout=60,
                lang=lang
            )
