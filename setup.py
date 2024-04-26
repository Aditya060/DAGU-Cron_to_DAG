from setuptools import setup, find_packages

setup(
    name='dagu-cron',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'dagu-cron = dagu_cron_Aditya07.main:cli'
        ]
    }
)
