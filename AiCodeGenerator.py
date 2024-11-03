import subprocess
import sys
import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key="API_KEY")

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

def generate_test_cases(prompt):
    structured_prompt = f"""
    This {prompt} would be used to generate a python code. Write test cases which can be used to validate if generated python code meets user requirements or not.
    Requirements:
    - Test cases should test both run time errors as well as higher order user requirements itself. If a user requirement is not met then that should result in failed test
    - Pay especial attention to edge cases to generate test cases
    - Provide only the test cases, no explanations unless specifically asked for it
    - Test cases should be such that it can be programtically fed into a python code
    - No markdown formatting
    """
    response = model.generate_content(structured_prompt)
    return response.text


def validate_code(code, testCase):
    max_attempts = 5
    attempt = 1
    
    while attempt <= max_attempts:
        print(f"\nAttempt {attempt} of {max_attempts}")
        
        prompt = f"""
        Test the following code: {code}
        against this test case with given input and expected output : {testCase} and fix the errors in code if execution not successful.
        The actual output of code written by you should match the expected output.
        If the code execution is successful, return 'true' else return both:
        1. The error that occurred
        2. The fixed code
        3. mandatory to show test case input, expected output and actual output
        Format: If error exists, return 'ERROR: <error_message>\nFIXED_CODE: <fixed_code>'
        If no error, just return 'true'
        """

        response = model.generate_content(prompt)
        result = response.text.strip()
        
        if result.lower() == 'true':
            return True, code
            
        if 'ERROR:' in result and 'FIXED_CODE:' in result:
            try:
                error_msg = result.split('FIXED_CODE:')[0].replace('ERROR:', '').strip()
                fixed_code = result.split('FIXED_CODE:')[1].strip()
                
                print(f"Error found: {error_msg}")
                print(f"Attempting fix...")
                
                if fixed_code == code:
                    print("No improvement in code. Trying again...")
                else:
                    code = fixed_code
                    print("New code version generated:")
                    print(code)
            except Exception as e:
                print(f"Error parsing response: {e}")
        
        attempt += 1
    
    return False, code

def main():
  prompt=input("Enter the python code prompt: ")

  code=generate_code(prompt)
  print("Initial code: \n", code)

  test_input= generate_test_cases(code)
  print('Validating code against the following input: \n', test_input)

  if validate_code(code, test_input):
    print("code validation successful")
  else:
    print("try again")



if __name__ == "__main__":
  main()
