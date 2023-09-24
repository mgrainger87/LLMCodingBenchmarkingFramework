# LLM Coding Ability Benchmark Suite

The LLM (Large Language Model) Coding Ability Benchmark Suite is designed to evaluate the problem-solving and code generation capabilities of AI models, particularly in the domain of programming challenges. This suite comprises three main phases: Problem Definition, Solution Generation, and Grading. Each phase is structured to facilitate a robust evaluation of AI models, ensuring that the generated solutions not only solve the problems as required but also adhere to specified criteria and standards.

## Overview

The benchmark suite takes problem sets in a defined structured format, provides each problem to an LLM, asks for code that solves the problem, then evaluates the solution on a variety of different factors. Separating these phases allows for a standardized approach to evaluating different AI models on a common ground of programming challenges.

## Quick Start

Get started by running the `benchmark.py` script. Here is an example using built-in problem sets, AIs, and graders:

`python3 benchmark.py --base_path problem_sets/bugfixing/ --grade --model gpt-4 --grader performance correctness`

This command provides each problem defined in `problem_sets/bugfixing/problems` to the OpenAI model `gpt-4` and grades the resulting code on both correctness and performance.

## Extending the benchmarking suite

### Problem Definition

The first phase of the benchmark suite is defining the problems that the AI models will attempt to solve. Problems are defined in a structured JSON format, which encapsulates various details of a problem including a unique identifier, description, function prototype, and correctness test suite among others. Each problem can also have multiple prompts to guide the AI models in generating solutions.

For more details on the problem definition JSON format, see the [full specification](problem_definition.md).

Here is an example of a basic problem definition:

```json
{
	"identifier": "add_numbers",
	"description": "Write a function to add two numbers.",
	"function_prototype": {
		"function_name": "add",
		"parameters": [{"name": "a", "type": "int"}, {"name": "b", "type": "int"}],
		"return_values": [{"type": "int"}]
	},
	"correctness_test_suite": [
		{"input": {"a": 1, "b": 2}, "expected_output": [3]},
		{"input": {"a": -1, "b": 2}, "expected_output": [1]}
	],
	"tags": ["Arithmetic", "Easy"],
	"prompts": [
		{
			"prompt_id": "detailed_prompt",
			"prompt": "Write a function named 'add' that takes two integer arguments, 'a' and 'b', and returns their sum as an integer.",
		}
	]
}
```

Each problem definition goes in a separate file in the `problems` directory for the problem set.

Here is an example of a more complex problem description that asks an LLM to correct buggy code. It defines input code and test cases to be provided to the LLM, an optimal solution, and multiple prompts.

```json
{
	"identifier": "multiply_numbers",
	"description": "Debug and fix the function to multiply two numbers.",
	"prompts": [
		{
			"prompt_id": "brief_prompt",
			"prompt": "The provided function `multiply` attempts to return the product of two integers, but it contains bugs. Debug and fix the function to return the correct product.",
			"genericize": false,
			"sample_inputs_outputs": [
				{"input": {"a": 5, "b": 6}, "expected_output": [30]},
				{"input": {"a": 8, "b": 3}, "expected_output": [24]}
			],
			"input_code": "def multiply(a: int, b: int) -> int:\n    return a + b"
		},
		{
			"prompt_id": "detailed_prompt",
			"prompt": "The function named 'multiply' is intended to take two integer arguments, 'a' and 'b', and return their product as an integer. However, it contains bugs. Debug and fix the function to ensure it returns the correct product.",
			"genericize": true,
			"sample_inputs_outputs": [
				{"input": {"a": 5, "b": 6}, "expected_output": [30]},
				{"input": {"a": 8, "b": 3}, "expected_output": [24]}
			],
			"input_code": "def multiply(a: int, b: int) -> int:\n    return a * b * 2  # bug: incorrect operation"
		}
	],
	"function_prototype": {
		"function_name": "multiply",
		"parameters": [{"name": "a", "type": "int"}, {"name": "b", "type": "int"}],
		"return_values": [{"type": "int"}]
	},
	"correctness_test_suite": [
		{"input": {"a": 4, "b": 3}, "expected_output": [12]},
		{"input": {"a": 7, "b": 2}, "expected_output": [14]}
	],
	"optimal_solution": "def multiply(a: int, b: int) -> int:\n    return a * b",
	"additional_instructions": "Ensure that your function handles negative numbers as well.",
	"tags": ["Debugging", "Easy"]
}
```

### Solution Generation

In the Solution Generation phase, AI models generate solutions for the defined problems.

The problem definition is converted to a prompt like the following:

```
The provided function `add` attempts to return the sum of two integers, but it contains bugs. Debug and fix the function to return the correct sum.

Function Signature:
add(a: int, b: int) -> int

Sample Inputs and Outputs:

Test Case 1:
Input: a = 5, b = 6
Expected Output: 11
Test Case 2:
Input: a = 8, b = 3
Expected Output: 11

Input Code:
def add(a: int, b: int) -> int:
	return a - b
```

#### Queriers
The test suite has two built-in queriers:

- `OpenAIModelQuerier`, which uses the OpenAI API to interact with any model supported by the API
- `HumanAIModelQuerier`, which provides prompts at the command line to be copied and pasted into LLMs.

