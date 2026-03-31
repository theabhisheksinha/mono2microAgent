import os
from mono2microagent.crew import ArchaionCrew

def run():
    # 1. Inputs mirror your "Archaion Analyzer" UI's radio button selection
    inputs = {
        'selected_app': 'LegacyStockManagement_COBOL', # Name from your UI
        'tech_stack': 'ibm cics tm, ibm cobol, ibm ims dc, jcl, java, sql', # Stack from UI
        'loc': '463,099', # LOC from UI
        'is_mainframe': 'Detected', # Status from UI
        'target_cloud': 'Azure' # Options: AWS, Azure, GCP, IBM Cloud, Oracle Cloud
    }

    # 2. Dynamic file naming & folder logic
    test_folder = "test"
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)
    
    filename = f"{inputs['selected_app']}_refactoring_blueprint.md"
    output_path = os.path.join(test_folder, filename)

    print(f"## Kicking off Archaion Mainframe Analysis for {inputs['selected_app']} ##")
    print(f"## Cloud Provider: {inputs['target_cloud']} ##")

    os.environ["ARCHAION_OUTPUT_FILE"] = output_path
    ArchaionCrew().crew().kickoff(inputs=inputs)
    print(f"\nDone! Blueprint saved to: {output_path}")

if __name__ == "__main__":
    run()
