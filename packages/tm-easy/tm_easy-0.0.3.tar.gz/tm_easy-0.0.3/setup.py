from setuptools import setup, find_packages

setup(
    name='tm_easy',
    version='0.0.3',
    description='teachable machine easy',
    author='yoonjinseok',
    author_email='insomang@hanmail.net',
    url='https://github.com/Yoon-JinSeok/tm-easy',
    install_requires=['keras', 'opencv-python',],
    packages=find_packages(exclude=[]),
    keywords=['teachable', 'machine'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)