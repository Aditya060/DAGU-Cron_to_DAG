import subprocess
import click
import yaml

# Command to read the crontab file
command = "crontab -l"

# Execute the command and capture the output
output = subprocess.run(command, shell=True, capture_output=True, text=True)

# Check if the command was successful
if output.returncode == 0:
    # Print the contents of the crontab file
    print("Crontab contents:")
    print(output.stdout)
else:
    # Print an error message if the command failed
    print("Error:", output.stderr)
