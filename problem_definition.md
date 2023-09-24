
# Problem Definition JSON specification

## Top-Level Problem JSON Structure

```json
{
	"identifier": "<string>",
	"description": "<string>",
	"prompts": [
		<Prompt JSON Object>,
		...
	],
	"function_prototype": <FunctionPrototype JSON Object>,
	"correctness_test_suite": [
		<TestCase JSON Object>,
		...
	],
	"optimal_solution": "<string> (Optional)",
	"additional_instructions": "<string> (Optional)",
	"tags": [
		"<string>",
		...
	] (Optional)
}
```

### Fields Description:

1. **identifier** (String):
	- A string representing the unique identifier of the problem definition.
  
2. **description** (String):
	- A string providing a description of the problem definition.

3. **prompts** (Array of `Prompt` JSON Objects):
	- An array of JSON objects representing the prompts. Each object should adhere to the JSON format expected by the `Prompt` class.

4. **function_prototype** (`FunctionPrototype` JSON Object):
	- A JSON object representing the function prototype. The object should adhere to the JSON format expected by the `FunctionPrototype` class.

5. **correctness_test_suite** (Array of `TestCase` JSON Objects, Optional):
	- An optional array of JSON objects representing the test cases for correctness. Each object should adhere to the JSON format expected by the `TestCase` class. If not provided, the default value is an empty array.

6. **optimal_solution** (String, Optional):
	- An optional string representing the optimal solution to the problem. If not provided, the default value is `null`.

7. **additional_instructions** (String, Optional):
	- An optional string providing additional instructions for the problem definition. If not provided, the default value is `null`.

8. **tags** (Array of Strings, Optional):
	- An optional array of strings representing tags associated with the problem definition. If not provided, the default value is `null`.

### Notes:

- The optional fields (`correctness_test_suite`, `optimal_solution`, `additional_instructions`, and `tags`) will have their default values if they are not provided in the JSON object.


## `FunctionPrototype` JSON Structure:

```json
{
	"function_name": "<string>",
	"parameters": [
		<Parameter JSON Object>,
		...
	],
	"return_values": [
		<ReturnValue JSON Object>,
		...
	]
}
```

### Fields Description:

- **function_name** (String):
	- A string representing the name of the function.
  
- **parameters** (Array of `Parameter` JSON Objects):
	- An array of JSON objects representing the parameters of the function. Each object should adhere to the JSON format expected by the `Parameter` class.

- **return_values** (Array of `ReturnValue` JSON Objects):
	- An array of JSON objects representing the return values of the function. Each object should adhere to the JSON format expected by the `ReturnValue` class.


## `Parameter` JSON Structure

```json
{
	"name": "<string>",
	"type": "<string>"
}
```

### Fields Description:

- **name** (String):
	- A string representing the name of the parameter.

- **type** (String):
	- A string representing the type of the parameter.


## `ReturnValue` JSON Structure

```json
{
	"type": "<string>"
}
```

### Fields Description

- **type** (String):
	- A string representing the type of the return value.


## `TestCase` JSON Structure:

```json
{
	"input": {
		"<parameter_name>": "<parameter_value>",
		...
	},
	"expected_output": {
		"<output_name>": "<output_value>",
		...
	}
}
```

### Fields Description

- **input** (Object):
	- An object where each key-value pair represents a parameter name and its corresponding value.

- **expected_output** (Object):
	- An object where each key-value pair represents an output name and its corresponding expected value.


## `Prompt` JSON Structure

```json
{
	"prompt_id": "<string>",
	"prompt": "<string>",
	"genericize": <boolean>,
	"sample_inputs_outputs": [
		<TestCase JSON Object>,
		...
	],
	"input_code": "<string> (Optional)"
}
```

### Fields Description

- **prompt_id** (String):
	- A string representing the unique identifier of the prompt.

- **prompt** (String):
	- A string representing the text of the prompt.

- **genericize** (Boolean):
	- A boolean value indicating whether to genericize the prompt or not.

- **sample_inputs_outputs** (Array of `TestCase` JSON Objects):
	- An array of JSON objects representing the sample inputs and outputs. Each object should adhere to the JSON format expected by the `TestCase` class.

- **input_code** (String, Optional):
	- An optional string representing the input code for the prompt. If not provided, the default value is `null`.
