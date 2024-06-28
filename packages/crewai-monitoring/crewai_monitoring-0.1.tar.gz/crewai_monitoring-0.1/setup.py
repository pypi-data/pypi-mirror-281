from setuptools import setup, find_packages

setup(
    name="crewai_monitoring",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "crewAI",
        "tiktoken",
        "numpy",
    ],
    author="AI Anytime",
    author_email="contact@aianytime.net",
    description="A library for monitoring CrewAI agents, including token usage, cost calculation, logging, carbon emissions, and more.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/aianytime/crewai_monitoring",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)

