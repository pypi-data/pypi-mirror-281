import os
import subprocess
import tempfile
import shutil

from .input import FLOPSInput
from .output import FLOPSOutput

def input_from_json(json_data: str) -> FLOPSInput:
    return FLOPSInput.model_validate_json(json_data)

def input_from_json_file(path: str) -> FLOPSInput:
    with open(path, "r", encoding="utf-8") as f:
        json_data = f.read()
        return input_from_json(json_data)

def output_from_json(json_data: str) -> FLOPSOutput:
    return FLOPSOutput.model_validate_json(json_data)

def output_from_json_file(path: str) -> FLOPSOutput:
    with open(path, "r", encoding="utf-8") as f:
        json_data = f.read()
        return output_from_json(json_data)

def input_to_json(input_data: FLOPSInput) -> str:
    return input_data.model_dump_json(exclude_defaults=True)

def input_to_json_file(input_data: FLOPSInput, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json_data = input_to_json(input_data)
        f.write(json_data)

def output_to_json(output_data: FLOPSOutput) -> str:
    return output_data.model_dump_json()

def output_to_json_file(output_data: FLOPSOutput, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json_data = output_to_json(output_data)
        f.write(json_data)

def run_flops_from_json_file(path: str, flops_directory: str):
    inPath = os.path.abspath(path) # os.path.join(flopsDirectory, os.path.splitext(os.path.basename(tempName))[0] + ".in")
    exe_path = os.path.abspath(os.path.join(flops_directory, "FLOPS.exe"))
    subprocess.run([exe_path, "run", inPath], check=True)

def run_flops_from_input(input_data: FLOPSInput, flops_directory: str):
    temp_dir = tempfile.mkdtemp()
    temp_in = os.path.join(temp_dir, "data.in.json")
    temp_out = os.path.join(temp_dir, "data.out.json")

    input_to_json_file(input_data, temp_in)
    run_flops_from_json_file(temp_in, flops_directory)
    output = output_from_json_file(temp_out)
    shutil.rmtree(temp_dir)
    return output