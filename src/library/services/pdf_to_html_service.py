import base64
import io

import fitz
from PIL import Image
from PyPDF2 import PdfReader


class PDFToHTMLService:
    def __init__(self, pdf_bytes: bytes) -> None:
        self.pdf_bytes = pdf_bytes

    def generate_html(self) -> str:
        images = self._process_images()
        html_content = "<!DOCTYPE html><html><body>"

        for i, img in enumerate(images):
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            html_content += f'<img src="data:image/jpeg;base64,{img_str}" ' \
                            f'alt="Page {i + 1}">'
        html_content += "</body></html>"

        return html_content

    def _process_images(self) -> list[Image]:
        pdf_reader = PdfReader(io.BytesIO(self.pdf_bytes))
        num_pages = len(pdf_reader.pages)
        pdf_document = fitz.open(stream=self.pdf_bytes, filetype="pdf")
        images = []

        for page_num in range(num_pages):
            page = pdf_document[page_num]
            image = page.get_pixmap()
            pil_image = Image.frombytes(
                "RGB",
                (image.width, image.height),
                image.samples
            )
            images.append(pil_image)
        pdf_document.close()

        return images
