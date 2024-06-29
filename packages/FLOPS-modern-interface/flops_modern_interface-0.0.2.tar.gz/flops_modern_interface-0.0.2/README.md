# FLOPS python

"Python pydantic classes for FLOPS input/output and web service"

Run from web service:

```python
# Path to your input file
input_file = "your-input-file.in.json"

# Parse input file and update input values if needed
flops_input = flops.input_from_json_file(input_file)
flops_input.CONFIN.DESRNG = 1800

# Execute from web API
url = "https://your-python-web-service-url.net"
flops_output = flops.run_flops_api_from_input(flops_input, url)

# Process output
print(flops_output.OBJ_VAR_CONSTR_SUMMARY.RANGE)
```

Run locally:

```python
# Path to your flops directory and input file
flops_directory = "path/to/flops/folder"
input_file = "your-input-file.in.json"

# Execute directly from file (generates test.out.json file)
flops.run_flops_from_json_file(input_file, flops_directory)

# Or parse input from  and update input values if needed Inspect output object.
flops_input = flops.input_from_json_file(input_file)
flops_input.CONFIN.DESRNG = 2200

# Execute locally
flops_output = flops.run_flops_from_input(flops_input, flops_directory)

# Process output
print(flops_output.OBJ_VAR_CONSTR_SUMMARY.RANGE)
```