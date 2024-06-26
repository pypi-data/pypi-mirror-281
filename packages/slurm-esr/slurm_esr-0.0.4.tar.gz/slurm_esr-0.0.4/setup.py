from setuptools import find_packages, setup

setup(
    name="slurm_esr",
    version="0.0.4",
    setup_requires=["setuptools-git-versioning"],
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "submit=slurm.submit:submit",
        ],
    },
    # python_requires='==3.9.*',
)
