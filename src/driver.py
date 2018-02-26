#!/usr/bin/python
# -*- coding: utf-8 -*-

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

    def initialize(self, context):
        """
        :param context: ResourceCommandContext,ReservationContextDetailsobject with all Resource Attributes inside
        :type context:  context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        cs_api = get_api(context)
        resource_config = TrafficGeneratorControllerResource.create_from_chassis_resource(context=context,
                                                                                          cs_api=cs_api)
        session_pool_size = int(resource_config.sessions_concurrency_limit)
        self._cli = get_cli(session_pool_size)

        self._trex_client = CTRexClient(trex_host=resource_config.address,
                                        trex_daemon_port=resource_config.trex_daemon_port)

    def get_inventory(self, context):
        """
        Autoload inventory
        Return device structure with all standard attributes
        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        return AutoLoadDetails([], [])

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

            controll_traffic = TRexTestRunner(cli=self._cli,
                                              trex_client=self._trex_client,
                                              resource_config=resource_config,
                                              logger=logger)

            controll_traffic.load_test_config(test_config_url=config_file_url)

        logger.info("Load test configuration file command ended")

    def start_traffic(self, context, test_file_name, blocking, timeout):
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

            controll_traffic.start_traffic(test_config=test_file_name,
                                           block_to_success=blocking,
                                           timeout=float(timeout))

        logger.info("Start traffic command ended")

    def stop_traffic(self, context, force):
        """ Stop traffic and unreserving ports """

        logger = get_logger_with_thread_id(context)
        logger.info("Stop traffic command started")

        with ErrorHandlingContext(logger):
            cs_api = get_api(context)
            resource_config = TrafficGeneratorControllerResource.create_from_chassis_resource(context=context,
                                                                                              cs_api=cs_api)

            controll_traffic = TRexTestRunner(cli=self._cli,
                                              trex_client=self._trex_client,
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
            controll_traffic = TRexTestRunner(cli=self._cli,
                                              trex_client=self._trex_client,
                                              resource_config=resource_config,
                                              logger=logger)

            res = controll_traffic.get_results()

            logger.info("Get results command ended")
            return res

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


if __name__ == "__main__":
    import mock
    import time
    from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails
    from cloudshell.api.cloudshell_api import CloudShellAPISession

    address = '192.168.65.78'
    # address = '192.168.65.143'

    user = 'root'
    password = 'Password1'
    auth_key = 'h8WRxvHoWkmH8rLQz+Z/pg=='
    api_port = 8029

    context = ResourceCommandContext()
    context.resource = ResourceContextDetails()
    context.resource.name = 'TRex'
    context.resource.fullname = 'Cisco TRex'
    context.reservation = ReservationContextDetails()
    # context.reservation.reservation_id = 'feb2e0a3-0779-4719-a336-5379671b445b'
    context.reservation.reservation_id = '7b9ca795-be63-4a0a-9418-2a6957291a39'
    context.resource.attributes = {}
    context.resource.attributes['User'] = user
    context.resource.attributes['Password'] = password
    context.resource.attributes["CLI TCP Port"] = 22
    context.resource.attributes["CLI Connection Type"] = "ssh"
    context.resource.attributes["Sessions Concurrency Limit"] = 1
    context.resource.attributes["Test Files Location"] = "D:\\"
    context.resource.address = address

    context.connectivity = mock.MagicMock()
    context.connectivity.server_address = "192.168.85.17"

    dr = TRexControllerDriver()

    api = session = CloudShellAPISession("192.168.85.17", "admin", "admin", "Global", port=8029)

    with mock.patch('__main__.get_api') as get_api:
        # get_api.return_value = type('api', (object,), {
        #     'DecryptPassword': lambda self, pw: type('Password', (object,), {'Value': pw})()})()

        get_api.return_value = api
        dr.initialize(context)
        # dr.load_test_config(context=context, config_file_url="extend_command.py")
        # dr.load_test_config(context=context, config_file_url="ftp://quali:Password1@192.168.85.17/test_config/sfr_delay_10_1g.yaml")
        # print dr.get_results(context=context)
        # dr.start_traffic(context=context, test_file_name="sfr_delay_10_1g.yaml", blocking="True", timeout="2")

        # time.sleep(40)

        dr.stop_traffic(context=context, force="False")
        # print dr.get_results(context=context)
    #
    #     # out = dr.get_inventory(context)
    #     #
    #     # for xx in out.resources:
    #     #     print xx.__dict__
    #
    #     out = dr.load_config(context, "TestConfig.xml")
    #
    #     print(out)

    # with mock.patch('__main__.get_api') as get_api:
    #     get_api.return_value = type('api', (object,), {
    #         'DecryptPassword': lambda self, pw: type('Password', (object,), {'Value': pw})()})()

    # out = dr.get_inventory(context)
    #
    # for xx in out.resources:
    #     print xx.__dict__

    # out = dr.load_config(context, "CS_TEST.xml")
    # out = dr.start_traffic(context)
    # out = dr.stop_traffic(context)
    # out = dr.get_results(context)
    # out = dr.cleanup_reservation(context)

    # print(out)
