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
	
	model = models.HumanAIModel()
	
	# for problemDefinition in problemDefinitions:
	# 	inputs = problemDefinition.get_llm_problem_inputs()
	# 
	# 	for problemInput in inputs:
	# 		solutions.append(model.generate_solution(problemInput))
	# 	
	# serialization.save_solutions(base_path, solutions)
	
# 	solutions = serialization.get_solutions(base_path, "human")
# 
# 	grades = grader.CorrectnessGrader().grade(problemDefinitions, solutions)

	grades = serialization.get_grades(base_path, "human")
	print(grades)
	serialization.save_grades(base_path, grades)
	print("Done")
	
