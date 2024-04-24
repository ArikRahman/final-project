from flask import Flask, request, render_template_string
import subprocess
import shlex

app = Flask(__name__)

# HTML template for the input form with added CSS
input_form_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Command Executor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 40px;
        }
        form {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        label {
            display: block;
            margin-bottom: 10px;
        }
        input[type="text"], select {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        input[type="submit"] {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <form action="/execute" method="post">
        <label for="command">Say Howdy to your new best friend!:</label>
        <input type="text" id="command" name="command" required>
        
        <!-- Dropdown for selecting the file -->
        <label for="fileChoice">Choose a personality:</label>
        <select name="fileChoice" id="fileChoice">
            <option value="fire.txt">Blaze</option>
            <option value="water.txt">Mirana</option>
            <option value="grass.txt">Verdant</option>
        </select>
        
        <input type="submit" value="Execute">
    </form>
</body>
</html>
'''


# HTML template for displaying the command output with added CSS
output_display_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 40px;
        }
        pre {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        a {
            display: inline-block;
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            margin-top: 20px;
            border-radius: 5px;
            text-decoration: none;
        }
        a:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <p>Answer:</p>
    <pre>{{ output }}</pre>
    <a href="/">Back to form</a>
      
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(input_form_html)

@app.route('/execute', methods=['POST'])
@app.route('/execute', methods=['POST'])
def execute_command():
    command = request.form['command']
    file_choice = request.form['fileChoice']  # Retrieve the selected file from the form

    # Basic command validation to only allow "safe" commands for demonstration
    if "rm" in command or "&&" in command or ";" in command:
        return "Unsafe command detected!", 400

    try:
        # Adjust the command string to use the selected file
        command_string = f'sgpt "{command}" < {file_choice}'  # Use the selected file
        
        # Execute the command using the shell
        output = subprocess.check_output(command_string, shell=True, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = f"Error executing command: {e.output}"

    return render_template_string(output_display_html, command=command, output=output)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

