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

# def read_requirements():
#     with open('requirements.txt') as req:
#         return req.readlines()

class CustomInstallCommand(install):
    """Customized setuptools install command to copy the validate_api_key.py file."""
    def run(self):
        install.run(self)
        self.copy_validation_script()

    def copy_validation_script(self):
        src = os.path.join(os.path.dirname(__file__), 'validate_api_key.py')
        dst = os.path.join(os.getcwd(), 'validate_api_key.py')  # Use os.getcwd() to get the current working directory
        
        # Avoid copying if source and destination are the same
        if os.path.abspath(src) != os.path.abspath(dst):
            if os.path.exists(src):
                shutil.copyfile(src, dst)
                print(f"Copied {src} to {dst}")
            else:
                print(f"Source file {src} not found")
        else:
            print(f"Source and destination are the same. No need to copy.")

setup(
    name='reliability_chatbot',
    version='0.33',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        
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
        ('', ['validate_api_key.py','requirements.txt','README.md']),  # Specify the file to be copied
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
