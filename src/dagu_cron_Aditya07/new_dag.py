import os


def add_basic_step(dag_name, step_schedule, step_name, step_command, step_dependencies):
    # output_dir = 
    data = {
            'schedule': step_schedule,
            'steps': 
            [
                {
                    'name': step_name,
                    'command': step_command,
                    'depends': {iterable for iterable in step_dependencies}
                    
                    
                }
            ]

        }
    print(data)
    file_path = os.path.join(output_dir, dag_name)
    with open(file_path, 'w') as file:
            yaml.dump(data, file)
        print(f"Step added to  '{dag_name}' at '{output_dir}'")
    
def add_custom_step(dag_name, data_dictionary):
      file_path = os.path.join(output_dir, dag_name)
      with open(file_path, 'w') as file:
            yaml.dump(data, file)
        print(f"Step added to  '{dag_name}' at '{output_dir}'")
      
      

