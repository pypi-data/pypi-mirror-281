from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="banking-adv-coding-proj",
    version="0.1.5",
    author="Zuha Haider",
    author_email="zuha.haider110@gmail.com",
    description="A banking system that helps you deposit, withdraw, change account password, and shows you your account details.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="advancedcoding_bankingproject"),
    package_dir={"": "advancedcoding_bankingproject"},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "run=main:main",
            "read=source.accounts.options:read_accounts"
        ]
    }
)
