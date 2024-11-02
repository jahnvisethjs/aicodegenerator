import subprocess
import sys
import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key='AIzaSyDpOlV5esrV6Myijkgo65VNt_r5Rvnw-_4')

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

def generate_code(prompt):
  structured_prompt = f"""
    Generate Python code for: {prompt}
    Requirements:
    - Code must be complete and runnable
    - Include input validation if needed
    - Include code to take input from user
    - Use proper indentation
    - No syntax errors
    - For patterns/pyramids, use nested loops
    - Provide only the code, no explanations
    - No markdown formatting
    """
  response = model.generate_content(structured_prompt)
  return response.text

def generate_input(code):
  prompt=f"""
    Generate input for the following code if needed: {code}. No explanations needed
  """
  response= model.generate_content(prompt)
  return response.text

def validate_code(code, inp):
  prompt=f"""
    Test the following code: {code}
    against this input: {inp} and fix the errors in code if execution not successful.
    If the code execution is successful, return true else return the error that occured, no other explanation required
  """

  response=model.generate_content(prompt)
  decision=response.text

  if decision=='true':
    return True
  else:
    return decision

def main():
  prompt=input("Enter the python code prompt: ")

  code=generate_code(prompt)
  print("Initial code: \n", code)

  test_input= generate_input(code)
  print('Validating code against the following input: \n', test_input)

  if validate_code(code, test_input):
    print("code validation successful")
  else:
    print("try again")



if __name__ == "__main__":
  main()