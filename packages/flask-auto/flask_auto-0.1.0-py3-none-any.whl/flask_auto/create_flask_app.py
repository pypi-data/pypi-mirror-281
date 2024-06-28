import os
import subprocess
import sys
import platform

def create_virtualenv(project_path):
    subprocess.run(['python', '-m', 'venv', os.path.join(project_path, 'venv')])

def install_dependencies(project_path):
    if platform.system() == 'Windows':
        pip_executable = os.path.join(project_path, 'venv', 'Scripts', 'pip')
    else:
        pip_executable = os.path.join(project_path, 'venv', 'bin', 'pip')
    subprocess.run([pip_executable, 'install', 'flask'])
    subprocess.run([pip_executable, 'install', 'flask-sqlalchemy'])
    subprocess.run([pip_executable, 'install', 'python-dotenv'])
    subprocess.run([pip_executable, 'install', 'psycopg2-binary'])
    subprocess.run([pip_executable, 'install', 'requests'])

    # Capturar la salida de pip freeze y escribirla en requirements.txt
    result = subprocess.run([pip_executable, 'freeze'], capture_output=True, text=True)
    with open(os.path.join(project_path, 'requirements.txt'), 'w') as f:
        f.write(result.stdout)

def create_folder_structure(project_path):
    os.makedirs(os.path.join(project_path, 'app', 'models'), exist_ok=True)
    os.makedirs(os.path.join(project_path, 'app', 'views'), exist_ok=True)
    os.makedirs(os.path.join(project_path, 'app', 'controllers'), exist_ok=True)
    os.makedirs(os.path.join(project_path, 'app', 'templates'), exist_ok=True)
    os.makedirs(os.path.join(project_path, 'app', 'utils'), exist_ok=True)

def create_init_files(project_path):
    open(os.path.join(project_path, 'app', '__init__.py'), 'w').close()
    open(os.path.join(project_path, 'app', 'models', '__init__.py'), 'w').close()
    open(os.path.join(project_path, 'app', 'views', '__init__.py'), 'w').close()
    open(os.path.join(project_path, 'app', 'controllers', '__init__.py'), 'w').close()
    open(os.path.join(project_path, 'app', 'utils', '__init__.py'), 'w').close()

def create_run_file(project_path):
    run_content = '''from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
'''
    with open(os.path.join(project_path, 'run.py'), 'w') as run_file:
        run_file.write(run_content)

def create_app_init(project_path):
    init_content = '''from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    load_dotenv()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    return app
'''
    with open(os.path.join(project_path, 'app', '__init__.py'), 'w') as init_file:
        init_file.write(init_content)

def create_gitignore_file(project_path):
    gitignore_content = '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtualenv
venv/
ENV/
env/
env.bak/
venv.bak/

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/
'''
    with open(os.path.join(project_path, '.gitignore'), 'w') as gitignore_file:
        gitignore_file.write(gitignore_content)

def create_docker_files(project_path):
    dockerfile_content = '''# Utiliza una imagen base oficial de Python
FROM python:3.8-slim-buster

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de requisitos
COPY requirements.txt requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Establece las variables de entorno para la base de datos
ENV DATABASE_URL=sqlite:///db.sqlite3

# Expone el puerto que la aplicación usará
EXPOSE 5000

# Comando para correr la aplicación
CMD ["python", "run.py"]
'''
    with open(os.path.join(project_path, 'Dockerfile'), 'w') as dockerfile:
        dockerfile.write(dockerfile_content)

    dockerignore_content = '''venv/
__pycache__/
*.py[cod]
*$py.class
.git
'''
    with open(os.path.join(project_path, '.dockerignore'), 'w') as dockerignore:
        dockerignore.write(dockerignore_content)

def create_dotenv_file(project_path):
    dotenv_content = '''DATABASE_URL=sqlite:///db.sqlite3
SECRET_KEY=supersecretkey
'''
    with open(os.path.join(project_path, '.env'), 'w') as dotenv_file:
        dotenv_file.write(dotenv_content)

def main():
    if len(sys.argv) != 3:
        print("Usage: python create_flask_app.py <project_name> <destination_directory>")
        sys.exit(1)

    project_name = sys.argv[1]
    destination_directory = sys.argv[2]
    
    project_path = os.path.join(destination_directory, project_name)
    
    if not os.path.exists(destination_directory):
        print(f"Error: Destination directory {destination_directory} does not exist.")
        sys.exit(1)

    os.makedirs(project_path, exist_ok=True)
    create_virtualenv(project_path)
    install_dependencies(project_path)
    create_folder_structure(project_path)
    create_init_files(project_path)
    create_run_file(project_path)
    create_app_init(project_path)
    create_gitignore_file(project_path)
    create_docker_files(project_path)
    create_dotenv_file(project_path)

    print(f'Flask project "{project_name}" created successfully in {destination_directory}.')

if __name__ == "__main__":
    main()
