"""
PDF text extraction module for resume parsing.
"""
import io
from pypdf import PdfReader
from typing import Optional


def parse_pdf_to_text(file_bytes: bytes) -> str:
    """
    Extract text content from PDF file bytes.
    
    Args:
        file_bytes: Raw bytes of the PDF file
        
    Returns:
        str: Extracted text content from the PDF
        
    Raises:
        ValueError: If PDF cannot be parsed or is empty
        Exception: For other PDF processing errors
    """
    try:
        # Create a BytesIO object from the file bytes
        pdf_file = io.BytesIO(file_bytes)
        
        # Create PDF reader object
        pdf_reader = PdfReader(pdf_file)
        
        # Check if PDF has pages
        if len(pdf_reader.pages) == 0:
            raise ValueError("PDF file contains no pages")
        
        # Extract text from all pages
        extracted_text = ""
        for page_num, page in enumerate(pdf_reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"
            except Exception as e:
                print(f"Warning: Could not extract text from page {page_num + 1}: {str(e)}")
                continue
        
        # Clean up the extracted text
        extracted_text = extracted_text.strip()
        
        if not extracted_text:
            raise ValueError("No text could be extracted from the PDF")
        
        return extracted_text
        
    except ValueError:
        # Re-raise ValueError as is
        raise
    except Exception as e:
        raise Exception(f"Error parsing PDF: {str(e)}")


def validate_pdf_file(file_bytes: bytes) -> bool:
    """
    Validate if the provided bytes represent a valid PDF file.
    
    Args:
        file_bytes: Raw bytes to validate
        
    Returns:
        bool: True if valid PDF, False otherwise
    """
    try:
        pdf_file = io.BytesIO(file_bytes)
        pdf_reader = PdfReader(pdf_file)
        return len(pdf_reader.pages) > 0
    except:
        return False
