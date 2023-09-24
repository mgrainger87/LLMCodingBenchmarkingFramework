from abc import ABC, abstractmethod
from llm_types import *
import execution

class Grader(ABC):
	"""
	Abstract base class for graders.
	"""
	
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
	def grade(self, problems: List[ProblemDefinition], solutions: List[LLMSolution]) -> GradingOutput:
		problemGrades = []
		for problem in problems:
			function_prototype = problem.function_prototype
			score = 0
			for solution in solutions:
				if solution.problem_identifier == problem.identifier:
					for test_case in problem.correctness_test_suite:
						actual_result = Grader.run_function(solution.solution_code, function_prototype, test_case)
						expected_result = function_prototype.get_return_values(test_case)
						print(f"Actual: {actual_result}\nExpected: {expected_result}")
						if expected_result == actual_result:
							score += 1
			grade = ProblemGrade(problem.identifier, score)
			problemGrades.append(grade)
		return GradingOutput(ProblemGrade.averageProblemGradeScores(problemGrades), problemGrades)
