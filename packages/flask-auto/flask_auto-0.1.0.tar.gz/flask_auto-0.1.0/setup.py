from setuptools import setup, find_packages

setup(
    name='flask_auto',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'python-dotenv',
        'psycopg2-binary',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'create_flask_app=flask_auto.create_flask_app:main',
        ],
    },
    author='Jose Luis Morales',
    author_email='josseluism@gmail.com',
    description='A simple Flask project generator',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ZeusPod/flask_auto',  # Actualiza con la URL de tu repositorio
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
