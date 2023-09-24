# LLM Coding Ability Benchmark Suite

The LLM (Large Language Model) Coding Ability Benchmark Suite is designed to evaluate the problem-solving and code generation capabilities of AI models, particularly in the domain of programming challenges. This suite comprises three main phases: Problem Definition, Solution Generation, and Grading. Each phase is structured to facilitate a robust evaluation of AI models, ensuring that the generated solutions not only solve the problems as required but also adhere to specified criteria and standards.

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Usage](#usage)
   - [Problem Definition](#problem-definition)
   - [Solution Generation](#solution-generation)
   - [Grading](#grading)
4. [File Structure](#file-structure)
5. [Contributing](#contributing)
6. [License](#license)

## Overview

The benchmark suite takes problem sets in a defined structured format, provides each problem to an LLM, asks for code that solves the problem, then evaluates the solution on a variety of different factors. Separating these phases allows for a standardized approach to evaluating different AI models on a common ground of programming challenges.

## Quick Start

Get started by running the `benchmark.py` script. Here is an example using built-in problem sets, AIs, and graders:

`python3 benchmark.py --base_path problem_sets/basic/ --generate --grade --model text-davinci-002 --grader performance correctness`

This command provides each problem defined in `problem_sets/basic/problems` to the OpenAI model `text-davinci-002` and grades the resulting code on both correctness and performance.

## Extending the benchmarking suite

### Problem Definition

The first phase of the benchmark suite is defining the problems that the AI models will attempt to solve. Problems are defined in a structured JSON format, which encapsulates various details of a problem including a unique identifier, description, function prototype, and correctness test suite among others. Each problem can also have multiple prompts to guide the AI models in generating solutions.

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
	
	def generate_solution(self, problem_input: LLMProblemInput) -> 'LLMSolution':
		# ... (implementation of generate_solution)
		pass

my_querier = MyQuerier(model_identifier="claude")
solution = my_querier.generate_solution(problem_input)
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

## File Structure

_Describe the file structure of the benchmark suite, explaining where to find key components and data._

## Contributing

_Guidelines for contributing to the benchmark suite._

## License

_License information for the benchmark suite._

---

This README provides a high-level overview of the LLM Coding Ability Benchmark Suite. Detailed documentation, including class definitions, method signatures, and examples, can be found within the codebase.