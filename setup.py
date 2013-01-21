try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
config = {
    'description': 'End Point Health Checker',
    'author': 'Vickleford',
    'url': 'https://github.com/vickleford/',
    'download_url': 'https://github.com/vickleford/',
    'author_email': 'vwatkinsjr@gmail.com',
    'version': '0.1',
    'install_requires': ['PyYAML', 'python-memcached', 'MySQL-python', 'psycopg2'],
    'packages': ['ephc'],
    'name': 'ephc',
    'entry_points': {
        'console_scripts': [
            'ephc = ephc.script:run'
        ]
    }
}

setup(**config)
