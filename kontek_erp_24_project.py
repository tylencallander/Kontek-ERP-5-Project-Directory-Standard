import os
import json

# Loading projects from the projects.json file in the ERP 1 folder

def load_projects(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}

# Verify the project folders exist based off of the template directory formatting

def verify_project_folders(template_path, projects):
    template_folders = [f for f in os.listdir(template_path) if os.path.isdir(os.path.join(template_path, f))]
    errors = {}
    project_folders = {}

    for project, details in projects.items():
        full_path = details['projectfullpath']
        existing_folders = [f for f in os.listdir(full_path) if os.path.isdir(os.path.join(full_path, f))]
        project_folder_info = {}

        for folder in template_folders:
            folder_path = os.path.join(full_path, folder)
            if folder in existing_folders:
                project_folder_info[folder.lower()] = {
                    'fullpath': folder_path,
                    'path': folder_path.split('\\')
                }
            else:
                errors.setdefault(f"{folder.lower()}_foldermissing", []).append(project)

        project_folders[project] = {**details, **project_folder_info}

    return project_folders, errors

# Saving to a new json file

def save_to_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Used ERP 1 projects.json file for testing, can be replaced by any other json projects file in the ERP folder

def main():
    project_file_path = 'P:/KONTEK/ENGINEERING/ELECTRICAL/Application Development/ERP/1. Project Folder Search/V3_2024-06-04/projects.json'
    template_directory = 'P:/KONTEK/CUSTOMER/~PROJECT FOLDER TEMPLATE - DO NOT DELETE, DO NOT CUT/JOB NUMBER AND SYSTEM NAME'
    output_projects_file = 'projectfolders.json'
    output_errors_file = 'errors.json'

    projects = load_projects(project_file_path)
    project_folders, errors = verify_project_folders(template_directory, projects)

    save_to_json(project_folders, output_projects_file)
    save_to_json(errors, output_errors_file)

if __name__ == "__main__":
    main()