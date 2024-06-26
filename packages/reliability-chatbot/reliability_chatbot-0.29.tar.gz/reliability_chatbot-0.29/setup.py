from setuptools import setup, find_packages

# setup(
#     name='reliability_chatbot',
#     version='0.11',
#     packages=find_packages(),
#     include_package_data=True,
#     install_requires=[
        
#     ],
#     package_data={
#         'app1': ['*.py'],  # Include all Python files in question_answer_db
#     },
#     classifiers=[
#         'Framework :: Django',
#         'Programming Language :: Python :: 3',
#         'License :: OSI Approved :: MIT License',
#         'Operating System :: OS Independent',
#     ],
# )



from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import shutil

with open("README.md", "r") as fh:
    long_description = fh.read()

class CustomInstallCommand(install):
    """Customized setuptools install command to copy the validate_api_key.py file."""
    def run(self):
        install.run(self)
        self.copy_validation_script()

    def copy_validation_script(self):
        src = os.path.join(os.path.dirname(__file__), 'validate_api_key.py')
        dst = os.path.join(os.getcwd(), './validate_api_key.py')  # Use os.getcwd() to get the current working directory
        
        # Avoid copying if source and destination are the same
        if os.path.abspath(src) != os.path.abspath(dst):
            if os.path.exists(src):
                shutil.copyfile(src, dst)
                print(f"Copied {src} to {dst}")
            else:
                print(f"Source file {src} not found")
        else:
            print(f"Source and destination are the same. No need to copy.")

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append((path, [os.path.join(path, filename)]))
    return paths

setup(
    name='reliability_chatbot',
    version='0.29',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'asgiref==3.8.1',
        'certifi==2024.6.2',
        'charset-normalizer==3.3.2',
        'click==8.1.7',
        'Django==5.0.6',
        'filelock==3.15.1',
        'fsspec==2024.6.0',
        'huggingface-hub==0.23.4',
        'idna==3.7',
        'inflect==7.2.1',
        'Jinja2==3.1.4',
        'joblib==1.4.2',
        'MarkupSafe==2.1.5',
        'more-itertools==10.3.0',
        'mpmath==1.3.0',
        'networkx==3.3',
        'nltk==3.8.1',
        'numpy==1.24.4',
        'packaging==24.1',
        'pillow==10.3.0',
        'PyYAML==6.0.1',
        'regex==2024.5.15',
        'requests==2.32.3',
        'safetensors==0.4.3',
        'scikit-learn==1.5.0',
        'scipy==1.13.1',
        'sentence-transformers==3.0.1',
        'sqlparse==0.5.0',
        'sympy==1.12.1',
        'threadpoolctl==3.5.0',
        'tokenizers==0.19.1',
        'torch==2.2.2',
        'tqdm==4.66.4',
        'transformers==4.41.2',
        'typeguard==4.3.0',
        'typing_extensions==4.12.2',
        'urllib3==2.2.2'
    ],
    entry_points={
        'console_scripts': [
            'manage.py = app1.manage:main',
            'configure-aws = app1.scripts.configure_aws:main',
            'readme = app1.scripts.readme:main',
        ],
    },
    package_data={
        'app1': [],  # Ensure no extra files are added here
    },
    data_files=[
        ('', ['validate_api_key.py']),  # Specify the file to be copied
    ],
    author='Swati Saini',
    author_email='swati@mixorg.com',
    description='A Django app for chatbot functionality.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/saini2001/chatbot_code',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3.11',
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
)
