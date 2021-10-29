# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser

from rbts_mts_visualize_pool.rbts_mts_visualize_poolImpl import rbts_mts_visualize_pool
from rbts_mts_visualize_pool.rbts_mts_visualize_poolServer import MethodContext
from rbts_mts_visualize_pool.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace


class rbts_mts_visualize_poolTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('rbts_mts_visualize_pool'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'rbts_mts_visualize_pool',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = rbts_mts_visualize_pool(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_rbts_mts_visualize_pool_server" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods

        
        genome_ref = "63063/3/1"
        mutantpool_ref = "63063/38/1"

        test_params = {
                "workspace_name": self.wsName,
                "genome_ref": genome_ref,
                "mutantpool_ref": mutantpool_ref
                }

        ret = self.serviceImpl.run_rbts_mts_visualize_pool(self.ctx, test_params)

        #self.assertEqual
