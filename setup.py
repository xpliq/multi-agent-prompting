from setuptools import find_packages, setup
from typing import List 

HYPHEN_E_DOT = '-e .'
def get_requirements(file_path)->List[str]:
    requirements = []   
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
                                
    return requirements
        
setup(
    name='multi-agent-persona',
    version='0.1',
    author='xpliq',
    author_email='xpliqbusiness@gmail.com',
    package=find_packages(),
    install_requires=get_requirements('requirements.txt')
)