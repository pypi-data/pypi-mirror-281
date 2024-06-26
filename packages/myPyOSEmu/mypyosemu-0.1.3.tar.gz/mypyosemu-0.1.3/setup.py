# setup.py

from setuptools import setup, find_packages

setup(
    name='myPyOSEmu',
    version='0.1.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'pythonos=pythonOS.pythonos:main',
        ],
    },
    author='Darren Chase Papa',
    author_email='darenchasepapa@gmail.com',
    description='An emulated OS in Python',
    long_description="https://ChaseDevelopmentGroup.pythonanywhere.com/docs",
    url='https://github.com/yourusername/pyos',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
