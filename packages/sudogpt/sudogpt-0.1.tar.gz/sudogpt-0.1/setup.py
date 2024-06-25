from setuptools import setup

description = "Let openai into your computer"

setup(
    name="sudogpt",
    version="0.1",
    description=description,
    long_description=description,
    url="https://github.com/tim-sparq/sudogpt",
    author="Tim Savage",
    author_email="tim.savage@datsparq.ai",
    license="MIT",
    packages=["sudogpt"],
    install_requires=[
        "openai",
    ],
    entry_points={"console_scripts": ["sudogpt=sudogpt.command_line:main"]},
    zip_safe=False,
)
