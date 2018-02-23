#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.cli.command_template.command_template import CommandTemplate

UPLOAD_FILE_FROM_TREX = CommandTemplate("curl --upload-file {file_path} {url}")
DOWNLOAD_FILE_TO_TREX = CommandTemplate("wget -O {file_path} {url}")
