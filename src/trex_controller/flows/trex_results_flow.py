#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.traffic.trex.client.trex_client import trex_exceptions


class TRexResultsFlow(object):

    def __init__(self, trex_client, logger):
        self._logger = logger
        self._trex_client = trex_client

    def get_results(self):
        """ Get results """

        try:
            return self._trex_client.get_result_obj()
        except Exception as e:
            self._logger.exception(e)
            raise Exception("Error happened during getting TRex results")
