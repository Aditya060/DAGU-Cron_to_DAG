import os
import subprocess
import click
import yaml
import sys
import re

# Crontab expression validator regex
crontab_regex = re.compile(r'(@(annually|yearly|monthly|weekly|daily|hourly|reboot))|(@every (\d+(ns|us|µs|ms|s|m|h))+)|((((\d+,)+\d+|(\d+(\/|-)\d+)|\d+|\*) ?){5,7})')

def is_valid_crontab(expression): 
    """Validate a crontab expression."""
    return bool(crontab_regex.fullmatch(expression))

def split_cron_expression(cron_expression):
    """
    Split a crontab expression into schedule and command.
    
    Args:
        cron_expression (str): The crontab expression to split.
    
    Returns:
        tuple: A tuple containing the schedule and command.
    """
    if (cron_expression[0].isdigit()) or cron_expression[0] == '*':
        parts = cron_expression.split(' ', 5)
        schedule = ' '.join(parts[:5])
        command = parts[5]
    else:
        schedule, command = cron_expression.split(' ', 1)
    
    return schedule, command

@click.group("dagu-cron")
@click.pass_context
def cli(ctx):
    """A tool to convert CRONTAB jobs to DAGU DAGs."""
    pass

###################################### Build from crontab ######################################

def build_core(output_dir):
    """Core logic to build DAGs from crontab."""
    if output_dir is None:
        output_dir = os.getcwd()

    # Command to read the crontab file
    command = "crontab -l"

    # Execute the command and capture the output
    output = subprocess.run(command, shell=True, capture_output=True, text=True)
    crontab_list = output.stdout

    # Check if the command was successful
    if output.returncode == 0:
        print("Crontab contents:")
        print(output.stdout)
    else:
        print("Error:", output.stderr)
        sys.exit(1)

    # Create a list of crontab entries
    cron_job_list = crontab_list.split('\n')
    print(cron_job_list)

    # Extract the schedule parameters from the crontab entry
    for i, cron_expression in enumerate(cron_job_list):
        if cron_expression.strip():  # Ignore empty lines
            schedule, command = split_cron_expression(cron_expression)
            cronjob_name = f'Task_{i}'
            print(command)

            data = {
                'schedule': schedule,
                'steps': [
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

@click.command("build")
@click.option("-o", "--output-dir", help="Output path for DAGs")
@click.pass_context
def build(ctx, output_dir):
    """Convert crontab file to DAGs."""
    try:
        build_core(output_dir)
    except click.UsageError as e:
        raise click.UsageError("Output Directory not provided. DAGs will be created in the current directory.")

cli.add_command(build)

###################################### Add step to existing DAG ######################################

def add_step_core(output_dir, dag_name, step_name, step_schedule, step_command, step_dependencies):
    """
    Core logic to add a step to an existing DAG.
    
    Args:
        output_dir (str): Output directory for DAGs.
        dag_name (str): Name of the DAG to be modified.
        step_name (str): Name of the step to be added.
        step_schedule (str): Schedule for the new step.
        step_command (str): Command for the new step.
        step_dependencies (str): Dependencies for the new step.
    """
    new_step = {
        'name': step_name,
        'command': step_command,
        'depends': step_dependencies.split(',') if step_dependencies else []
    }

    file_path = os.path.join(output_dir, dag_name)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
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
    print(f"Step added to '{dag_name}' at '{output_dir}'")

@click.command("add_step")
@click.option("-o", "--output-dir", help="Output path for DAGs")
@click.option("-dag", "--dag-name", help="Name of the DAG to be modified")
@click.option("-step", "--step-name", help="Name of the step to be added")
@click.option("-schedule", "--step-schedule", help="Schedule for the new step")
@click.option("-command", "--step-command", help="Command for the new step")
@click.option("-dependencies", "--step-dependencies", help="Dependencies for the new step")
@click.pass_context
def add_step(ctx, output_dir, dag_name, step_name, step_schedule, step_command, step_dependencies):
    add_step_core(output_dir, dag_name, step_name, step_schedule, step_command, step_dependencies)

cli.add_command(add_step)

###################################### Transfer step from one DAG to another ######################################

def transfer_step_core(output_dir, source_file, destination_file, step_name):
    """
    Core logic to transfer a step from one DAG to another.
    
    Args:
        output_dir (str): Output directory for DAGs.
        source_file (str): Source DAG file.
        destination_file (str): Destination DAG file.
        step_name (str): Name of the step to transfer.
    """
    source_path = os.path.join(output_dir, source_file)
    with open(source_path, 'r') as file:
        data = yaml.safe_load(file)

    if 'steps' in data and isinstance(data['steps'], list):
        step_to_transfer = None
        for step in data['steps']:
            if step.get('name') == step_name:
                step_to_transfer = step
                break
        print("This function is working")

        if step_to_transfer:
            data['steps'].remove(step_to_transfer)
            print("Extracted Step:", step_to_transfer)
            
            # Writing the modified data back to the source file
            with open(source_path, 'w') as file:
                yaml.safe_dump(data, file)
            print("Updated data written back to source file.")

            # Writing step to the destination file
            destination_path = os.path.join(output_dir, destination_file)
            with open(destination_path, 'r') as file:
                dest_data = yaml.safe_load(file)
            print(dest_data)

            dest_data['steps'].append(step_to_transfer)
            print(dest_data)

            with open(destination_path, 'w') as file:
                yaml.safe_dump(dest_data, file)

@click.command("transfer_step")
@click.option("-o", "--output-dir", help="Output path for DAGs")
@click.option("-source", "--source-file", help="Source DAG file")
@click.option("-dest", "--destination-file", help="Destination DAG file")
@click.option("-step", "--step-name", help="Name of the step to transfer")
@click.pass_context
def transfer_step(ctx, output_dir, source_file, destination_file, step_name):
    transfer_step_core(output_dir, source_file, destination_file, step_name)

cli.add_command(transfer_step)

###################################### Remove step from a DAG ######################################

def remove_step_core(output_dir,dag_name, step_name):
    source_path = os.path.join(output_dir, dag_name)
    with open(source_path, 'r') as file:
        data = yaml.safe_load(file)
    step_to_remove = None
    for step in data['steps']:
        dependencies = step.get('dependencies', [])
        if dependencies:
            for dependency in dependencies:
                if dependency == step_name:
                    print("Error. Step is a dependency in other steps. Cannot remove.")
                        # ßraise click.UsageError("Error. Step is a dependency in other steps. Cannot remove.")
                    return
    for step in data['steps']:
            if step.get('name') == step_name:
                step_to_remove = step
                break
                            
                        

        
    data['steps'].remove(step_to_remove)
    print("Removed Step:", step_name)
            
    # Writing the modified data back to the source file
    with open(source_path, 'w') as file:
        yaml.safe_dump(data, file)
        print("Updated data written back to source file.")
    

@click.command("remove_step")
@click.option("-o", "--output-dir", help = "Output path for DAGs")
@click.option("-dag", "--dag-name", help="Name of the DAG to be modified")
@click.option("-step", "--step-name", help="Name of the step to be removed")
@click.pass_context
def remove_step(ctx, output_dir, dag_name, step_name):
    remove_step_core(output_dir, dag_name, step_name)

cli.add_command(remove_step)

if __name__ == "__main__":
    cli()
