from llm_types import *
import json

with open("sample/problem.json", 'r') as f:
	problem = f.read()
print(problem)
problemDefinition = ProblemDefinition.from_json(json.loads(problem))
print(problemDefinition)

with open("sample/solution.json", 'r') as f:
	solution = f.read()
print(solution)
solution = LLMSolution.from_json(json.loads(solution))
print(solution)

with open("sample/grade.json", 'r') as f:
	grade = f.read()
print(grade)
gradingOutput = GradingOutput.from_json(json.loads(grade))
print(gradingOutput)