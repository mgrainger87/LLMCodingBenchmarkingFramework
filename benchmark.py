import argparse
from base_types import *
import json
import grader
import serialization
import querier
import sys
import os
import validation

def load_problems(base_path):
	return serialization.get_problems(base_path)

def validate_problems(base_path):
	validation_results = {}
	
	problemsJSON = serialization.get_problems_json(base_path)
	
	for fileName, json in problemsJSON.items():
		validation_results[fileName] = validation.validate_problem_json(json)
	return validation_results

def generate_solutions(base_path, problem_definitions, models):
	solutions = []	
	for model in models:
		for problem_definition in problem_definitions:
			inputs = problem_definition.get_llm_problem_inputs()
			for problem_input in inputs:
				solutions.append(model.generate_solution(problem_input))
	serialization.save_solutions(base_path, solutions)
	return solutions
	
def load_solutions(base_path, models):
	solutions = []
	for model in models:
		solutions += serialization.load_solutions(base_path, model.model_identifier)
	return solutions

def grade_solutions(base_path, problem_definitions, models, graders):
	gradingOutputs = []
	for grader in graders:
		if not grader.can_grade(problem_definitions):
			continue
		for model in models:
			solutions = serialization.get_solutions(base_path, model.model_identifier)
			grades = grader.grade(problem_definitions, solutions)
			serialization.save_grades(base_path, grades)
			gradingOutputs.append(grades)
	print(gradingOutputs)
	return gradingOutputs
	
def load_grades(base_path, models, graders):
	gradingOutputs = []
	for grader in graders:
		for model in models:
			gradingOutputs.append(serialization.get_grades(base_path, model.model_identifier, grader.identifier))

	return gradingOutputs	

def main():
	parser = argparse.ArgumentParser(description="Run specified phases of the grading process.")
	parser.add_argument('--base_path', nargs='*', default=None, help="The base path(s) for data files. If this arg is not set, run all problem sets in ./problem_sets")
	parser.add_argument('--validate', action='store_true', help="Validate the problem definition JSON.")
	parser.add_argument('--generate', action='store_true', help="Generate solutions for problems.")
	parser.add_argument('--grade', action='store_true', help="Grade the generated solutions.")
	parser.add_argument('--model', required='--generate' in sys.argv or '--grade' in sys.argv, nargs='+', help="The model(s) to use for generating solutions.")
	parser.add_argument('--grader', required='--grade' in sys.argv, nargs='+', help="The grader(s) to use for grading solutions.")
	parser.add_argument('--force-human', action='store_true', help="Always use the interactive human model querier.")
	args = parser.parse_args()

	problem_definitions = []
	
	if args.model:
		models = querier.AIModelQuerier.resolve_queriers(args.model, args.force_human)
	if args.grader:
		graders = grader.Grader.resolve_graders(args.grader)
	
	if args.base_path is None:
		args.base_path = [os.path.join('problem_sets', d) for d in os.listdir('problem_sets') if os.path.isdir(os.path.join('problem_sets', d))]
		
	if args.validate:
		print("Validating problems…")
		all_validation_results = {x: validate_problems(x) for x in args.base_path}
		print("Validation results:")
		for base_path, validation_results in all_validation_results.items():
			print(f"{base_path}:")
			for fileName, validation_result in validation_results.items():
				print(f"\t{fileName}: {validation_result}")
	
	if args.generate or args.grade:
		print("Loading problems…")
		problem_sets = [load_problems(x) for x in args.base_path]
	
		# Run benchmarks on all problem sets sequentially
		for problem_definitions in problem_sets:
			for problem_definition in problem_definitions:
				print(problem_definition)
				print()
				
			if args.generate:
				print("Generating solutions…")
				solutions = generate_solutions(args.base_path, problem_definitions, models)
				print(solutions)
			
			if args.grade:
				print("Grading solutions…")
				grading_outputs = grade_solutions(args.base_path, problem_definitions, models, graders)
	
				for output in grading_outputs:
					print(output.str_including_solutions())
	
				print()
	
				for output in grading_outputs:
					print(output)
	
	print("Done")

if __name__ == "__main__":
	main()
