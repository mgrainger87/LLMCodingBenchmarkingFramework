from llm_types import *
import os

def get_problems(basePath: str):
	problems = []
	problemsDirectory = os.path.join(basePath, "problems")
	for problem_file in os.listdir(problemsDirectory):
		problemPath = os.path.join(problemsDirectory, problem_file)
		with open(problemPath) as f:
			problemJSON = f.read()
		problems.append(ProblemDefinition.from_json(problemJSON))
	return problems		

def save_solutions(basePath: str, solutions: List[LLMSolution]):
	for solution in solutions:
		path = os.path.join(basePath, "solutions", solution.model_identifier, solution.problem_identifier, solution.prompt_identifier + ".py")
		
		print(path)
		with open(path, 'w') as f:
			f.write(solution.to_json())
	
	
def save_grades(basePath: str, grades: List[GradingOutput]):
	pass