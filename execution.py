import sys
import os
from base_types import FunctionPrototype
from typing import *
import traceback
import tempfile
import multiprocessing
import json

def add_line_numbers(text):
	lines = text.split("\n")
	numbered_lines = ["{}: {}".format(i+1, line) for i, line in enumerate(lines)]
	return "\n".join(numbered_lines)
	
def executor_script(function_code_file, parameters_file, result_file):
	try:
		# Load the function code
		with open(function_code_file, 'r') as file:
			function_code = file.read()
		
		# Load the parameters
		with open(parameters_file, 'r') as file:
			parameters = json.load(file)
		
		# Execute the function code to define the function(s)
		exec_globals = {}
		exec(function_code, exec_globals)
		
		# Get the name of the last defined function
		last_function_name = [name for name in exec_globals if callable(exec_globals[name])][-1]
		function = exec_globals[last_function_name]
		# Call the function with the parameters
		result = function(*parameters)
		
		# Write the result to the result file
		# Write the result to the result file as a dictionary
		with open(result_file, 'w') as file:
			json.dump({'result': result}, file)
	except Exception as e:
		# Write any exception to the result file as a dictionary
		with open(result_file, 'w') as file:
			json.dump({'result': None, 'error': str(e), 'traceback': traceback.format_exc()}, file)
	

def execute_function(function_code, parameters):
	try:
		# Create temporary files for function_code, parameters, and result
		function_code_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.py')
		parameters_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json')
		result_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json')
		
		# Write function_code and parameters to temporary files
		function_code_file.write(function_code)
		function_code_file.close()  # Close the file to ensure it's written to disk
		
		json.dump(parameters, parameters_file)
		parameters_file.close()  # Close the file to ensure it's written to disk
		
		# Create a separate Python process to run the executor_script
		process = multiprocessing.Process(target=executor_script, args=(function_code_file.name, parameters_file.name, result_file.name))
		process.start()
		process.join()
		
		# Load the result from the result file
		with open(result_file.name, 'r') as file:
			result_data = json.load(file)
		
		# Clean up temporary files
		os.unlink(function_code_file.name)
		os.unlink(parameters_file.name)
		os.unlink(result_file.name)
		
		# Check for an error in the result data
		if 'error' in result_data:
			error_info = {
				"exception": result_data['error'],
				"traceback": result_data['traceback'],
				"parameters": parameters,
				"function_code": function_code
			}
			# print(f"An error occurred: {error_info}")
			# print(add_line_numbers(function_code))
			# input("Press Enter to continue…")

			return error_info
		
		# Return the result
		return result_data['result']
		
	except Exception as e:
		error_info = {
			"exception": str(e),
			"parameters": parameters,
			"function_code": function_code
		}
		return error_info
