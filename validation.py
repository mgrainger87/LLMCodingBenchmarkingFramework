

def validate_parameter(parameter: dict) -> tuple:
	"""
	Validates a Parameter JSON object.

	Args:
	parameter (dict): A dictionary representing a Parameter JSON object.

	Returns:
	tuple: A tuple containing a boolean and a string. The boolean is True if the parameter conforms to the 
		   specified format, False otherwise. The string contains the error message if validation fails.
	"""
	# Check that all required fields are present
	required_fields = ["name", "type"]
	if not all(field in parameter for field in required_fields):
		missing_fields = [field for field in required_fields if field not in parameter]
		return False, f"Missing required fields: {', '.join(missing_fields)}"
	
	# Check that the fields are of the correct type
	if not isinstance(parameter["name"], str) or not isinstance(parameter["type"], str):
		return False, "Both 'name' and 'type' fields must be of type string."

	return True, ""

def validate_return_value(return_value: dict) -> tuple:
	"""
	Validates a ReturnValue JSON object.

	Args:
	return_value (dict): A dictionary representing a ReturnValue JSON object.

	Returns:
	tuple: A tuple containing a boolean and a string. The boolean is True if the return_value conforms to the 
		   specified format, False otherwise. The string contains the error message if validation fails.
	"""
	# Check that all required fields are present
	required_fields = ["type"]
	if not all(field in return_value for field in required_fields):
		missing_fields = [field for field in required_fields if field not in return_value]
		return False, f"Missing required fields: {', '.join(missing_fields)}"
	
	# Check that the fields are of the correct type
	if not isinstance(return_value["type"], str):
		return False, "'type' field must be of type string."

	return True, ""

def validate_function_prototype(function_prototype: dict) -> tuple:
	"""
	Validates a FunctionPrototype JSON object.

	Args:
	function_prototype (dict): A dictionary representing a FunctionPrototype JSON object.

	Returns:
	tuple: A tuple containing a boolean and a string. The boolean is True if the function_prototype conforms to the 
		   specified format, False otherwise. The string contains the error message if validation fails.
	"""
	# Check that all required fields are present
	required_fields = ["function_name", "parameters", "return_values"]
	if not all(field in function_prototype for field in required_fields):
		missing_fields = [field for field in required_fields if field not in function_prototype]
		return False, f"Missing required fields: {', '.join(missing_fields)}"
	
	# Check that the fields are of the correct type
	if not isinstance(function_prototype["function_name"], str):
		return False, "'function_name' field must be of type string."

	# Check that parameters and return_values are arrays
	if not isinstance(function_prototype["parameters"], list) or not isinstance(function_prototype["return_values"], list):
		return False, "'parameters' and 'return_values' fields must be of type array."

	# Validate each Parameter and ReturnValue JSON object
	for param in function_prototype["parameters"]:
		valid, error = validate_parameter(param)
		if not valid:
			return False, f"Invalid Parameter JSON object: {error}"
	
	for ret_val in function_prototype["return_values"]:
		valid, error = validate_return_value(ret_val)
		if not valid:
			return False, f"Invalid ReturnValue JSON object: {error}"

	return True, ""

def validate_test_case(test_case: dict) -> tuple:
	"""
	Validates a TestCase JSON object.

	Args:
	test_case (dict): A dictionary representing a TestCase JSON object.

	Returns:
	tuple: A tuple containing a boolean and a string. The boolean is True if the test_case conforms to the 
		   specified format, False otherwise. The string contains the error message if validation fails.
	"""
	# Check that all required fields are present
	required_fields = ["input", "expected_output"]
	if not all(field in test_case for field in required_fields):
		missing_fields = [field for field in required_fields if field not in test_case]
		return False, f"Missing required fields: {', '.join(missing_fields)}"
	
	# Check that input is an object and expected_output is an array
	if not isinstance(test_case["input"], dict) or not isinstance(test_case["expected_output"], list):
		return False, "'input' field must be of type object and 'expected_output' field must be of type array."

	return True, ""

# Test the updated validate_test_case function
validate_test_case({
	"input": {"a": 5, "b": 3},
	"expected_output": "invalid"
})  # Expected output: (False, "'input' field must be of type object and 'expected_output' field must be of type array.")

