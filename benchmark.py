import argparse
from base_types import *
import json
import grader
import serialization
import querier
import sys

def load_problems(base_path):
	return serialization.get_problems(base_path)

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
	parser.add_argument('--base_path', required=True, help="The base path for data files.")
	parser.add_argument('--generate', action='store_true', help="Generate solutions for problems.")
	parser.add_argument('--grade', action='store_true', help="Grade the generated solutions.")
	parser.add_argument('--model', required=True, nargs='+', help="The model(s) to use for generating solutions.")
	parser.add_argument('--grader', required='--grade' in sys.argv, nargs='+', help="The grader(s) to use for grading solutions.")
	parser.add_argument('--force-human', action='store_true', help="Always use the interactive human model querier.")
	args = parser.parse_args()
	
	problem_definitions = []
	
	models = querier.AIModelQuerier.resolve_queriers(args.model, args.force_human)
	graders = grader.Grader.resolve_graders(args.grader)
	
	print("Loading problems…")
	problem_definitions = load_problems(args.base_path)
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
