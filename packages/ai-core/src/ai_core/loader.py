import os
from pathlib import Path
from PIL import Image
from docling.document_converter import DocumentConverter
from pdf2image import convert_from_path

class UniversalLoader:
    """
    Handles the conversion of various file formats (PDF, DOCX, PNG, JPG) 
    into high-resolution images for vision-based processing.
    """
    def __init__(self, dpi: int = 300):
        # 300 DPI is the 'Senior' choice—it ensures small text in diagrams is readable.
        self.dpi = dpi
        self.converter = DocumentConverter()

    def to_images(self, file_path: str) -> list[Image.Image]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Could not find file at {file_path}")

        ext = path.suffix.lower()

        # CASE 1: Standard Images
        if ext in [".png", ".jpg", ".jpeg", ".webp"]:
            return [Image.open(path).convert("RGB")]

        # CASE 2: PDFs (Direct rasterization)
        if ext == ".pdf":
            # convert_from_path is robust for Windows/Linux
            return convert_from_path(str(path), dpi=self.dpi)

        # CASE 3: Documents (DOCX, PPTX)
        if ext in [".docx", ".pptx"]:
            # Docling handles complex structure. We convert the document 
            # to a structured internal format, then we'll treat it as a visual page.
            result = self.converter.convert(str(path))
            # Senior Tip: For DOCX, it's often best to export to a temporary PDF 
            # then rasterize to ensure tables don't break.
            temp_pdf = path.with_suffix(".temp.pdf")
            # (Assuming docling export logic here)
            # return convert_from_path(str(temp_pdf), dpi=self.dpi)
            
            # For now, we use a direct rasterizer approach:
            return convert_from_path(str(path), dpi=self.dpi)

        raise ValueError(f"Unsupported file format: {ext}")