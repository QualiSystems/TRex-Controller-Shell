#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from trex_controller.command_templates.trex_server_config import DOWNLOAD_FILE_TO_TREX, UPLOAD_FILE_FROM_TREX

TREX_SERVER_CONFIG_FILE = "/etc/trex_cfg.yaml"


class TRexServerConfigActions(object):
    def __init__(self, cli_service, logger):
        """ Save and Restore device configuration actions

        :param cli_service: default mode cli_service
        """

        self._cli_service = cli_service
        self._logger = logger

    def download_file(self, server_config_url):
        """ Download file from FTP/TFTP Server """

        output = CommandTemplateExecutor(self._cli_service,
                                         DOWNLOAD_FILE_TO_TREX).execute_command(file_path=TREX_SERVER_CONFIG_FILE,
                                                                                  url=server_config_url)

        if not re.search(r"saved\s*\[\d+\]", output, re.IGNORECASE):
            self._logger.error("Downloading TRex server configuration failed: {}".format(output))
            raise Exception("Downloading TRex server configuration failed.")

    def upload_file(self, server_config_url):
        """ Upload file to FTP/TFTP Server """

        output = CommandTemplateExecutor(self._cli_service,
                                         UPLOAD_FILE_FROM_TREX).execute_command(file_path=TREX_SERVER_CONFIG_FILE,
                                                                              url=server_config_url)

        if re.search(r"curl:|[Ff]ail|[Ee]rror]", output, re.IGNORECASE):
            self._logger.error("Uploading TRex server configuration failed: {}".format(output))
            raise Exception("Uploading TRex server configuration failed.")
