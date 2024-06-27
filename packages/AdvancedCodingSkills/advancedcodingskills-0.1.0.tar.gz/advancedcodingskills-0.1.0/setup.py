from setuptools import setup, find_packages

setup(
    name="AdvancedCodingSkills",
    version="0.1.0",
    author="Armin Karimi",
    author_email="Akarimi@stud.macromedia.de",
    description="In response to the dynamic demands of student life, we present our Multi-Purpose Program—a flexible application carefully designed to meet the unique needs of students and beyond. Beyond its usefulness for students, this application extends its functionality to anyone seeking efficient task management, expense tracking, and a touch of entertainment a game(sudoku).For Saving Method we have used JSON and the whole project is coded using inheritance.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PersianArmin/AdvancedCodingSkills",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
