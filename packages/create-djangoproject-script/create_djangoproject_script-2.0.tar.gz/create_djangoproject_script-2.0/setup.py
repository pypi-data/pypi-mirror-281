from setuptools import setup, find_packages

setup(
    name="create_djangoproject_script",  # Your package name
    version="2.0",  # Initial release version
    author="kamalkant",
    author_email="kamalkantupadhyay255@gmail.com",
    description="A script to create Django projects and apps",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kamalkant255/create_djangoproject",  # URL to your project's repository
    packages=find_packages(),  # Automatically find packages in the directory
    py_modules=["create_django_project"],
    install_requires=[
        "Django>=3.2,<4.0",
        "mysqlclient",
        "djangorestframework",
        "drf-yasg",
        "djangorestframework-simplejwt",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "create_django_project=create_django_project:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
