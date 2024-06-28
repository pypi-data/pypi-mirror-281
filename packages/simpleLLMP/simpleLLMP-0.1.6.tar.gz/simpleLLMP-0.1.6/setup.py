from setuptools import setup, find_packages

setup(
    name='simpleLLMP',
    version='0.1.6',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'openai',
        'pytesseract',
        'pdf2image',
        'pillow',
        'PyPDF2',
        'requests'
    ],
    url='https://github.com/ykim336/simpleML',  
    author='Yvon Kim',
    author_email='kmyn7up@gmail.com',
    description='A simple library for interacting with OpenAI models.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
