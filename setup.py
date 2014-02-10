# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

from setuptools import find_packages, setup


def read_from_req(extra=None):
    f_name = "requirements.txt"

    if extra is not None:
        f_name = "requirements-%s.txt" % extra

    with open(f_name) as f:
        requirements = [line.strip() for line in f if line.strip()]

    return requirements


setup(name="chores",
      version="0.1.0",
      description="Simplistic chore minder",
      packages=find_packages(),
      install_requires=read_from_req(),
      setup_requires='',
      extras_require=dict(test=read_from_req("test")),
)
