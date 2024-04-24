from flask import Flask, request, render_template_string, session
import subprocess
import shlex

app = Flask(__name__)
app.secret_key = 'your_secure_key'
global total
commands_by_ip = {}

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
            <option value="fire.txt">Charmander</option>
            <option value="water.txt">Squirtle</option>
            <option value="grass.txt">Bulbosaur</option>
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
        button, a {
            display: inline-block;
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            margin-top: 20px;
            border-radius: 5px;
            text-decoration: none;
            border: none;
            cursor: pointer;
        }
        button:hover, a:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <p>Answer:</p>
    <pre>{{ output }}</pre>
    <button onclick="window.location.href='/'">Ask Another Question</button>
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
    source_ip = request.remote_addr  # Get the source IP address of the client

    # Log the received input and source IP
    print(f"Command received: {command} from IP: {source_ip}")
    
    # Basic command validation to only allow "safe" commands for demonstration
    if "rm" in command or "&&" in command or ";" in command:
        return "Unsafe command detected!", 400

    try:
        print("Checking contents of commands_by_ip:", commands_by_ip)
        if source_ip not in commands_by_ip:
            commands_by_ip[source_ip] = []

        print("Current command:", command)
        print("Commands by IP:", commands_by_ip[source_ip])

        total = command + str(commands_by_ip[source_ip])
        print("Total after concatenation:", total)
        # Adjust the command string to use the selected file
        command_string = f'sgpt "{total}" < {file_choice}'  # Use the selected file
        
        # Execute the command using the shell
        output = subprocess.check_output(command_string, shell=True, text=True, stderr=subprocess.STDOUT)
        print(output)
        if source_ip not in commands_by_ip:
            commands_by_ip[source_ip] = []
        commands_by_ip[source_ip].append((command, output))
        print(commands_by_ip[source_ip])
    except subprocess.CalledProcessError as e:
        output = f"Error executing command: {e.output}"

    return render_template_string(output_display_html, command=command, output=output)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

