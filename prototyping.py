import argparse
from llm_types import *
import json
import grader
import serialization
import querier
import sys

def load_problems(base_path):
	return serialization.get_problems(base_path)

def generate_solutions(base_path, problem_definitions, models):
	for model in models:
		solutions = []
		for problem_definition in problem_definitions:
			inputs = problem_definition.get_llm_problem_inputs()
			for problem_input in inputs:
				solutions.append(model.generate_solution(problem_input))
		serialization.save_solutions(base_path, solutions)

def grade_solutions(base_path, problem_definitions, graders):
	for grader in graders:
		solutions = serialization.get_solutions(base_path, "human")
		grades = grader.grade(problem_definitions, solutions)
		serialization.save_grades(base_path, grades)
		print(grades)
	
def resolve_graders(grader_names):
	resolvedGraders = []
	for grader_name in grader_names:
		if grader_name == "correctness":
			resolvedGraders.append(grader.CorrectnessGrader())
			
	if len(resolvedGraders) == 0:
		resolvedGraders.append("correctness")
		
	return resolvedGraders

def main():
	parser = argparse.ArgumentParser(description="Run specified phases of the grading process.")
	parser.add_argument('--base_path', required=True, help="The base path for data files.")
	parser.add_argument('--load', action='store_true', help="Load problems from disk.")
	parser.add_argument('--generate', action='store_true', help="Generate solutions for problems.")
	parser.add_argument('--grade', action='store_true', help="Grade the generated solutions.")
	parser.add_argument('--model', required=True, nargs='+', help="The model(s) to use for generating solutions.")
	parser.add_argument('--grader', required=True, nargs='+', help="The grader(s) to use for grading solutions.")
	args = parser.parse_args()
	
	problem_definitions = []
	
	models = querier.AIModelQuerier.resolve_model_names(args.model)
	graders = resolve_graders(args.grader)
	
	if args.load:
		problem_definitions = load_problems(args.base_path)
		print(problem_definitions)
	
	if args.generate:
		if not problem_definitions:
			problem_definitions = load_problems(args.base_path)
		generate_solutions(args.base_path, problem_definitions, models)
		print()
	
	if args.grade:
		if not problem_definitions:
			problem_definitions = load_problems(args.base_path)
		grade_solutions(args.base_path, problem_definitions, graders)
	
	print("Done")

if __name__ == "__main__":
	main()
