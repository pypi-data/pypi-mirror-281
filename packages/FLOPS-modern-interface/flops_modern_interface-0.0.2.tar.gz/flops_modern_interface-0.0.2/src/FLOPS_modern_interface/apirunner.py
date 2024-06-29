from pydantic import BaseModel
import requests
import os

from .input import FLOPSInput
from .output import FLOPSOutput


class FLOPSInputResponse(BaseModel):
    Input: FLOPSInput
    Warnings: list[str]

def parse_flops_input(fortran_input: str, api_endpoint: str):
    url = api_endpoint + "/parse-fortran-input"
    headers = {"Content-Type": "application/json"}
    verify = os.environ.get("VERIFY") != "False"
    response = requests.post(url, json=fortran_input, headers=headers, verify=verify)
    if not response.ok:
        print(response.text)
    input = FLOPSInputResponse.model_validate_json(response.text)
    for i, warning in enumerate(input.Warnings):
        print(f"Warning {i}: {warning}")
    return input.Input


def run_flops_api_from_input(input_data: FLOPSInput, api_endpoint: str):
    url = api_endpoint + "/run-flops"
    payload = input_data.model_dump(mode="json", exclude_defaults=True)
    headers = {"Content-Type": "application/json"}
    verify = os.environ.get("VERIFY") != "False"
    response = requests.post(url, json=payload, headers=headers, verify=verify)
    if not response.ok:
        print(response.text)
    output = FLOPSOutput.model_validate_json(response.text)
    return output
