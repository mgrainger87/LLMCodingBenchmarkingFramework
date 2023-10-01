from abc import ABC, abstractmethod
from base_types import *
import execution
import time

class Grader(ABC):
	"""
	Abstract base class for graders.
	"""
	@classmethod
	@property
	@abstractmethod
	def identifier(self) -> str:
		"""
		A human-readable identifier for the grader.
		"""
		pass
		
	@classmethod
	def resolve_graders(cls, grader_names: List[str]) -> List['Grader']:
		subclass_mapping = {subclass.identifier: subclass for subclass in cls.__subclasses__()}
		instances = []
		for grader_name in grader_names:
			subclass = subclass_mapping.get(grader_name, CorrectnessGrader)
			instances.append(subclass())
		return instances
	
	@classmethod
	def run_function(cls, code: str, function_prototype: FunctionPrototype, test_case: TestCase) -> str:
		"""
		Runs generated Python code against a given test case.
		"""
		parameters = function_prototype.get_ordered_parameter_values(test_case)
		return execution.execute_function(code, parameters)
		pass
		
	@classmethod
	def can_grade(cls, problems: List[ProblemDefinition]) -> bool:
		"""
		Check if the current grader is capable of running the problem set.
		This method should be overridden by a child class if said class has stricter requirements.
		"""
		for p in problems:
			if not (all(var is not None for var in (p.identifier, p.description, p.prompts, p.function_prototype)) and len(p.prompts) > 0):
				return False
		return True
	
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
			for solution in solutions:
				number_correct = 0
				total_tests = 0
				issues = []
				if solution.problem_identifier == problem.identifier:
					for test_case in problem.correctness_test_suite:
						actual_result = Grader.run_function(solution.solution_code, function_prototype, test_case)
						expected_result = function_prototype.get_return_values(test_case)
						total_tests += 1
						if expected_result == actual_result:
							number_correct += 1
						else:
							issues.append(f"Test failed: {test_case} Result: {actual_result}")
							
					score = 0
					if total_tests > 0:
						score = number_correct / total_tests
					grade = SolutionGrade(problem.identifier, solution.prompt_identifier, solution.model_identifier, score, None, issues)
					solutionGrades.append(grade)
		return GradingOutput(solutionGrades, self.identifier)

class PerformanceGrader(Grader):
	@classmethod
	@property
	def identifier(self):
		return "performance"
		
	def grade(self, problems: List[ProblemDefinition], solutions: List[LLMSolution]) -> GradingOutput:
		solutionGrades = []
		for problem in problems:
			function_prototype = problem.function_prototype
			for solution in solutions:
				if solution.problem_identifier == problem.identifier:
					total_solution_time = 0
					total_optimal_time = 0
					issues = []
					for test_case in problem.correctness_test_suite:
						start_time = time.process_time()
						Grader.run_function(solution.solution_code, function_prototype, test_case)
						end_time = time.process_time()
						total_solution_time = end_time - start_time

						start_time = time.process_time()
						Grader.run_function(problem.optimal_solution, function_prototype, test_case)
						end_time = time.process_time()
						total_optimal_time = end_time - start_time
						
					grade = SolutionGrade(problem.identifier, solution.prompt_identifier, solution.model_identifier, total_solution_time/total_optimal_time, None, issues)
					solutionGrades.append(grade)
		return GradingOutput(solutionGrades, self.identifier)

from typing import Set

class HumanLikeGrader(Grader):
    @classmethod
    @property
    def identifier(self):
        return "humanlikeness"

    @staticmethod
    def jaccard_distance(set1: Set, set2: Set) -> float:
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return 1 - (intersection / union) if union != 0 else 0

    def grade(self, problems: List[ProblemDefinition], solutions: List[LLMSolution]) -> GradingOutput:
        solutionGrades = []
        for problem in problems:
            function_prototype = problem.function_prototype
            for solution in solutions:
                issues = []
                if solution.problem_identifier == problem.identifier:
                    ai_solution_tokens = set(solution.solution_code.split())
                    optimal_solution_tokens = set(problem.optimal_solution.split())
                    distance = self.jaccard_distance(ai_solution_tokens, optimal_solution_tokens)

                    score = 1 - distance

                    grade = SolutionGrade(problem.identifier, solution.prompt_identifier, solution.model_identifier, score, None, issues)
                    solutionGrades.append(grade)
        return GradingOutput(solutionGrades, self.identifier)


