from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="heros_time_syncronizer",
    version="0.1.0",
    author="Lee Suhyun",
    author_email="shlee2@withtech.co.kr",
    description="A Time Syncronizer for HEROS",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="http://192.168.0.203:7990/projects/HERO/repos/time_sync/browse",  # 패키지의 홈페이지 URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pyqt5",
    ],
    entry_points={
        'console_scripts': [
            'heros-time-sync=heros_time_sync.main:main',  # main.py의 main 함수를 진입점으로 설정
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
