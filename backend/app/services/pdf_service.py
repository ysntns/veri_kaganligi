"""
PDF Isleme Servisi
"""
import io
import logging
from typing import Optional

import fitz  # PyMuPDF
import pdfplumber

logger = logging.getLogger(__name__)


class PDFService:
    """PDF dosyalarini isleyen servis"""

    def __init__(self, use_ocr: bool = False):
        self.use_ocr = use_ocr

    def extract_text(self, pdf_content: bytes) -> dict:
        """
        PDF'den metin ve tablo cikarir.

        Args:
            pdf_content: PDF dosyasinin byte icerigi

        Returns:
            {"text": str, "tables": list, "page_count": int, "metadata": dict}
        """
        text_content = ""
        tables = []
        metadata = {}

        try:
            # PyMuPDF ile metin cikarma
            doc = fitz.open(stream=pdf_content, filetype="pdf")
            metadata = {
                "page_count": len(doc),
                "title": doc.metadata.get("title", ""),
                "author": doc.metadata.get("author", ""),
                "subject": doc.metadata.get("subject", "")
            }

            for page_num in range(len(doc)):
                page = doc[page_num]
                text_content += page.get_text()

                # OCR kullanilacaksa resimleri isle
                if self.use_ocr:
                    text_content += self._ocr_images(doc, page)

            doc.close()

            # pdfplumber ile tablo cikarma
            tables = self._extract_tables(pdf_content)

            return {
                "text": self._clean_text(text_content),
                "tables": tables,
                "page_count": metadata["page_count"],
                "metadata": metadata
            }

        except Exception as e:
            logger.error(f"PDF isleme hatasi: {e}")
            raise

    def _extract_tables(self, pdf_content: bytes) -> list:
        """PDF'den tablolari cikarir"""
        tables = []
        try:
            with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
                for page in pdf.pages:
                    page_tables = page.extract_tables()
                    if page_tables:
                        tables.extend(page_tables)
        except Exception as e:
            logger.warning(f"Tablo cikarma hatasi: {e}")
        return tables

    def _ocr_images(self, doc, page) -> str:
        """Sayfa icindeki resimlere OCR uygular"""
        text = ""
        try:
            import pytesseract
            from PIL import Image

            for img in page.get_images(full=True):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                image = Image.open(io.BytesIO(image_bytes))
                text += pytesseract.image_to_string(image, lang='tur') + "\n"

        except ImportError:
            logger.warning("pytesseract yuklenmemis, OCR atlanıyor")
        except Exception as e:
            logger.warning(f"OCR hatasi: {e}")

        return text

    def _clean_text(self, text: str) -> str:
        """Metni temizler"""
        import re
        # Fazla bosluklari temizle
        text = re.sub(r'\s+', ' ', text)
        # Sayfa basi/sonu karakterlerini temizle
        text = re.sub(r'\x0c', '\n\n', text)
        return text.strip()

    def get_page_count(self, pdf_content: bytes) -> int:
        """PDF sayfa sayisini dondurur"""
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        count = len(doc)
        doc.close()
        return count

    def extract_page(self, pdf_content: bytes, page_number: int) -> str:
        """Belirli bir sayfanin metnini cikarir"""
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        if page_number < 0 or page_number >= len(doc):
            raise ValueError(f"Gecersiz sayfa numarasi: {page_number}")

        text = doc[page_number].get_text()
        doc.close()
        return self._clean_text(text)