class CorrectnessGrader(Grader):
	@classmethod
	@property
	def identifier(self):
		return "correctness"

	def grade(self, problems: List[ProblemDefinition], solutions: List[LLMSolution]) -> GradingOutput:
		solutionGrades = []
		for problem in problems:
			function_prototype = problem.function_prototype
			for solution in solutions:
				number_correct = 0
				total_tests = 0
				issues = []
				if solution.problem_identifier == problem.identifier:
					for test_case in problem.correctness_test_suite:
						actual_result = Grader.run_function(solution.solution_code, function_prototype, test_case)
						expected_result = function_prototype.get_return_values(test_case)
						total_tests += 1
						if expected_result == actual_result:
							number_correct += 1
						else:
							issues.append(f"Test failed: {test_case} Result: {actual_result}")

					score = 0
					if total_tests > 0:
						score = number_correct / total_tests
					grade = SolutionGrade(problem.identifier, solution.prompt_identifier, solution.model_identifier,
										  score, None, issues)
					solutionGrades.append(grade)
		return GradingOutput(solutionGrades, self.identifier)


class PerformanceGrader(Grader):
	@classmethod
	@property
	def identifier(self):
		return "performance"

	def grade(self, problems: List[ProblemDefinition], solutions: List[LLMSolution]) -> GradingOutput:
		solutionGrades = []
		for problem in problems:
			function_prototype = problem.function_prototype
			for solution in solutions:
				if solution.problem_identifier == problem.identifier:
					total_solution_time = 0
					total_optimal_time = 0
					issues = []
					for test_case in problem.correctness_test_suite:
						start_time = time.process_time()
						Grader.run_function(solution.solution_code, function_prototype, test_case)
						end_time = time.process_time()
						total_solution_time = end_time - start_time

						start_time = time.process_time()
						Grader.run_function(problem.optimal_solution, function_prototype, test_case)
						end_time = time.process_time()
						total_optimal_time = end_time - start_time

					grade = SolutionGrade(problem.identifier, solution.prompt_identifier, solution.model_identifier,
										  total_solution_time / total_optimal_time, None, issues)
					solutionGrades.append(grade)
		return GradingOutput(solutionGrades, self.identifier)


from memory_profiler import memory_usage


class SpaceEfficiencyGrader(Grader):
	@classmethod
	@property
	def identifier(self):
		return "memory_efficiency"

	def grade(self, problems: List[ProblemDefinition], solutions: List[LLMSolution]) -> GradingOutput:
		solutionGrades = []
		for problem in problems:
			for solution in solutions:
				if solution.problem_identifier == problem.identifier:
					accumulated_memory_ratio = 0
					test_cases_count = len(problem.correctness_test_suite)

					for test_case in problem.correctness_test_suite:
						# Measure memory used by the solution
						solution_memory_usage = memory_usage(
							(Grader.run_function, (solution.solution_code, problem.function_prototype, test_case)),
							max_usage=True, interval=0.1, timeout=None)
						solution_memory = solution_memory_usage if solution_memory_usage else 0

						# Measure memory used by the optimal solution
						optimal_memory_usage = memory_usage(
							(Grader.run_function, (problem.optimal_solution, problem.function_prototype, test_case)),
							max_usage=True, interval=0.1, timeout=None)
						optimal_memory = optimal_memory_usage if optimal_memory_usage else 0

						# Compute the ratio of solution memory to optimal memory
						memory_ratio = solution_memory / optimal_memory if optimal_memory != 0 else 0
						accumulated_memory_ratio += memory_ratio

					# Average the memory ratios across all test cases
					averaged_memory_ratio = accumulated_memory_ratio / test_cases_count if test_cases_count != 0 else 0

					grade = SolutionGrade(
						problem.identifier,
						solution.prompt_identifier,
						solution.model_identifier,
						averaged_memory_ratio,
						None,
						[]
					)
					solutionGrades.append(grade)
		return GradingOutput(solutionGrades, self.identifier)


