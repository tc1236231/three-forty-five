from setuptools import setup, find_packages

setup(
    name='tff',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask==1.0.2',
        'Flask-SQLAlchemy==2.3.2',
        'Flask-Markdown==0.3',
        'Flask-Dance==1.2.0',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
