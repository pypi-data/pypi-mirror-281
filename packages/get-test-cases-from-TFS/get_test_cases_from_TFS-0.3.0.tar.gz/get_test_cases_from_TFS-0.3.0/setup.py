from pkg_resources import parse_requirements
from setuptools import setup, find_packages


def load_requirements(file_name):
    with open(file_name) as f:
        return [str(requirement) for requirement in parse_requirements(f)]
    
setup(
    name='get_test_cases_from_TFS',
    version='0.3.0',
    packages=find_packages(),
    install_requires=load_requirements('requirements.txt'),
    author='Ayman Mansour, Mohanad Hesham',
    author_email='Ayman.Mansour@integrant.com, Mohanad.hesham@integrant.com',
    description='this Lib is to get the TFS testPlan data, and communicate with TFS API to get the test cases from TFS. Then extract the Testcases as XML file.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
