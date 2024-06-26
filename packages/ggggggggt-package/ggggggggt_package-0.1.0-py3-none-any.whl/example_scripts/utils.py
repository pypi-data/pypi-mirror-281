import json
import os

def get_env_json():
    current_script_path = os.path.abspath(__file__)
    base_dir = os.path.abspath(
        os.path.join(current_script_path, '..', '..', '..')
    )
    env_file = os.path.join(base_dir, 'gemnify-sdk-python', 'env.json')
    print(env_file)
    return json.load(
        open(
            env_file
        )
    )
