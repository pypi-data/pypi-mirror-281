1. 패키지를 빌드하기 위해 setuptools와 wheel을 설치합니다.: pip install setuptools wheel
2. 그런 다음 패키지를 빌드합니다: python setup.py sdist bdist_wheel
3. PyPI에 업로드하기 위해 twine을 설치합니다: pip install twine
4. PyPI에 업로드합니다: twine upload dist/*


