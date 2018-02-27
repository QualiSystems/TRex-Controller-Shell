#!/usr/bin/python
# -*- coding: utf-8 -*-

from threading import RLock

from cloudshell.core.context.error_handling_context import ErrorHandlingContext
from cloudshell.shell.core.driver_context import AutoLoadDetails
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface

from cloudshell.devices.driver_helper import get_api, get_cli, get_logger_with_thread_id

from cloudshell.traffic.trex.client.trex_client.trex_client import CTRexClient

from trex_controller.runners.trex_server_config_runner import TRexServerConfigurationRunner
from trex_controller.runners.trex_test_runner import TRexTestRunner
from trex_controller.helpers.configuration_attributes_structure import TrafficGeneratorControllerResource


class TRexControllerDriver(ResourceDriverInterface):
    def __init__(self):
        super(TRexControllerDriver, self).__init__()
        self._cli = None
        self._trex_client = None
        self.lock = RLock()

    def initialize(self, context):
        """
        :param context: ResourceCommandContext,ReservationContextDetailsobject with all Resource Attributes inside
        :type context:  context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        resource_config = TrafficGeneratorControllerResource.from_context(context)
        session_pool_size = int(resource_config.sessions_concurrency_limit)
        self._cli = get_cli(session_pool_size)

        return 'Finished initializing'

    def get_inventory(self, context):
        """
        Autoload inventory
        Return device structure with all standard attributes
        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        return AutoLoadDetails([], [])

    def _get_trex_client(self, resource_config):

        with self.lock:
            if self._trex_client is None:
                self._trex_client = CTRexClient(trex_host=resource_config.address,
                                                trex_daemon_port=resource_config.trex_daemon_port)

            return self._trex_client

    def upload_server_config(self, context, config_file_url):
        """ Upload server configuration file to FTP/TFTP Server """

        logger = get_logger_with_thread_id(context)
        logger.info("Upload TRex Server configuration command started")

        with ErrorHandlingContext(logger):
            cs_api = get_api(context)
            resource_config = TrafficGeneratorControllerResource.create_from_chassis_resource(context=context,
                                                                                              cs_api=cs_api)

            server_config_runner = TRexServerConfigurationRunner(cli=self._cli,
                                                                 resource_config=resource_config,
                                                                 logger=logger)

            server_config_runner.upload_trex_server_config(server_config_url=config_file_url)

        logger.info("Upload TRex Server configuration command ended")

    def download_server_config(self, context, config_file_url):
        """ Download Cisco TRex Server configuration from FTP/TFTP Server """

        logger = get_logger_with_thread_id(context)
        logger.info("Download TRex Server configuration command started")

        with ErrorHandlingContext(logger):
            cs_api = get_api(context)
            resource_config = TrafficGeneratorControllerResource.create_from_chassis_resource(context=context,
                                                                                              cs_api=cs_api)

            server_config_runner = TRexServerConfigurationRunner(cli=self._cli,
                                                                 resource_config=resource_config,
                                                                 logger=logger)

            server_config_runner.download_trex_server_config(server_config_url=config_file_url)

        logger.info("Download TRex Server configuration command ended")

    def load_test_config(self, context, config_file_url):
        """ Load test configuration file to TRex"""

        logger = get_logger_with_thread_id(context)
        logger.info("Load test configuration file command started")
        with ErrorHandlingContext(logger):
            cs_api = get_api(context)
            resource_config = TrafficGeneratorControllerResource.create_from_chassis_resource(context=context,
                                                                                              cs_api=cs_api)

            trex_client = self._get_trex_client(resource_config=resource_config)

            controll_traffic = TRexTestRunner(cli=self._cli,
                                              trex_client=trex_client,
                                              resource_config=resource_config,
                                              logger=logger)

            controll_traffic.load_test_config(test_config_url=config_file_url)

        logger.info("Load test configuration file command ended")

    def start_traffic(self, context, test_file_name, blocking, timeout, latency):
        """ Start traffic """

        logger = get_logger_with_thread_id(context)
        logger.info("Start traffic command started")

        with ErrorHandlingContext(logger):
            cs_api = get_api(context)
            resource_config = TrafficGeneratorControllerResource.create_from_chassis_resource(context=context,
                                                                                              cs_api=cs_api)

            controll_traffic = TRexTestRunner(cli=self._cli,
                                              trex_client=self._trex_client,
                                              resource_config=resource_config,
                                              logger=logger)

            blocking = (blocking == "True")

            if latency:
                latency = int(latency)

            controll_traffic.start_traffic(test_config=test_file_name,
                                           block_to_success=blocking,
                                           timeout=float(timeout),
                                           latency=latency)

        logger.info("Start traffic command ended")

    def stop_traffic(self, context, force):
        """ Stop traffic and unreserving ports """

        logger = get_logger_with_thread_id(context)
        logger.info("Stop traffic command started")

        with ErrorHandlingContext(logger):
            cs_api = get_api(context)
            resource_config = TrafficGeneratorControllerResource.create_from_chassis_resource(context=context,
                                                                                              cs_api=cs_api)

            trex_client = self._get_trex_client(resource_config=resource_config)

            controll_traffic = TRexTestRunner(cli=self._cli,
                                              trex_client=trex_client,
                                              resource_config=resource_config,
                                              logger=logger)

            force = (force == "True")
            controll_traffic.stop_traffic(force)

        logger.info("Stop traffic command ended")

    def get_results(self, context):
        """ Attach result file to the reservation """

        logger = get_logger_with_thread_id(context)
        logger.info("Get results command started")

        with ErrorHandlingContext(logger):
            cs_api = get_api(context)
            resource_config = TrafficGeneratorControllerResource.create_from_chassis_resource(context=context,
                                                                                              cs_api=cs_api)

            trex_client = self._get_trex_client(resource_config=resource_config)

            controll_traffic = TRexTestRunner(cli=self._cli,
                                              trex_client=trex_client,
                                              resource_config=resource_config,
                                              logger=logger)

            res = controll_traffic.get_results()

            logger.info("Get results command ended")
            return str(res)

    def cleanup_reservation(self, context):
        """ Clear reservation when it ends """

        logger = get_logger_with_thread_id(context)
        logger.info("Cleanup reservation command started")

        with ErrorHandlingContext(logger):
            cs_api = get_api(context)
            resource_config = TrafficGeneratorControllerResource.create_from_chassis_resource(context=context,
                                                                                              cs_api=cs_api)

        logger.info("Cleanup reservation command ended")

    def cleanup(self):
        """ Close runners """

        pass

    def keep_alive(self, context, cancellation_context):
        """  """

        logger = get_logger_with_thread_id(context)
        logger.info("Keep alive command started")

        with ErrorHandlingContext(logger):
            cs_api = get_api(context)
            resource_config = TrafficGeneratorControllerResource.create_from_chassis_resource(context=context,
                                                                                              cs_api=cs_api)

        logger.info("Keep alive command ended")
