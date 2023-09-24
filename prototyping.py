from llm_types import *
import json
import grader
import serialization
import models
import sys

if __name__ == "__main__":	
	# Check if the user has provided a command-line argument
	if len(sys.argv) < 2:
		print("Please provide correct arguments.")
		sys.exit(1)
		
	base_path = sys.argv[1]

	problemDefinitions = serialization.get_problems(base_path)
		
	solutions = []
	
	for problemDefinition in problemDefinitions:
		inputs = problemDefinition.get_llm_problem_inputs()
	# print(f"Number of inputs: {len(inputs)}")
	
		for problemInput in inputs:
			# print(f"Generating solution for {problemInput}")
			solutions.append(models.HumanAIModel().generate_solution(problemInput))
		
	print(grader.CorrectnessGrader().grade([problemDefinition], solutions))
	print("Done")
	
	serialization.save_solutions(base_path, solutions)
