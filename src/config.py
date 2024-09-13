#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The FastAPI settings for GRNDP-server project.

Created on Fri Sep 13 12:25:14 2024
@author: Tz Wang <wangtianze23@mails.ucas.ac.cn>
"""

from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

LOCAL_RESOURCE_ROOT = BASE_DIR / 'local'
