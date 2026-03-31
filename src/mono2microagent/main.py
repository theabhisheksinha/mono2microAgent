import os
from mono2microagent.crew import ArchaionCrew

def run():
    # 1. Simulated inputs based on your UI "DNA Badge"
    inputs = {
        'selected_app': 'nopCommerce', 
        'tech_stack': '.net ado.net asp.net mvc html javascript jquery redis sql web',
        'loc': '420,313',
        'is_mainframe': 'False',
        'target_cloud': 'AWS' # Options: AWS, Azure, GCP, IBM Cloud, Oracle Cloud
    }

    # 2. Dynamic file naming logic
    test_folder = "tests"
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)
    
    filename = f"{inputs['selected_app']}_refactoring_blueprint.md"
    output_path = os.path.join(test_folder, filename)

    print(f"## Kicking off Archaion Analysis for {inputs['selected_app']} ##")
    print(f"## Output will be saved to: {output_path} ##")

    # 3. Execution
    os.environ["ARCHAION_OUTPUT_FILE"] = output_path
    ArchaionCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()
