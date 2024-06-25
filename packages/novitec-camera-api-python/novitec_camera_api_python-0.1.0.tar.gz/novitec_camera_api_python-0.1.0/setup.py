from setuptools import setup, find_packages

setup(
    name='novitec_camera_api_python',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    description='Python wrapper for Novitec Camera API',
    author='KiSeon Song',
    author_email='devks0228@novitec.co.kr',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    package_data={
        'novitec_camera_api': ['NovitecCameraAPIWrapper.py', 'NOVITECCAMERAAPIC.dll'],
    },
    python_requires='>=3.10.11',
)
