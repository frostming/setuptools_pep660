import os
import shutil
from glob import glob

import nox

PYTHON_ALL_VERSIONS = ["2.7", "3.6", "3.7", "3.8", "3.9"]


@nox.session(python=PYTHON_ALL_VERSIONS)
def test_build_editable(session):
    session.run("pip", "install", ".")
    session.chdir("tests/demo")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    session.run("python", "build.py")
    wheel_file = glob("dist/*.whl")[0]
    session.run("python", "-m", "pip", "install", wheel_file)
    session.run("python", "-c", "import a; print(a)")
