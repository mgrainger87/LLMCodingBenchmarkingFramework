from abc import ABC, abstractmethod
from typing import Dict, List, Union, Optional, Any
from llm_types import *

class AIModel(ABC):
	"""
	Abstract base class for AI models.
	"""
	
	@classmethod
	def construct_textual_prompt(cls, llm_problem_input: LLMProblemInput) -> str:
		# Start with the textual prompt
		prompt_text = llm_problem_input.prompt
	
		# Add function prototype if available
		function_prototype = llm_problem_input.function_prototype
		if function_prototype:
			prompt_text += f"\n\nFunction Signature:\n{str(function_prototype)}"
	
		# Add sample inputs and outputs if available
		sample_io = llm_problem_input.sample_inputs_outputs
		if sample_io:
			sample_io_text = '\n\nSample Inputs and Outputs:\n'
			for i, test_case in enumerate(sample_io, start=1):
				sample_io_text += f"\nTest Case {i}:\n{str(test_case)}"
			prompt_text += sample_io_text
	
		# Add input code if available
		input_code = llm_problem_input.input_code
		if input_code:
			prompt_text += f"\n\nInput Code:\n{input_code}"
	
		return prompt_text
	
	@abstractmethod
	def generate_solution(self, problem_input: LLMProblemInput) -> 'LLMSolution':
		"""
		Generates a solution for the given problem definition.
		
		Subclasses should override this method to provide the logic for
		generating solutions.
		
		:param problem_definition: The problem definition for which to generate a solution.
		:return: An LLMSolution object containing the generated solution.
		"""
		pass
		
	def __str__(self) -> str:
		return f"{self.__class__.__name__}()"

class HumanAIModel(AIModel):
	def generate_solution(self, problem_input: LLMProblemInput) -> 'LLMSolution':
		prompt = AIModel.construct_textual_prompt(problem_input)
		response = querier.HumanQuerier().performQuery(prompt)
		return LLMSolution(problem_input.problem_id, "human", problem_input.prompt_id, response)

