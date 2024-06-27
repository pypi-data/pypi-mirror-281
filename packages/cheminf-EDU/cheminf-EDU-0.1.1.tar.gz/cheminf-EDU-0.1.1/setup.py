from setuptools import setup, find_packages

setup(
    name='cheminf-EDU',
    version='0.1.1',  
    author='Ziheng Zhao',
    author_email='zhacisbw4801@gmail.com',
    description='Chemie informatik education',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Yakimochinai/cheminf-EDU',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # 列出你的依赖包，例如
        # 'requests>=2.20',
    ],
)
