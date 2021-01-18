from setuptools import setup

setup(
    name='api_teamnexus',
    packages=['api_teamnexus'],
    package_dir={'api_teamnexus': 'api_teamnexus'},
    version='0.1.0',
    description='Api per l\'integrazione della piattaforma del TeamNexus',
    author='Me',
    license='MIT',
    url='https://github.com/Sedan55/api_teamnexus.git',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)