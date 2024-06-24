from setuptools import setup, find_packages

setup(
    name="text-adventure-game",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    description="冒险战斗恋爱文字游戏",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/text_adventure_game",
    author="将和",
    author_email="1727949032@qq.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests>=2.20.0",
    ],
)
