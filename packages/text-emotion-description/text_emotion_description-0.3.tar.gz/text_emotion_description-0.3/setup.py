from setuptools import setup, find_packages

setup(
    name='text_emotion_description',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'seaborn',
        'matplotlib',
        'nltk',
        'scikit-learn',
        'tensorflow',
        'keras'
    ],
    entry_points={
        'console_scripts': [
            'text_emotion_description = text_emotion_description.main:main'
        ]
    },
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    description='A Python package for emotion detection using neural networks',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ankith Manchale',
)