import re


class CodingConventionGrader(Grader):
	@classmethod
	@property
	def identifier(self):
		return "coding_convention"

	def _check_line_length(self, code: str) -> List[str]:
		return [f"Line {i + 1} exceeds 79 characters." for i, line in enumerate(code.split('\n')) if len(line) > 79]

	def _check_multiple_blank_lines(self, code: str) -> List[str]:
		return ["Multiple blank lines found."] if re.search(r"\n\s*\n\s*\n", code) else []

	def _check_spaces_before_punctuations(self, code: str) -> List[str]:
		return [f"Space found before punctuation on line {i + 1}." for i, line in enumerate(code.split('\n')) if
				re.search(r"\s[,;:]", line)]

	def _check_naming_convention(self, code: str) -> List[str]:
		issues = []
		# Check variable and function names
		for match in re.finditer(r"def (\w+)|(\w+) =", code):
			name = match.group(1) or match.group(2)
			if not re.match(r"^[a-z_][a-z0-9_]*$", name):
				issues.append(f"Invalid function or variable name '{name}'.")

		# Check class names
		for match in re.finditer(r"class (\w+)", code):
			name = match.group(1)
			if not re.match(r"^[A-Z][a-zA-Z0-9]*$", name):
				issues.append(f"Invalid class name '{name}'.")
		return issues

	def _check_indentation(self, code: str) -> List[str]:
		return ["Inconsistent indentation found."] if re.search(r"^(    |\t)", code, re.MULTILINE) else []

	def _check_import_order_and_format(self, code: str) -> List[str]:
		issues = []
		imports = re.findall(r"^import (\w+)", code, re.MULTILINE)
		if imports != sorted(imports):
			issues.append("Imports are not in alphabetical order.")
		if re.search(r"^from .+ import \*", code, re.MULTILINE):
			issues.append("Wildcard import found.")
		return issues

	def _check_trailing_whitespace(self, code: str) -> List[str]:
		return [f"Trailing whitespace found on line {i + 1}." for i, line in enumerate(code.split('\n')) if
				line.endswith(' ')]

	def _check_space_around_operators(self, code: str) -> List[str]:
		return [f"Missing space around operator on line {i + 1}." for i, line in enumerate(code.split('\n')) if
				re.search(r"=\w|==\w|\+\w|-\w|\*\w|/\w", line)]

	def grade(self, problems: List[ProblemDefinition], solutions: List[LLMSolution]) -> GradingOutput:
		solutionGrades = []
		for problem in problems:
			for solution in solutions:
				if solution.problem_identifier == problem.identifier:
					issues = []
					issues.extend(self._check_line_length(solution.solution_code))
					issues.extend(self._check_multiple_blank_lines(solution.solution_code))
					issues.extend(self._check_spaces_before_punctuations(solution.solution_code))
					issues.extend(self._check_naming_convention(solution.solution_code))
					issues.extend(self._check_indentation(solution.solution_code))
					issues.extend(self._check_import_order_and_format(solution.solution_code))
					issues.extend(self._check_trailing_whitespace(solution.solution_code))
					issues.extend(self._check_space_around_operators(solution.solution_code))

					score = 1 - len(issues) * 0.1  # Deduct 0.1 for each issue found
					score = max(score, 0)  # Ensure score doesn't go below 0

					grade = SolutionGrade(problem.identifier, solution.prompt_identifier, solution.model_identifier,
										  score, None, issues)
					solutionGrades.append(grade)
		return GradingOutput(solutionGrades, self.identifier)
