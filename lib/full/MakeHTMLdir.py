#!python3

import os
import sys
import logging
import json
import random
import string
import copy
import shutil
import subprocess
#from HTMLReport import CreateHTMLdir
from full.GeneTableGenomePoolFileToScfPosBC import GeneTable_Barcodes_To_BarcodeGenes
from full.ScfPosBC_To_BarChartData import ScfPosBC_Info_To_Scaffolds
from full.ScfPosBC_to_MhtnData import PosScfBCDataToZScrPointsForValues
from full.PoolStats import RunPoolStatsPy


"""
We want to copy HTML dir to the "op dir" destination

"""

def CreateCompleteHTML_dir(genome_fna_fp, genes_table_fp, poolfile_fp, op_dir, 
                           genome_name, tmp_dir, HTML_dir):
    """
    Args:
        op_dir (str): The path to which the new HTML dir will be moved/created.
    """

    if not os.path.exists(HTML_dir):
        raise Exception(f"HTML_dir doesn't exist at {HTML_dir}.")

    if not os.path.exists(op_dir):
        shutil.copytree(HTML_dir, op_dir)
    else:
        raise Exception("Output directory already exists. Please choose new destination")

    if not os.path.exists(tmp_dir):
        raise Exception(f"tmp dir doesn't exist at {tmp_dir}.")
    """
    else:
        if len(os.listdir("tmp")) > 0:
            raise Exception("Please reserve tmp dir for work")
    """

    # Getting PoolStats
    success_bool, stats_d = RunPoolStatsPy(poolfile_fp, genes_table_fp, nTotalReads=None)

    if not success_bool:
        pool_stats_d = {"failed": True}
    else:
        pool_stats_d = stats_d
        pool_stats_d["failed"] = False

    with open(os.path.join(op_dir, "JS", "StatsDisplay", "PoolStats.js"), "w" ) as g:
        g.write("window.pool_stats_d = " + json.dumps(pool_stats_d, indent=2))
    '''
    R_op = RunPoolStatsR(poolfile_fp, genes_table_fp)
    R_log_d = RlogToDict(R_op)
    R_log_d["genome_name"] = genome_name

    '''

    scfPosBC_fp = os.path.join(tmp_dir,"ScfPosBC.json")

    GeneTable_Barcodes_To_BarcodeGenes(
            genes_table_fp,
            poolfile_fp,
            genome_fna_fp,
            scfPosBC_fp,
            genome_name,
            "Default"
            )



    # Expanding Bar Chart Data
    EBC_data_dir = os.path.join(op_dir, "JS","EBC","DATA")

    ScfPosBC_Info_To_Scaffolds(scfPosBC_fp, 
                                10, 
                                genes_table_fp,
                                genome_fna_fp,
                                EBC_data_dir
                                )
    
    # We move a specific file to the right loc
    shutil.move(os.path.join(EBC_data_dir,"EBC_Scaffolds_Init_Data.js"), 
               os.path.join(op_dir, "JS","EBC"))


    #MH Plot Data
    MH_dir = os.path.join(op_dir, "JS","MH")
    MH_data_fp = os.path.join(MH_dir, "MH_Data.js")
    PosScfBCDataToZScrPointsForValues(scfPosBC_fp, MH_data_fp, "0")

    logging.info("finished creating files at " + op_dir)

    
    #os.system("open " + os.path.join(op_dir, "FullDisplay_index.html"))
    


def RunPoolStatsR(poolfile_fp, genes_table_fp):
    """
    inp_d: (dict) contains
        R_fp (str) Path to R script 'PoolStats.R'
        output_fp (str) (pool_fp) finished pool file
        genes_table_fp (str) genes table file path
        nMapped (int) 
        R_op_fp: (str) Path to R log
        tmp_dir: (str) Path to tmp_dir
    """

    # getting nMapped (length of poolfile -1)
    pf_FH = open(poolfile_fp)
    c_line = pf_FH.readline() # we don't count header line
    nMapped = 0
    while c_line != "":
        nMapped += 1
        c_line = pf_FH.readline() 

    RCmds = ["Rscript", 
            "PoolStats.R", 
            poolfile_fp,
            genes_table_fp,
            str(nMapped)]


    logging.info("Running R PoolStats")

    R_op = os.path.join("tmp", "PoolStatsOutput.txt")
    std_op = os.path.join("tmp", "R_STD_OP.txt")
    with open(R_op, "w") as f:
        with open(std_op, "w") as g:
            subprocess.call(RCmds, stderr=f, stdout=g)

    if os.path.exists(R_op):
        logging.info("Succesfully ran R, log found at " + R_op)

    return R_op



def RlogToDict(R_log_fp):
    """
    Inputs:
        R_log_fp: (str)
    Outputs:
        res_d: (dict) 'results dict'
            failed: (bool) True if failed.
            [Error_str]: exists if failed=True
            insertions: (int)
            diff_loc: (int)
            nPrtn_cntrl: (int)
            cntrl_ins: (int)
            cntrl_distinct: (int)
            num_surp: (int) # number surprising insertions
            stn_per_prtn_median: (int)
            stn_per_prtn_mean: (float)
            gene_trspsn_same_prcnt: (float)
            reads_per_prtn_median: (int)
            reads_per_prtn_mean: (float)
            reads_per_mil_prtn_median: (float)
            reads_per_mil_prtn_mean: (float)
    """
    with open(R_log_fp, "r") as f:
        rlog_str = f.read()

    res_d = {"failed": False}

    rlog_l = rlog_str.split("\n")

    if rlog_str == '':
        res_d["failed"] = True
        res_d['Error_str'] = 'PoolStats failed to create any results at ' + R_log_fp

        return res_d
    elif len(rlog_l) < 11:
        res_d["failed"] = True
        res_d["Error_str"] = 'PoolStats output does not have 11 lines as expected:\n"' + rlog_str
        return res_d

    res_d['insertions'] = int(rlog_l[0].split(' ')[0])
    res_d['diff_loc'] = int(rlog_l[0].split(' ')[6])
    res_d['cntrl_ins'] = int(rlog_l[1].split(' ')[1])
    res_d['cntrl_distinct'] = int(rlog_l[1].split(' ')[3][1:])
    res_d['nPrtn_cntrl'] = int(rlog_l[2].split(' ')[4])
    res_d["num_surp"] = int(rlog_l[5].split(' ')[1])
    res_d['stn_per_prtn_median'] = int(rlog_l[7].split(' ')[5])
    res_d['stn_per_prtn_mean'] = float(rlog_l[7].split(' ')[-1])
    res_d['gene_trspsn_same_prcnt'] = float(rlog_l[8].split(' ')[-1][:-1])
    res_d['reads_per_prtn_median'] = int(rlog_l[9].split(' ')[5])
    res_d['reads_per_prtn_mean'] = float(rlog_l[9].split(' ')[7])

    return res_d


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def test():
    logging.basicConfig(level=logging.DEBUG)
    # Program should be run FullProgram.py map_cfg.json drp_cfg.json tmp_dir output_fp
    args = sys.argv
    if args[-1] != "1":
        print("Program should be run python3 MakeHTMLdir.py genome_fna_fp genes_table_fp poolfile_fp op_dir genome_name 1")
        sys.exit(os.EX_OK)
    genome_fna_fp = args[1]  
    genes_table_fp = args[2]  
    poolfile_fp = args[3] 
    op_dir = args[4]
    genome_name = args[5]

    CreateCompleteHTML_dir(genome_fna_fp, genes_table_fp, poolfile_fp, op_dir, genome_name)





def main():
    test()

    return None

if __name__ == "__main__":
    main()
