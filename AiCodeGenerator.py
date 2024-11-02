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
    max_attempts = 5
    attempt = 1
    
    while attempt <= max_attempts:
        print(f"\nAttempt {attempt} of {max_attempts}")
        
        prompt = f"""
        Test the following code: {code}
        against this input: {inp} and fix the errors in code if execution not successful.
        If the code execution is successful, return 'true' else return both:
        1. The error that occurred
        2. The fixed code
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

  test_input= generate_input(code)
  print('Validating code against the following input: \n', test_input)

  if validate_code(code, test_input):
    print("code validation successful")
  else:
    print("try again")



if __name__ == "__main__":
  main()