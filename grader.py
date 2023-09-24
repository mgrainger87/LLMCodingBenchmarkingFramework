from abc import ABC, abstractmethod
from llm_types import *
import execution

class Grader(ABC):
	"""
	Abstract base class for graders.
	"""
	@classmethod
	@property
	@abstractmethod
	def identifier(self):
		pass
	
	@classmethod
	def run_function(cls, code: str, function_prototype: FunctionPrototype, test_case: TestCase) -> str:
		parameters = function_prototype.get_ordered_parameter_values(test_case)
		return execution.execute_function(code, parameters)
		pass
	
	@abstractmethod
	def grade(self, problems: List[ProblemDefinition], solutions: List[LLMSolution]) -> GradingOutput:
		"""
		Grades the provided solutions against the problem definitions.
		"""
		pass
		
	def __str__(self) -> str:
		return f"{self.__class__.__name__}()"
		
class CorrectnessGrader(Grader):
	@classmethod
	@property
	def identifier(self):
		return "correctness"
		
	def grade(self, problems: List[ProblemDefinition], solutions: List[LLMSolution]) -> GradingOutput:
		solutionGrades = []
		for problem in problems:
			function_prototype = problem.function_prototype
			number_correct = 0
			total_tests = 0
			issues = []
			for solution in solutions:
				if solution.problem_identifier == problem.identifier:
					for test_case in problem.correctness_test_suite:
						actual_result = Grader.run_function(solution.solution_code, function_prototype, test_case)
						expected_result = function_prototype.get_return_values(test_case)
						# print(f"Actual: {actual_result}\nExpected: {expected_result}")
						total_tests += 1
						if expected_result == actual_result:
							number_correct += 1
						else:
							issues.append(f"Test failed: {test_case} Result: {actual_result}")
			grade = SolutionGrade(problem.identifier, solution.prompt_identifier, solution.model_identifier, number_correct/total_tests, None, issues)
			solutionGrades.append(grade)
		return GradingOutput(solutionGrades, CorrectnessGrader.identifier)
