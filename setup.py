#!/usr/bin/env python

# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import pytimedb



setup(

   name='pytimedb',

   version='0.0.1-beta.1',

   description='Raisonnement temporel.',

   author='Jean-François Baget',

   author_email='baget@lirmm.fr',

   packages=find_packages(), 

   install_requires=['matplotlib']

)