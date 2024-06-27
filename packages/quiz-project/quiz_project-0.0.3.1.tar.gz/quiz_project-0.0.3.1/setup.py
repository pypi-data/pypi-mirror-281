from setuptools import setup, find_packages




VERSION = '0.0.3.1'
DESCRIPTION = 'Quiz creator and displayer'
LONG_DESCRIPTION = 'Advanced coding skills project: A game of a quiz that allows you to create it and save it, and play your own and other saved quizzes'

# Setting up
setup(
    version=VERSION,
    name="quiz_project",
    author="Mariana Aguerrevere",
    author_email="aamariana1907@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'quiz', 'creator','display', 'game']
)