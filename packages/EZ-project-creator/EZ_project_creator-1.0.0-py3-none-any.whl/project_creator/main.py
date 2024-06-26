import os
import subprocess
from project_creator.config import load_config, save_config
from project_creator.utils import run_subprocess


def create_project_structure(project_location, project_name, project_type, additional_packages=None):
    """Create project structure and setup environment.

    Args:
        project_location (str): Location to create the project.
        project_name (str): Name of the project.
        project_type (str): Type of the project (full_stack_website, full_stack_data_science, full_stack_app).
        additional_packages (list): List of additional packages to install.
    """
    try:
        # Define the project structure
        structures = {
            "full_stack_website": [
                "backend/app", "backend/tests", "frontend/public", "frontend/src/components", "frontend/src/pages"
            ],
            "full_stack_data_science": [
                "data/raw", "data/processed", "data/external", "notebooks", "src/data", "src/models", "src/app", "src/visualizations", "src/utils", "tests"
            ],
            "full_stack_app": [
                "backend/app", "backend/tests", "mobile/src/components", "mobile/src/screens", "desktop/src/main", "desktop/src/renderer/components", "web/public", "web/src/components", "web/src/pages"
            ]
        }

        # Basic requirements for each project type
        requirements = {
            "full_stack_website": ["Django", "djangorestframework", "pytest", "selenium"],
            "full_stack_data_science": ["pandas", "numpy", "scikit-learn", "matplotlib", "seaborn", "plotly", "jupyter", "pytest"],
            "full_stack_app": ["FastAPI", "uvicorn", "pytest", "react-native", "electron"]
        }

        # Get the chosen structure and requirements
        structure = structures.get(project_type, [])
        if not structure:
            raise ValueError(
                "Invalid project type. Valid options are: full_stack_website, full_stack_data_science, full_stack_app.")
        base_requirements = requirements.get(project_type, [])

        # Create the full project path
        project_path = os.path.join(project_location, project_name)

        # Create the project directory
        os.makedirs(project_path, exist_ok=True)

        # Create the subdirectories
        for folder in structure:
            os.makedirs(os.path.join(project_path, folder), exist_ok=True)

        # Create a virtual environment
        run_subprocess(
            [f"python", "-m", "venv", os.path.join(project_path, "venv")])

        # Activate the virtual environment and install base requirements
        run_subprocess([os.path.join(project_path, "venv",
                       "Scripts", "pip"), "install"] + base_requirements)

        # Install additional packages if provided
        if additional_packages:
            run_subprocess([os.path.join(project_path, "venv",
                           "Scripts", "pip"), "install"] + additional_packages)

        # Create basic README file
        with open(os.path.join(project_path, "README.md"), "w") as f:
            f.write(
                f"# {project_name}\n\n{project_type.replace('_', ' ').title()} project")

        # Create a requirements.txt file
        with open(os.path.join(project_path, "requirements.txt"), "w") as f:
            f.write("\n".join(base_requirements))
            if additional_packages:
                f.write("\n" + "\n".join(additional_packages))

        # Create an initial .gitignore file
        with open(os.path.join(project_path, ".gitignore"), "w") as f:
            f.write("venv/\n__pycache__/\n*.pyc\n")

        # Create a basic setup for different types
        if project_type == "full_stack_website":
            with open(os.path.join(project_path, "backend", "app", "models.py"), "w") as f:
                f.write(
                    "from django.db import models\n\n# Create your models here.\n")
            with open(os.path.join(project_path, "backend", "app", "views.py"), "w") as f:
                f.write(
                    "from django.shortcuts import render\n\n# Create your views here.\n")
            with open(os.path.join(project_path, "backend", "app", "urls.py"), "w") as f:
                f.write(
                    "from django.urls import path\n\n# Define your URL patterns here.\n")
            with open(os.path.join(project_path, "backend", "manage.py"), "w") as f:
                f.write(
                    "import os\nimport sys\n\n"
                    "if __name__ == '__main__':\n"
                    "    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')\n"
                    "    try:\n"
                    "        from django.core.management import execute_from_command_line\n"
                    "    except ImportError as exc:\n"
                    "        raise ImportError(\n"
                    "            \"Couldn't import Django. Are you sure it's installed and \"\n"
                    "            \"available on your PYTHONPATH environment variable? Did you \"\n"
                    "            \"forget to activate a virtual environment?\"\n"
                    "        ) from exc\n"
                    "    execute_from_command_line(sys.argv)\n"
                )

        elif project_type == "full_stack_data_science":
            with open(os.path.join(project_path, "src", "data", "load_data.py"), "w") as f:
                f.write("import pandas as pd\n\n# Function to load data\n")
            with open(os.path.join(project_path, "src", "data", "preprocess.py"), "w") as f:
                f.write("import pandas as pd\n\n# Function to preprocess data\n")
            with open(os.path.join(project_path, "src", "models", "train_model.py"), "w") as f:
                f.write(
                    "from sklearn.model_selection import train_test_split\n\n# Function to train model\n")
            with open(os.path.join(project_path, "src", "models", "predict.py"), "w") as f:
                f.write(
                    "from sklearn.externals import joblib\n\n# Function to make predictions\n")

        elif project_type == "full_stack_app":
            with open(os.path.join(project_path, "backend", "app", "main.py"), "w") as f:
                f.write(
                    "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef read_root():\n    return {'Hello': 'World'}\n")
            with open(os.path.join(project_path, "mobile", "src", "App.js"), "w") as f:
                f.write(
                    "import React from 'react';\nimport { View, Text } from 'react-native';\n\nexport default function App() {\n  return (\n    <View>\n      <Text>Hello, world!</Text>\n    </View>\n  );\n}\n")
            with open(os.path.join(project_path, "desktop", "src", "main", "main.js"), "w") as f:
                f.write(
                    "const { app, BrowserWindow } = require('electron');\n\n"
                    "function createWindow () {\n"
                    "  const win = new BrowserWindow({\n"
                    "    width: 800,\n"
                    "    height: 600,\n"
                    "    webPreferences: {\n"
                    "      nodeIntegration: true\n"
                    "    }\n"
                    "  })\n\n"
                    "  win.loadFile('index.html')\n"
                    "}\n\n"
                    "app.whenReady().then(createWindow)\n"
                )
            with open(os.path.join(project_path, "web", "src", "App.js"), "w") as f:
                f.write(
                    "import React from 'react';\n\n"
                    "function App() {\n"
                    "  return (\n"
                    "    <div className='App'>\n"
                    "      <header className='App-header'>\n"
                    "        <p>Hello, World!</p>\n"
                    "      </header>\n"
                    "    </div>\n"
                    "  );\n"
                    "}\n\n"
                    "export default App;\n"
                )

        print(
            f"Project {project_name} created successfully at {project_path}!")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running a subprocess: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    config = load_config()
    default_location = config.get("default_location", "")

    project_location = input(
        f"Enter the location for the project [{default_location}]: ") or default_location
    project_name = input("Enter the project name: ")
    project_type = input(
        "Enter the project type (full_stack_website, full_stack_data_science, full_stack_app): ")
    additional_packages = input(
        "Enter additional packages to install (comma-separated): ").split(',')

    # Save the project location for future use
    config["default_location"] = project_location
    save_config(config)

    create_project_structure(
        project_location, project_name, project_type, additional_packages)


if __name__ == "__main__":
    main()
