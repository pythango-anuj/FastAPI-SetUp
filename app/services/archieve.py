import os
import shutil
import subprocess
from app.schemas.services.archieve import (
    ArchieveInputSchema,
    ArchieveOutputSchema, 
    ArchieveFormatEnum,
    StatusEnum
)
from app.utils.result import ServiceResult
from app.utils.exceptions import AppException


class ArchieveService:
    def __init__(self, data: ArchieveInputSchema) -> None:
        self.input_path = data.input_path
        self.ouput_format = data.output_format
        self.ext_name = os.path.splitext(os.path.basename(self.input_path))[1][1:]
        self.file_name = os.path.splitext(os.path.basename(self.input_path))[1]
    
    
    def create_output_path(self):
        output_dir = "outputs/archieve"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = f"{output_dir}/{self.file_name}.{self.ext_name}"
        return output_path
    
    def __call__(self):
        try:
            output_path = self.create_output_path(
                input_path=self.input_path,
                output_format=self.ouput_format
            )
            converter = ArchieveConverter(
                input_path=self.input_path,
                output_path=output_path
                )
            if self.ext_name == ArchieveFormatEnum.ZIP:
                status, output_path, message = converter.from_zip_to_7z()

            elif self.ext_name == ArchieveFormatEnum._7Z:
                status, output_path, message = converter.from_7z_to_rar()

            elif self.ext_name == ArchieveFormatEnum.RAR:
                status, output_path, message = converter.from_rar_to_zip()
            
            response = ArchieveOutputSchema(
                status = status,
                output_pdf = output_path,
                message = message
            )
            return ServiceResult(response)

        except Exception as e:
            return ServiceResult(AppException.RunProcess({"Error during conversion": e}))


class ArchieveConverter:
    def __init__(self, input_path, output_path) -> None:
        self.input_path = input_path
        self.output_path = output_path

    def from_zip_to_7z(self):
        try:
            # Command: 7z a output.7z input.zip
            subprocess.run(["/usr/bin/7z", "a", self.output_path, self.input_path], check=True)
            status = StatusEnum.SUCCESS
            message = f"Conversion Successfull from {self.input_path} -> {self.output_path}"

        except Exception as e:
            status = StatusEnum.FAILED
            message = f"Error during conversion: {e}"
            output_path = None
        
        finally:
            return status, output_path, message


    def from_7z_to_rar(self):
        try:
            # Command: 7z e input.7z -ooutput && rar a output.rar output
            subprocess.run(["/usr/bin/7z", "e", self.input_path, "-odump", "&&"], check=True)
            if not os.path.exists("dump"):
                os.makedirs("dump")
            subprocess.run(["rar", "a", self.output_path, "dump"], check=True)
            status = StatusEnum.SUCCESS
            message = f"Conversion Successfull from {self.input_path} -> {self.output_path}"

        except Exception as e:
            status = StatusEnum.FAILED
            message = f"Error during conversion: {e}"
            output_path = None
            
        finally:
            os.rmdir("dump")
            return status, output_path, message


    # Method to convert from rar to zip
    def from_rar_to_zip(self):
        try:
            # Extract the contents of the RAR file
            extract_command = ["unrar", "x", self.input_path]
            subprocess.run(extract_command, check=True)
            print(f"Extraction successful: {self.input_path}")

            # Get the base name of the RAR file (excluding extension)
            base_name = os.path.splitext(os.path.basename(self.input_path))[0]
            # Create a ZIP archive from the extracted contents
            zip_command = ["zip", "-r", self.output_path, base_name]
            
            subprocess.run(zip_command, check=True)
            status = StatusEnum.SUCCESS
            message = f"Conversion Successfull from {self.input_path} -> {self.output_path}"

        except Exception as e:
            status = StatusEnum.FAILED
            message = f"Error during conversion: {e}"
            output_path = None

        finally:
            # Clean up the extracted contents
            shutil.rmtree(base_name, ignore_errors=True)

            return status, output_path, message
