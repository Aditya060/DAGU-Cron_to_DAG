import os
import subprocess
import click
import yaml
import sys
import re


# Crontab expression validator regex
crontab_regex = re.compile(r'(@(annually|yearly|monthly|weekly|daily|hourly|reboot))|(@every (\d+(ns|us|µs|ms|s|m|h))+)|((((\d+,)+\d+|(\d+(\/|-)\d+)|\d+|\*) ?){5,7})')

def is_valid_crontab(expression):
    return bool(crontab_regex.fullmatch(expression))


def split_cron_expression(cron_expression):
    # Split the string at the first 5 spaces
    
    if (cron_expression[0] >= '0' and cron_expression[0] <= '9') or cron_expression[0] == '*':
        parts = cron_expression.split(' ', 5)
        # The schedule is the first 5 parts joined by space
        schedule = ' '.join(parts[:5])
        # The command is the remaining part
        command = parts[5]
    else:
        schedule, command = cron_expression.split(' ',1)
    
    return schedule, command




@click.group("dagu-cron")
# @click.version_option(version=__version__)
@click.pass_context
def cli(*args, **kwargs):
    # A tool to convert CRONTAB jobs to DAGU DAGs
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
        print (cron_expression)
        # schedule = cron_expression[0:10]
        # command = cron_expression[10:]
        schedule, command = split_cron_expression(cron_expression)
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


@cli.command("add_step")
@click.option("-o", "--output-dir", help="Output path for DAGs")
@click.option("-dag", "--dag-name", help="Name of the DAG to be modified")
@click.option("-step", "--step-name", help="Name of the step to be added")
@click.option("-schedule", "--step-schedule", help="Schedule for the new step")
@click.option("-command", "--step-command", help="Command for the new step")
@click.option("-dependencies", "--step-dependencies", help="Dependicies for the new step")
@click.pass_context
def add_basic_step(*args, **kwargs):

    dag_name = kwargs['dag_name']
    output_dir = kwargs['output_dir']
    step_schedule = kwargs['step_schedule']
    step_name = kwargs['step_name']
    step_command = kwargs['step_command']
    step_dependencies = kwargs['step_dependencies']
    
    new_step = {
            # 'schedule': step_schedule,
            'name': step_name,
            'command': step_command,
            'depends': step_dependencies.split(',') if step_dependencies else []
            

        }
    # print(new_step)

    file_path = os.path.join(output_dir, dag_name)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        # If there are no steps, initialize the steps list
        if 'steps' not in data:
            data['steps'] = []
    else:
         data = {
            'schedule': step_schedule,
            'steps': []
        }
         raise click.UsageError("You have provided an invalid DAG path")
    
    data['steps'].append(new_step)
    

    with open(file_path, 'w') as file:
            yaml.dump(data, file)
    print(f"Step added to  '{dag_name}' at '{output_dir}'")

# def add_basic_step(dag_name, step_schedule, step_name, step_command, step_dependencies):
#     # output_dir = 
#     data = {
#             'schedule': step_schedule,
#             'steps': 
#             [
#                 {
#                     'name': step_name,
#                     'command': step_command,
#                     'depends': {iterable for iterable in step_dependencies}
                    
                    
#                 }
#             ]

#         }
#     print(data)
#     file_path = os.path.join(output_dir, dag_name)
#     with open(file_path, 'w') as file:
#             yaml.dump(data, file)
#     print(f"Step added to  '{dag_name}' at '{output_dir}'")

    
