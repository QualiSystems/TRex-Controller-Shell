#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re

from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from cloudshell.traffic.trex.command_templates.trex_common import FILE_INFO, MAKE_DIRECTORY

from trex_controller.command_templates.trex_config import DOWNLOAD_FILE_TO_TREX


class TRexTestActions(object):
    def __init__(self, cli_service, trex_client, logger):
        """ Actions with test configuration files """

        self._cli_service = cli_service
        self._trex_client = trex_client
        self._logger = logger

    def download_file(self, test_config_url):
        """ Download file from FTP/TFTP Server """

        try:
            test_files_location = self._trex_client.get_trex_files_path()
        except Exception as e:
            self._logger.exception(e)
            raise Exception("Error happened during determination TRex files location")

        output = CommandTemplateExecutor(self._cli_service,
                                         FILE_INFO).execute_command(file_path=test_files_location)

        if "no such file or directory" in output.lower():
            CommandTemplateExecutor(self._cli_service,
                                    MAKE_DIRECTORY).execute_command(path=test_files_location)

        file_name = os.path.basename(test_config_url)
        output = CommandTemplateExecutor(self._cli_service,
                                         DOWNLOAD_FILE_TO_TREX).execute_command(file_path=os.path.join(test_files_location, file_name),
                                                                                url=test_config_url)

        if not re.search(r"saved\s*\[\d+\]", output, re.IGNORECASE):
            self._logger.error("Downloading TRex test configuration file failed: {}".format(output))
            raise Exception("Downloading TRex test configuration file failed.")
