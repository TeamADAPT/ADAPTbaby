# ... (previous imports and setup)

import ast

def generate_function(prompt):
    # Use Groq to generate a Python function based on the prompt
    function_prompt = f"Generate a Python function that does the following: {prompt}"
    function_code = test_groq_model(function_prompt)
    
    # Extract the function definition from the generated code
    try:
        tree = ast.parse(function_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                function_body = ast.unparse(node)
                return function_name, function_body
    except SyntaxError:
        return None, None

def execute_generated_function(function_body, *args, **kwargs):
    # Execute the generated function
    try:
        exec(function_body, globals())
        function_name = function_body.split("def ")[1].split("(")[0]
        return eval(f"{function_name}(*args, **kwargs)")
    except Exception as e:
        return f"Error executing function: {str(e)}"

@app.route('/self_build', methods=['POST'])
@login_required
def self_build():
    data = request.json
    prompt = data.get('prompt', "")
    
    function_name, function_body = generate_function(prompt)
    
    if function_name and function_body:
        result = execute_generated_function(function_body)
        return jsonify({
            "status": "success",
            "function_name": function_name,
            "function_body": function_body,
            "result": result
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Failed to generate a valid function"
        })

# ... (rest of the file)
