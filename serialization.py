from llm_types import *
import os
import pathlib

def get_problems(basePath: str):
	problems = []
	problemsDirectory = os.path.join(basePath, "problems")
	for problem_file in [file for file in os.listdir(problemsDirectory) if not file.startswith('.')]:
		problemPath = os.path.join(problemsDirectory, problem_file)
		print(problemPath)
		with open(problemPath) as f:
			problemJSON = json.loads(f.read())
		problems.append(ProblemDefinition.from_json(problemJSON))
	return problems		

def save_solutions(basePath: str, solutions: List[LLMSolution]):
	for solution in solutions:
		directoryPath = os.path.join(basePath, "solutions", solution.model_identifier, solution.problem_identifier)
		pathlib.Path(directoryPath).mkdir(parents=True, exist_ok=True)
		path = os.path.join(directoryPath, solution.prompt_identifier + ".json")
		
		print(path)
		with open(path, 'w') as f:
			jsonString = json.dumps(solution.to_json(), indent=4)
			f.write(jsonString)
	
	
def save_grades(basePath: str, grades: List[GradingOutput]):
	pass