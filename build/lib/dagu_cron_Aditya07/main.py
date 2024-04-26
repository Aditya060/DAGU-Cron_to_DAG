import os
import subprocess
import click
import yaml
import sys

@click.group("dagu-cron")
# @click.version_option(version=__version__)
@click.pass_context
def cli(*args, **kwargs):
    """A tool to convert CRONTAB jobs to DAGU DAGs"""
    pass

@cli.command("build")
@click.option("-o", "--output-dir", help="Output path for DAGs")
@click.pass_context
def build(*args, **kwargs):
    """Convert crontab file to DAGs."""
    output_dir = kwargs["output_dir"] if kwargs["output_dir"] is not None else os.getcwd()
    if kwargs["output_dir"] is None:
        raise click.UsageError("Output Directory not provided. DAGs will be created in the current directory.")


# Command to read the crontab file
    command = "crontab -l"

    # Execute the command and capture the output
    output = subprocess.run(command, shell=True, capture_output=True, text=True)
    crontab_list = output.stdout

    # Check if the command was successful
    if output.returncode == 0:
        # Print the contents of the crontab file
        print("Crontab contents:")
        print(output.stdout)
    else:
        # Print an error message if the command failed
        print("Error:", output.stderr)
        sys.exit(1)
        
        # return

        
    # Create a list of cron tab entries
    cron_job_list = output.stdout.split('\n')
    print(cron_job_list)
        
    # Extract the schedule parameters from the crontab entry
    for i in range (0,len(cron_job_list)):
        cron_expression = cron_job_list[i]
        schedule = cron_expression[0:10]
        command = cron_expression[10:]
        cronjob_name = 'Task_{}'.format(i)
        print(command)
        
        data = {
            'schedule': schedule,
            'steps': 
            [
                {
                    'name': cronjob_name,
                    'command': command
                }
            ]

        }
        file_name = f"{cronjob_name}.yaml"
        file_path = os.path.join(output_dir, file_name)
    

        with open(file_path, 'w') as file:
            yaml.dump(data, file)
        print(f"YAML file '{file_name}' created at '{output_dir}'")

    
