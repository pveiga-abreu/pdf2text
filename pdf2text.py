from pdf2image import convert_from_bytes
from datetime import datetime
from io import BytesIO
from PIL import Image
import numpy as np
import pytesseract
import subprocess
import cv2
import os

from pytesseract.pytesseract import TesseractNotFoundError

class PDF2Text:
    def __init__(self, pdf_file: str) -> None:
        """
        pdf_file: str -> path from de PDF file
        """
        self.__validate_tesseract()
        self._convert_to_image(pdf_file)

    def __validate_tesseract(self) -> None:
        tess = subprocess.run(
            ['which', 'tesseract'],
            stdout=subprocess.PIPE
        ).stdout.decode('utf-8')
        if not tess: raise TesseractNotFoundError()

    def _convert_to_image(self, pdf_file: str) -> None:
        image = convert_from_bytes(
            open(pdf_file, 'rb').read(),
            dpi=350,
            single_file=True
        )[0]
        self.dimensions = image.size

        with BytesIO() as f:
            image.save(f,format="jpeg")
            f.seek(0)
            self.image = np.array(Image.open(f))[:, :, ::-1].copy()

    def save_image(
        self,
        dir: str = './',
        name: str = f'pdf2text_img_{datetime.now()}.jpeg'
    ) -> None:
        """
        dir: str -> default './'
        name: str -> default 'pdf2text_img_{datetime.now()}.jpeg'
        """
        cv2.imwrite(
            os.path.join(dir, name),
            self.image
        )

    def draw_lines(
        self,
        *args,
        thickness: int = 5,
        color: tuple = (0,0,255)
    ) -> None:
        """
        args : tuple -> top-left corner (X,Y), width and height formatted like this (X, Y, Width, Height)

        thickness: int - default 5 -> line thickness in pixels
        color: tuple - default (0,0,255) -> (Blue, Green, Red)
        """
        for coordinates in args:
            x, y, w, h = coordinates
            cv2.line(self.image, (x,y), ((x+w),(y+h)), color, thickness)

    def draw_rectangles(
        self,
        *args,
        thickness: int = 5,
        color: tuple = (0,0,255)
    ) -> None:
        """
        args : tuple -> top-left corner (X,Y), width and height formatted like this (X, Y, Width, Height)

        thickness: int - default 5 -> line thickness in pixels
        color: tuple - default (0,0,255) -> (Blue, Green, Red)
        """
        for coordinates in args:
            x, y, w, h = coordinates
            cv2.rectangle(self.image, (x,y), ((x+w),(y+h)), color, thickness)

    def extract_text_from_location(
        self,
        coordinates: tuple,
        lang: str = 'eng'
    ) -> str:
        """
        coordinates : tuple -> top-left corner (X,Y), width and height formatted like this (X, Y, Width, Height) 

        lang: str - default 'eng' -> define tesseract language

        Returns text from the specified location
        """
        x,y,w,h = coordinates
        chunk = self.image[y:y+h, x:x+w]
        text = pytesseract.image_to_string(chunk, lang=lang)

        return text.strip()

    def extract_all_text(
        self,
        lang: str = 'eng'
    ) -> str:
        """
        lang: str - default 'eng' -> define tesseract language

        Returns text from the pdf
        """
        return pytesseract.image_to_string(self.image, lang=lang)
