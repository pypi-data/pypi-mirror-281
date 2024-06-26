from setuptools import setup, find_packages


# Функция для чтения зависимостей из requirements.txt
def parse_requirements(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]


# Чтение зависимостей из requirements.txt
requirements = parse_requirements('requirements.txt')

setup(
    name='logs_weasel',
    version='1.16',
    packages=find_packages(),
    install_requires=requirements,
    author='Aleksei Goncharov',
    author_email='gnlx@proton.me',
    description='Easy-to-read display of logs with save to db redis and sending notifications in telegram',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/gnlxpy/logs_weasel',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