The test suite will determine which querier to use based on the model name passed in. It first checks it to see if the OpenAI API handles it; if not, it falls back to the human querier.

Adding new queriers is straightforward. Simply extend the abstract base class `AIModelQuerier`, and implement the `generate_solution` method to provide logic for generating solutions. The `LLMProblemInput` class is used to encapsulate the input data for the AI models, while the `LLMSolution` class is used to encapsulate the generated solutions.

Example:

```python
from llm_types import AIModelQuerier, LLMProblemInput, LLMSolution

class MyQuerier(AIModelQuerier):
	def __init__(self, model_identifier: str):
		super().__init__(model_identifier)
	
	@classmethod
	def supported_model_names(cls):
		# ... (determine which model names are supported by this querier)
		pass
	
	def generate_solution(self, problem_input: LLMProblemInput) -> 'LLMSolution':
		# ... (implementation of generate_solution)
		pass

my_querier = MyQuerier(model_identifier="claude")
solution = my_querier.generate_solution(problem_input)
```

#### Solution JSON format

After the querier returns solutions for the provided problems, the resulting `LLMSolution` can be serialized in the following format. For more details on the JSON format, see the [full specification](querier_format.md).

```json
{
	"problem_identifier": "problem_1",
	"model_identifier": "text-davinci-002",
	"prompt_identifier": "brief_prompt",
	"solution_code": "\"\"\"\n\ndef add(a, b):\n    # fill in your code here\n    return a + b",
	"feedback": null
}
```

### Grading

The Grading phase evaluates the generated solutions against the defined problems and grading criteria. The `SolutionGrade` class captures the grading details for each solution, and the `GradingOutput` class encapsulates the overall grading output. A `Grader` abstract base class provides the interface that subclasses implement for grading the solutions, which can be customized to suit different grading criteria and requirements.

The test suite includes `correctness` and `performance` graders; new graders can be added by creating new subclasses of `Grader`.

Example:

```python
from llm_types import Grader, SolutionGrade, GradingOutput

class MyGrader(Grader):
	def grade(self, problem_definitions, solutions) -> GradingOutput:
		# ... (implementation of grading logic)
		pass

my_grader = MyGrader()
grading_output = my_grader.grade(problem_definitions, solutions)
```

### Grader output JSON format

Here is an example grading JSON output. For more details on the JSON format, see the [full specification](grader_format.md).

```json
{
"problem_identifier": "problem_1",
"prompt_identifier": "detailed_prompt",
"model_identifier": "text-davinci-002",
"score": 0.8,
"sub_criteria_scores": null,
"issues": [
	"Test failed: Input: a = 1, b = 2\nExpected Output: 3 Result: {'exception': 'EOF while scanning triple-quoted string literal (<string>, line 5)', 'traceback': 'Traceback (most recent call last):\\n  File \"/Users/morgang/code/LLMCodingBenchmarkingFramework/execution.py\", line 27, in executor_script\\n    exec(function_code, exec_globals)\\n  File \"<string>\", line 5\\n    \"\"\"\\n\\ndef add(a, b):\\n    # fill in your code here\\n    return a + b\\n       \\n\\n              \\n                            \\n                ^\\nSyntaxError: EOF while scanning triple-quoted string literal\\n', 'parameters': [1, 2], 'function_code': '\"\"\"\\n\\ndef add(a, b):\\n    # fill in your code here\\n    return a + b'}"
]
```


## File Structure

The framework separates different phases, models, and graders into distinct directories and files.

The directory structure of the Benchmarking Framework is as follows:

- **problem_sets**:
	- **<problem_set_name>**:
		- **problems**:
			- Contains JSON files for each problem (e.g., `problem_1.json`).
		- **solutions**:
			- Contains JSON files for solutions to each problem, named the same as the problems (e.g., `problem_1.json`).
			- **<model_name>**:
				- Each problem has its own directory (e.g., `problem_1`), within which there is a JSON file for each prompt with the model's solution for that prompt.
		- **grades**:
			- **text-davinci-002**:
				- **<grader**:
					- Each problem has its own directory (e.g., `problem_1`), within which there is a JSON file for each prompt with the grading information for that prompt.
	- **bugfixing**:
		- Similar structure to the `basic` directory but tailored for bugfixing problems.

Some additional notes:

- Each problem set (e.g., `basic`, `bugfixing`) has a similar structure containing directories for grades, problems, and solutions.
- The `problems` directory holds the problem definition files in JSON format for each problem within the problem set.
- The `solutions` directory contains sub-directories for different models, with each problem having its own folder containing `brief_prompt.json` and `detailed_prompt.json` files, likely representing different levels of solution details.
- Within the `grades` directory, different AI models (e.g., `text-davinci-002`) have their own sub-directories, further subdivided by grader (e.g. `correctness` and `performance`). Each problem within these sub-directories has a dedicated folder containing a JSON file for each prompt that holds grading details.

This structured setup facilitates the organization of problems, solutions, and grading details, making it easier to manage and navigate the benchmarking framework.

## Regenerating the Suite Itself Using LLMs

See [regenerate_framework.py](regenerate_framework.py) for an early look at an attempt to regenerate this testing suite by prompting an LLM!