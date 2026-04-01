import os
from mono2microagent.crew import ArchaionCrew

def run():
    # 1. Test Inputs mirroring your UI selection
    inputs = {
        'selected_app': 'WebGoat_v3', 
        'tech_stack': 'ansi sql java java server pages java servlet java soap javascript jdbc jee python sql ',
        'loc': '40,313',
        'is_mainframe': 'False',
        'target_cloud': 'AWS' 
    }

    # 2. Dynamic File Path Logic (test/AppName_modernization_blueprint.md)
    test_folder = "test"
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)
    
    filename = f"{inputs['selected_app']}_modernization_blueprint.md"
    output_path = os.path.join(test_folder, filename)

    print(f"## Generating Professional Archaion Report for: {inputs['selected_app']} ##")

    os.environ["ARCHAION_OUTPUT_FILE"] = output_path
    ArchaionCrew().crew().kickoff(inputs=inputs)
    print(f"Report saved to: {output_path}")

if __name__ == "__main__":
    run()
