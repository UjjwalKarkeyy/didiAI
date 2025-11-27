# DEFINES FILE READING CLASS
import mimetypes
import pdfplumber
from fastapi import HTTPException, UploadFile
from docx import Document
from io import BytesIO

# class to read pdf, txt, docx, etc files
class FileReader:
    def __init__(self, file: UploadFile):
        self.file = file
        self.file_name = file.filename

    async def read_file(self) -> str:
        mime = mimetypes.guess_type(self.file_name)[0]

        file_bytes = await self.file.read()   # read once here
        # if pdf
        if mime == "application/pdf":
            text = self.extract_pdf(file_bytes)
        # if txt
        elif mime == "text/plain":
            text = self.extract_txt(file_bytes)

        # if docx
        elif mime and mime.endswith("wordprocessingml.document"):
            text = self.extract_docx(file_bytes)

        else:
            raise HTTPException(400, "Unsupported file type")
        # strip unnecessary characters
        return self.clean_text(text)

    # ------------ Extractors -------------

    def extract_pdf(self, file_bytes: bytes) -> str:
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        return text

    def extract_txt(self, file_bytes: bytes) -> str:
        return file_bytes.decode("utf-8", errors="ignore")

    def extract_docx(self, file_bytes: bytes) -> str:
        doc = Document(BytesIO(file_bytes))
        return "\n".join([p.text for p in doc.paragraphs])

    # ------------ Cleaning -------------

    def clean_text(self, t: str) -> str:
        t = t.replace("\x00", "")
        t = " ".join(t.split())
        return t.strip()
