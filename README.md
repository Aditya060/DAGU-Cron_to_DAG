# Published to pypi 
https://pypi.org/project/dagu-cron/

# Dagu-cron

Dagu-cron is a versatile Python package and command-line tool designed to facilitate the conversion of CRONTAB jobs into DAGU DAGs, enabling efficient management of complex workflows within a controlled application environment.

## Features

- **CRONTAB to DAGU Conversion**: Automatically convert CRONTAB entries to DAGU DAGs, streamlining the management and visualization of intricate workflows.
  
- **Workflow Management**:
  - **Add Steps**: Seamlessly integrate new steps into existing DAGs.
  - **Transfer Steps**: Move steps between DAGs to reorganize workflows.
  - **Remove Steps**: Simplify DAGs by removing unnecessary steps.
  
- **CLI and Library Integration**:
  - **Command-Line Interface**: Execute commands to perform CRONTAB conversion, step addition, transfer, and removal.
  - **Library Functions**: Import directly into projects for deeper integration and customized workflow management.
  
- **Secure Application Environment**: Control and manage DAG operations exclusively through the application interface, ensuring security by restricting access to the DAGU UI and server.

## Usage

### Command-Line Interface

Execute commands to perform tasks:

```bash
# Convert CRONTAB to DAGU DAGs
$ dagu-cron build -o /path/to/output/dags

# Add a step to an existing DAG
$ dagu-cron add_step -o /path/to/output/dags -dag dag_name -step step_name -schedule "*/5 * * * *" -command "python script.py" -dependencies "dependency1,dependency2"

# Transfer a step from one DAG to another
$ dagu-cron transfer_step -o /path/to/output/dags -source source_dag.yaml -dest dest_dag.yaml -step step_name

# Remove a step from a DAG
$ dagu-cron remove_step -o /path/to/output/dags -dag dag_name -step step_name
```

Library Integration
Import functions for programmatic control:

```bash
from dagu_cron.lib import add_step_to_dag, build_dag_from_crontab

# Example usage in Python code

output_dir = '/path/to/output/dags'
dag_name = 'my_dag.yaml'
step_name = 'step1'
step_schedule = '*/5 * * * *'
step_command = 'python script.py'
step_dependencies = 'dependency1,dependency2'

add_step_core(output_dir, dag_name, step_name, step_schedule, step_command, step_dependencies)

build_core(output_dir)
```

By offering both a versatile CLI and seamless library integration, dagu-cron empowers developers to manage workflows effectively and securely, whether through direct commands or integrated functions within their projects.
