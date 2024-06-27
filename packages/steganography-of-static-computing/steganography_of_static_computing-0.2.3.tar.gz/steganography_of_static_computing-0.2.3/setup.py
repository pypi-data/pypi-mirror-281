from setuptools import setup, find_packages

setup(
    name="steganography_of_static_computing",
    version="0.2.3",
    author="ECUsam",
    author_email="wangyanzhao2003@gmail.com",
    description="project",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/ECUsam/Steganography",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "shiny",
        "opencv-python",
        "numpy",
        "line_profiler",
        "Pillow",
    ],
)
