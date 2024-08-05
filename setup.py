from setuptools import setup, find_packages

setup(
    name="Requri",
    version="0.1.0",
    description="A requirement and traceability manager for teams size 1.",
    author="Kason Bennett",
    author_email="kasonbennett65@gmail.com",
    url="https://github.com/smileyface/Requri",  # Update with your project's URL
    packages=find_packages(),
    install_requires=[
        'ply>=3.11',  # lexer
        'pytest>=8.2.2',  # Testing
        'clang>=17.0.6'  # C++ parsing
        'jsonlib',  # Example dependency, adjust as necessary
        'tkinter',  # UI components
        'logging',  # Standard library, included by default
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",  # Update with your project's license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
