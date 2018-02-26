#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from trex_controller.actions.trex_test_actions import TRexTestActions


class TRexLoadTestConfigFlow(object):

    def __init__(self, cli_handler, trex_client, logger):
        self._logger = logger
        self._cli_handler = cli_handler
        self._trex_client = trex_client

    def load_test_config(self, test_files_location, test_config_url):
        """ Load test configuration files from FTP/TFTP Server or Execution Server"""

        if test_config_url.lower().startswith("ftp") or test_config_url.lower().startswith("tftp"):
            with self._cli_handler.get_cli_service(self._cli_handler.enable_mode) as enable_session:
                config_actions = TRexTestActions(enable_session, self._trex_client, self._logger)

                config_actions.download_file(test_config_url=test_config_url)
        else:
            test_file_full_path = os.path.join(test_files_location, test_config_url)
            self._trex_client.push_files(test_file_full_path)