def validate_prompt(prompt: dict) -> tuple:
	"""
	Validates a Prompt JSON object.

	Args:
	prompt (dict): A dictionary representing a Prompt JSON object.

	Returns:
	tuple: A tuple containing a boolean and a string. The boolean is True if the prompt conforms to the 
		   specified format, False otherwise. The string contains the error message if validation fails.
	"""
	# Check that all required fields are present
	required_fields = ["prompt_id", "prompt"]
	if not all(field in prompt for field in required_fields):
		missing_fields = [field for field in required_fields if field not in prompt]
		return False, f"Missing required fields: {', '.join(missing_fields)}"
	
	# Check that the fields are of the correct type
	if not isinstance(prompt["prompt_id"], str) or not isinstance(prompt["prompt"], str):
		return False, "Both 'prompt_id' and 'prompt' fields must be of type string."

	# Check that optional fields, if present, are of the correct type
	if "genericize" in prompt and not isinstance(prompt["genericize"], bool):
		return False, "'genericize' field must be of type boolean."
	
	if "sample_inputs_outputs" in prompt:
		if not isinstance(prompt["sample_inputs_outputs"], list):
			return False, "'sample_inputs_outputs' field must be of type array."
		# Validate each TestCase JSON object
		for test_case in prompt["sample_inputs_outputs"]:
			valid, error = validate_test_case(test_case)
			if not valid:
				return False, f"Invalid TestCase JSON object in 'sample_inputs_outputs': {error}"

	if "input_code" in prompt and not isinstance(prompt["input_code"], str):
		return False, "'input_code' field must be of type string."

	return True, ""

def validate_problem_json(problem_json: dict) -> (bool, str):
	"""
	Validates the top-level problem JSON structure.
	
	Args:
	problem_json (dict): A dictionary representing the top-level problem JSON object.
	
	Returns:
	tuple: A tuple containing a boolean and a string. 
	   	The boolean is True if the problem_json conforms to the specified format, False otherwise.
	   	The string provides an error message in case of a failure.
	"""
	# Check that all required fields are present
	required_fields = ["identifier", "prompts"]
	if not all(field in problem_json for field in required_fields):
		missing_fields = [field for field in required_fields if field not in problem_json]
		return False, f"Missing required fields: {', '.join(missing_fields)}"
	
	# Check that the fields are of the correct type
	if not isinstance(problem_json["identifier"], str):
		return False, "Field 'identifier' should be a string"
	
	# Check that prompts, correctness_test_suite, and tags are arrays
	if not isinstance(problem_json["prompts"], list):
		return False, "Field 'prompts' should be an array"
	
	if "correctness_test_suite" in problem_json and not isinstance(problem_json["correctness_test_suite"], list):
		return False, "Field 'correctness_test_suite' should be an array"
	
	if "tags" in problem_json and not isinstance(problem_json["tags"], list):
		return False, "Field 'tags' should be an array"
	
	# Validate each Prompt, TestCase, and FunctionPrototype JSON object
	for index, prompt in enumerate(problem_json["prompts"]):
		valid, error_message = validate_prompt(prompt)
		if not valid:
			return False, f"Invalid prompt at index {index}: {error_message}"
	
	if "correctness_test_suite" in problem_json:
		for index, test_case in enumerate(problem_json["correctness_test_suite"]):
			valid, error_message = validate_test_case(test_case)
			if not valid:
				return False, f"Invalid test case in 'correctness_test_suite' at index {index}: {error_message}"
	
	if "function_prototype" in problem_json:
		valid, error_message = validate_function_prototype(problem_json["function_prototype"])
		if not valid:
			return False, f"Invalid function prototype: {error_message}"
	
	# Check that optional fields, if present, are of the correct type
	if "optimal_solution" in problem_json and not isinstance(problem_json["optimal_solution"], str):
		return False, "Field 'optimal_solution' should be a string"
	
	if "tags" in problem_json and not all(isinstance(tag, str) for tag in problem_json["tags"]):
		return False, "All elements in field 'tags' should be strings"
	
	return True, "Validation successful"
