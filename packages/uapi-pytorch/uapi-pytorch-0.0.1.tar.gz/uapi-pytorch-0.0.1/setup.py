from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
      long_description = fh.read()

setup(
      name="uapi-pytorch",
      version="0.0.1",
      author="test",
      author_email="test@163.com",
      description="pytorch model pipeline",
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages()
)
