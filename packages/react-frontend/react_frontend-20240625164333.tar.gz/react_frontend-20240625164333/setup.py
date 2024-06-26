from setuptools import setup, find_packages

setup(
    name="react-frontend",
    version="20240625164333",
    description="The React frontend",
    url="https://github.com/gertjanstulp/ha-react-frontend",
    author="Gertjan Stulp",
    author_email="",
    packages=find_packages(include=["react_frontend", "react_frontend.*"]),
    include_package_data=True,
    zip_safe=False,
)