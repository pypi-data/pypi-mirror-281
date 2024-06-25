import setuptools

setuptools.setup(
    name="ebsfm-schedule",
    version="0.0.2",
    license='MIT',
    author="cheddars",
    author_email="nezahrish@gmail.com",
    description="Crwaling EBS FM, EBS 외국어전문 방송 편성표",
    long_description=open('README.rst').read(),
    url="https://github.com/cheddars/pypi-ebsfm-schedule",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
