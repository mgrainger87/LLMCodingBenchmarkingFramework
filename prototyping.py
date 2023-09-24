from llm_types import *
import json
import grader

if __name__ == "__main__":	
	with open("sample/problem.json", 'r') as f:
		problem = f.read()
	# print(problem)
	problemDefinition = ProblemDefinition.from_json(json.loads(problem))
	print(problemDefinition)
	
	solutions = []
	
	inputs = problemDefinition.get_llm_problem_inputs()
	# print(f"Number of inputs: {len(inputs)}")
	
	for problemInput in inputs:
		# print(f"Generating solution for {problemInput}")
		solutions.append(HumanAIModel().generate_solution(problemInput))
		
	print(grader.CorrectnessGrader().grade([problemDefinition], solutions))
	print("Done")
