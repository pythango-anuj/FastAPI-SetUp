from pydantic import BaseModel, FilePath
from typing import Optional
from enum import Enum


# Enum class for status options
class StatusEnum(str, Enum):
    SUCCESS = "success"
    FAILED = "Failed"


# Archieve FormatEnum
class ArchieveFormatEnum(str, Enum):
    _7Z = '7z'
    RAR = 'rar'
    ZIP = 'zip'
    


# Archieve Conversion Input Schema
class ArchieveInputSchema(BaseModel):
    input_path: FilePath
    output_format: ArchieveFormatEnum
    

# Archieve Conversion Output Schema
class ArchieveOutputSchema(BaseModel):
    status: StatusEnum
    output_pdf: Optional[FilePath] = None
    message: str

