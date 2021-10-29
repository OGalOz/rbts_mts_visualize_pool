# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.GenomeFileUtilClient import GenomeFileUtil
from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.WorkspaceClient import Workspace
from installed_clients.rbts_genome_to_genetableClient import rbts_genome_to_genetable

from full.MakeHTMLdir import CreateCompleteHTML_dir
from util.PrepareIO import PrepareProgramInputs, PrepareUserOutputs, clear_dir
#END_HEADER


class rbts_mts_visualize_pool:
    '''
    Module Name:
    rbts_mts_visualize_pool

    Module Description:
    A KBase module: rbts_mts_visualize_pool
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        self.ws_url = config['workspace-url']
        #END_CONSTRUCTOR
        pass


    def run_rbts_mts_visualize_pool(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String

        Args:
            params (d) contains keys:
                'workspace_name' (str): ,
                'genome_ref' (str): ,
                "mutantpool_ref": pool_ref (str),

        Description:
            We download the genome and create a genes table and keep
            the genome FNA file.
            Then we use the pool file with the genes/genome to make visualization - 
            fitting it into whatever is needed by the JS files.
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_rbts_mts_visualize_pool

        if len(os.listdir(self.shared_folder)) > 0:
            logging.info("Clearing scratch directory")
            clear_dir(self.shared_folder)
        # Preparing main classes - dfu, gfu, genetableobj, workspace
        dfu = DataFileUtil(self.callback_url)
        gfu = GenomeFileUtil(self.callback_url)
        genetable_obj = rbts_genome_to_genetable(self.callback_url)
        # We need the workspace object to get info on the workspace the app is running in.
        token = os.environ.get('KB_AUTH_TOKEN', None)
        ws = Workspace(self.ws_url, token=token)
        ws_info = ws.get_workspace_info({'workspace': params['workspace_name']})
        workspace_id = ws_info[0]
        td = self.shared_folder
        op_dir = os.path.join(td, "op_HTML")
        HTML_dir = os.path.join("/kb/module/lib/full/HTML")

        cfg_d = {
                "gfu": gfu,
                "dfu": dfu,
                "ws": ws,
                "ws_id": workspace_id,
                "gt_obj": genetable_obj,
                "username" : ctx['user_id'],
                "tmp_dir": td,
                "gene_table_fp": os.path.join(td, "genes.GC")
        }


        #HERE
        res = PrepareProgramInputs(params, cfg_d)
        # unpacking results
        genome_fna_fp, genes_table_fp, poolfile_fp, genome_name = res


        CreateCompleteHTML_dir(genome_fna_fp, genes_table_fp, poolfile_fp, op_dir, 
                                genome_name, td, HTML_dir)


        report = KBaseReport(self.callback_url)
        report_info = report.create({'report': {'objects_created':[],
                                                'text_message': params['parameter_1']},
                                                'workspace_name': params['workspace_name']})
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
        }

        #END run_rbts_mts_visualize_pool

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_rbts_mts_visualize_pool return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
