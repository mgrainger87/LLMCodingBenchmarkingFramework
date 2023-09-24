from base_types import *
import os
import pathlib

def get_problems(basePath: str):
	problems = []
	problemsDirectory = os.path.join(basePath, "problems")
	for problem_file in [file for file in sorted(os.listdir(problemsDirectory)) if not file.startswith('.')]:
		problemPath = os.path.join(problemsDirectory, problem_file)
		# print(problemPath)
		with open(problemPath) as f:
			problemJSON = json.loads(f.read())
		problems.append(ProblemDefinition.from_json(problemJSON))
	return problems		

def save_solutions(basePath: str, solutions: List[LLMSolution]):
	for solution in solutions:
		directoryPath = os.path.join(basePath, "solutions", solution.model_identifier, solution.problem_identifier)
		pathlib.Path(directoryPath).mkdir(parents=True, exist_ok=True)
		path = os.path.join(directoryPath, solution.prompt_identifier + ".json")
		
		# print(path)
		with open(path, 'w') as f:
			jsonString = json.dumps(solution.to_json(), indent=4)
			f.write(jsonString)

def get_solutions(basePath: str, model_identifier: str):
	solutions = []
	solutionsDirectory = os.path.join(basePath, "solutions", model_identifier)

	for problemName in [file for file in sorted(os.listdir(solutionsDirectory)) if not file.startswith('.')]:
		problemDirectory = os.path.join(solutionsDirectory, problemName)

		for solution_file in [file for file in sorted(os.listdir(problemDirectory)) if not file.startswith('.')]:
			solutionPath = os.path.join(problemDirectory, solution_file)
			# print(solutionPath)
			with open(solutionPath) as f:
				solutionJSON = json.loads(f.read())
			solutions.append(LLMSolution.from_json(solutionJSON))
	return solutions		
	
def save_grades(basePath: str, grades: GradingOutput):
	# print(grades.solution_grades)
	for solutionGrade in grades.solution_grades:
		directoryPath = os.path.join(basePath, "grades", solutionGrade.model_identifier, grades.grader_identifier, solutionGrade.problem_identifier)
		pathlib.Path(directoryPath).mkdir(parents=True, exist_ok=True)
		path = os.path.join(directoryPath, solutionGrade.prompt_identifier + ".json")

		# print(path)
		with open(path, 'w') as f:
			jsonString = json.dumps(solutionGrade.to_json(), indent=4)
			f.write(jsonString)
			
def get_grades(basePath: str, model_identifier: str, grader_identifier: str):
	grades = []
	gradesDirectory = os.path.join(basePath, "grades", model_identifier, grader_identifier)
	
	for problemName in [file for file in sorted(os.listdir(gradesDirectory)) if not file.startswith('.')]:
		problemDirectory = os.path.join(gradesDirectory, problemName)
	
		for grade_file in [file for file in sorted(os.listdir(problemDirectory)) if not file.startswith('.')]:
			gradePath = os.path.join(problemDirectory, grade_file)
			# print(gradePath)
			with open(gradePath) as f:
				gradeJSON = json.loads(f.read())
			grades.append(SolutionGrade.from_json(gradeJSON))
	return GradingOutput(grades, grader_identifier)		
