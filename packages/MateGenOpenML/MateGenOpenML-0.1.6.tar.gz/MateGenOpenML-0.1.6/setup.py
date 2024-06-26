from setuptools import setup, find_packages

setup(
    name='MateGenOpenML',  # 替换为你的包名
    version='0.1.6',
    packages=find_packages(),
    install_requires=[
        'IPython',
        'openai',
        'matplotlib',
        'seaborn',
        'pandas',
        'datetime',
        'pathlib',  
    ],
    entry_points={
        'console_scripts': [
            'mategenopenml=MateGenOpenML.assistant:main',
        ],
    },
    author='Jiutian',
    author_email='2323365771@qq.com',
    description='九天老师机器学习实战公开课智能助教Agent',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)