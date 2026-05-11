from setuptools import find_packages,setup
from typing import List

hyphen_dot_e = '-.e'
def get_requirements(file_path:str)->List[str]:
    requirements=[]


    with open(file_path)as file_obj:
        requirements=file_obj.readline()
        requirements=[req.replace('/n','') for req in requirements]
        if hyphen_dot_e in requirements:
            requirements.remove(hyphen_dot_e)
    return requirements
setup(
    name='CineFlicx',
    version='0.0.0',
    author='Shubham Joshi',
    author_email='indsjos@gmail.com',
    packages=find_packages(),
    install_requires=['numpy','pandas']
)