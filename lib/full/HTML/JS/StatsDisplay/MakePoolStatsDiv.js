


 /* 
  * This file is intended to create a stats report within a larger div 
  *     as part of work on the MapTnSeq output display.
  *
  *
  *
  *
  */

function CreateStatsReportInDiv(parent_div_id, stats_data, stats_defaults) {
 /* 
  * Args:
  *     parent_div_id: (str) for now, 'entire-display-holder' (NOT IN USE)
  *     stats_data: (d) Main data used to populate display (StatsData.js)
  *     stats_defaults: (d) Main data used for design of display (StatsDefaults.js)
  */

    FillPoolStatsInDiv(parent_div_id, pool_stats_d, stats_defaults);

    /*
    CreateLayoutSkeleton(stats_defaults);
    FillTitleDiv(stats_defaults, stats_data);
    FillModelDivs(stats_defaults, stats_data);
    CreateFASTQTables(stats_defaults, stats_data);
    CreateDRPTable(stats_defaults, stats_data["DRP_report_dict"]);
    */



}

function FillPoolStatsInDiv(parent_div_id, pool_stats_d, stats_defaults) {
 /* 
  * pool_stats_d: (object)
  *     
  * e.g
        "failed": false,
        "insertions": 222617,
        "diff_loc": 67557,
        "cntrl_ins": 134405,
        "cntrl_distinct": 40301,
        "nPrtn_cntrl": 4089,
        "num_surp": 25,
        "stn_per_prtn_median": 20,
        "stn_per_prtn_mean": 32.4,
        "gene_trspsn_same_prcnt": 51.3,
        "reads_per_prtn_median": 682,
        "reads_per_prtn_mean": 1129.0
  *
  */
    let main_display_dobj = document.getElementById(parent_div_id);
    SpecialCreationofDRPTable(pool_stats_d, main_display_dobj, stats_defaults);
    

}

function SpecialCreationofDRPTable(rl, main_display_dobj, stats_defaults) {
    /*
     * rl is pool_stats_d which has the following keys:
     *
     *          'failed': bool
     *          if failed is false:
                'nNonPastEnd', 'nUnique_Insertions', 'nSeenMoreThanOnce', 
                'nSeenExactlyTwice', 'nMedian_strains_per_gene', 'fMean_strains_per_gene', 
                'nMedian_reads_per_gene', 'fMean_reads_per_gene', 
                'fBias_reads_per_gene', 'prcnt_gene_and_transposon_ratio_same_strand', 
                'nCentralInsertions',  'nUniqueCentralInsertions', 
                'nGenesWithInsertions', 'nGenesWithCentralInsertions', 'nGenes',
                'nEssentialGenes', 'nNotEssentialGenes', 'nEssentialGenesHit', 
                'nNotEssentialGenesHit', 'fEssentialGenesHitRatio', 
                'fNonEssentialGenesHitRatio'
     *
     *
     */




    if (rl["failed"]) {
        main_display_dobj.innerHTML = "'PoolStatsPy' failed to run properly"

    } else {

        // We prepare the rows of text for the table
        let table_list = [
                ['# Protein-Coding Genes with Central Insertion(s): ', prepInt(rl['nGenesWithCentralInsertions']) ],
                ['# Central Insertions in Protein Coding Genes: ', prepInt(rl['nCentralInsertions'])],
                ['# Putatively Essential Genes with Insertions: ', prepInt(rl['nEssentialGenesHit'])],
                ['Reads per Protein: Mean ', rl['fMean_reads_per_gene']],
                ['Reads per Protein: Median ', prepInt(rl['nMedian_reads_per_gene'])],
                ['Reads per Protein: Bias (mean/median)',
                    (rl['fBias_reads_per_gene']).toString().slice(0,5) ],
                ['% Of Insertions in Protein-Coding Genes on the Coding Strand: ', 
                    (rl['prcnt_gene_and_transposon_ratio_same_strand']).toString().slice(0,5) + "%"]
        ];

        let tbl = document.createElement("TABLE");

        main_display_dobj.appendChild(tbl);
        
        LUAddStyleToDOMObj(tbl, stats_defaults["text_display"][
                                                "table_style"])


        // First we create the name of the organism
        let title_row = tbl.insertRow(-1);
        let title_cell = title_row.insertCell(0);
        title_cell.innerHTML = "Genome: " + rl["genome_name"];
        
        LUAddStyleToDOMObj(title_row, stats_defaults["text_display"][
                                                "row_styles"][
                                                "title_cell"]);


        for (let j=0; j<table_list.length; j++) {
        
            let row = tbl.insertRow(-1);

            let cell1 = row.insertCell(0);
            let cell2 = row.insertCell(1);

            LUAddStyleToDOMObj(cell1, stats_defaults["text_display"][
                                                "row_styles"][
                                                "basic_row"])

            LUAddStyleToDOMObj(cell2, stats_defaults["text_display"][
                                                "row_styles"][
                                                "basic_row"])
            cell1.innerHTML = table_list[j][0];
            cell2.innerHTML = table_list[j][1];

        }
    }

}


function FillTitleDiv(stats_defaults, stats_data) {

    document.getElementById(stats_defaults["lyt_vls"][
                                            "genome_title_div"][
                                            "id_i"]["id"]).innerHTML = stats_data["genome_name"]


}

function FillModelDivs(stats_defaults, stats_data) {
 /*
  * We add the text to the Model Divs from the Data
  *
  *
  *
  */
   let model_name_dobj =  document.getElementById(stats_defaults["lyt_vls"][
                                                    "model_name_content_div"][
                                                    "id_i"][
                                                    "id"]);

   let model_seq_dobj =  document.getElementById(stats_defaults["lyt_vls"][
                                                    "model_sequence_content_div"][
                                                    "id_i"][
                                                    "id"]);

   model_name_dobj.innerHTML = stats_data["models_info"]["model_name"];
   model_seq_dobj.innerHTML = stats_data["models_info"]["model_str"];



}




function CreateDRPTable(stats_defaults, inp_d) {
    /*
    input is dict with the following keys:

       nUsableBarcodes: (int)
       total_MTS_table_lines: (int)
       nMapped: (int)
       nReadsForUsable: (int) This is the total number of reads that were used for barcodes
       Rlog_d : (dict) 'results dict'
            failed: (bool) True if failed.
            [Error_str]: existant if failed=True
            insertions: (int)
            diff_loc: (int)
            cntrl_ins: (int)
            cntrl_distinct: (int)
            nPrtn_cntrl: (int)
            num_surp: (int) # number surprising insertions
            stn_per_prtn_median: (int)
            stn_per_prtn_mean: (float)
            gene_trspsn_same_prcnt: (float) Strand Bias?
            reads_per_prtn_median: (int)
            reads_per_prtn_mean: (float)
            reads_per_mil_prtn_median: (float)
            reads_per_mil_prtn_mean: (float)
            
  * Note: We import the functions FracToPrcString & prepInt from LayoutUtil
    */

    let pool_report_table_dobj = document.getElementById(stats_defaults["lyt_vls"][
                                                "pool_report_table_div"]["id_i"]["id"]);

    let rl = inp_d["Rlog_d"];


    if (rl["failed"]) {
        pool_report_table_dobj.innerHTML = "'Design Random Pool' failed to run properly"

    } else {

        // We prepare the rows of text for the table
        let table_list = [
                ['# Usable Barcodes: ', prepInt(inp_d['nUsableBarcodes'])],
                ['% Coverage of mapped reads by usable barcodes: ', 
                    FracToPrcString(inp_d['nReadsForUsable']/(inp_d['nMapped'] + 10**-6)) + "%" ],
                ['# Protein-Coding Genes with Central Insertion(s): ', prepInt(rl['nPrtn_cntrl']) ],
                ['# Central Insertions in Protein Coding Genes: ', prepInt(rl['cntrl_ins'])],
                ['# Putatively Essential Genes with Insertions: ', prepInt(rl['num_surp'])],
                ['Reads per Protein: Mean ', rl['reads_per_prtn_mean']],
                ['Reads per Protein: Median ', prepInt(rl['reads_per_prtn_median'])],
                ['Reads per Protein: Bias (mean/median)',
                    (rl['reads_per_prtn_mean']/rl['reads_per_prtn_median']).toString().slice(0,5) ],
                ['% Of Insertions in Protein-Coding Genes on the Coding Strand: ', 
                    (rl['gene_trspsn_same_prcnt']).toString().slice(0,5) + "%"]
        ];

        let tbl = document.createElement("TABLE");

        pool_report_table_dobj.appendChild(tbl);
        
        LUAddStyleToDOMObj(tbl, stats_defaults["text_display"][
                                                "table_style"])


        for (let j=0; j<table_list.length; j++) {
        
            let row = tbl.insertRow(-1);

            let cell1 = row.insertCell(0);
            let cell2 = row.insertCell(1);

            LUAddStyleToDOMObj(cell1, stats_defaults["text_display"][
                                                "row_styles"][
                                                "basic_row"])

            LUAddStyleToDOMObj(cell2, stats_defaults["text_display"][
                                                "row_styles"][
                                                "basic_row"])
            cell1.innerHTML = table_list[j][0];
            cell2.innerHTML = table_list[j][1];

        }
    }

}

    /*
    HTML_l = ["<h2>Mutant Pool Report</h2>"]

    HTML_l += ['<div id="DRP_table" class="rpt_tbl_div">']
    
    css_tbl_cls = "dataTable__table table table-striped table-bordered dataTable no-footer"
    HTML_l += ['<table class="{}">'.format(css_tbl_cls)]

    if rl["failed"]:
        for info in [
                ['# Usable Barcodes ', prep_int(rd['nUsableBarcodes'])],
                ['% Coverage of mapped reads by usable barcodes', 
                    Prc(float(rd['nReadsForUsable'])/(float(rd['nMapped']) + 10**-6)) + "%" ]
                ]:
            html_str = '<tr role="row" class="DRP_row">\n' \
                    + '<td class="DRP_col_1">' + info[0] + '</td>\n' \
                    + '<td class="DRP_col_2">' + str(info[1]) + '</td>\n' \
                    + '</tr>'
            HTML_l.append(html_str)
    else:
        for info in [
                ['# Usable Barcodes ', prep_int(rd['nUsableBarcodes'])],
                ['% Coverage of mapped reads by usable barcodes', 
                    Prc(float(rd['nReadsForUsable'])/(float(rd['nMapped']) + 10**-6)) + "%" ],
                ['# Protein-Coding Genes with Central Insertion(s)', prep_int(rl['nPrtn_cntrl']) ],
                ['# Central Insertions in Protein Coding Genes ', prep_int(rl['cntrl_ins'])],
                ['# Putatively Essential Genes with Insertions', prep_int(rl['num_surp'])],
                ['Reads per Protein: Mean ', rl['reads_per_prtn_mean']],
                ['Reads per Protein: Median', prep_int(rl['reads_per_prtn_median'])],
                ['Reads per Protein: Bias (mean/median)',
                    str(round(float(rl['reads_per_prtn_mean'])/float(rl['reads_per_prtn_median']), 3)) ],
                ['% Of Insertions in Protein-Coding Genes on the Coding Strand', 
                    str(round(rl['gene_trspsn_same_prcnt'],3)) + "%"]
                ]:
            html_str = '<tr role="row" class="DRP_row">\n' \
                    + '<td class="DRP_col_1">' + info[0] + '</td>\n' \
                    + '<td class="DRP_col_2">' + str(info[1]) + '</td>\n' \
                    + '</tr>'
            HTML_l.append(html_str)

    HTML_l.append('</table>\n')
    HTML_l.append("</div>\n")

    return "\n".join(HTML_l)
    */



function CreateLayoutSkeleton(stats_defaults) {

    let stats_dom_lyts = Object.keys(stats_defaults["lyt_vls"]);
   
    for (let i = 0; i < stats_dom_lyts.length; i++) {

        LUCreateElementFromInfo(stats_defaults["lyt_vls"][stats_dom_lyts[i]]);

    }

}


function CreateFASTQTables(stats_defaults, stats_data) {

 /*
  * stats_data: (obj)
  *     "MapTnSeq_reports_list": trd (obj)
  *         trd: Described in function "AddFASTQTable"
  *             
  *
  *
  */

   let fq_reads_table_div = document.getElementById(
                                stats_defaults["lyt_vls"][
                                                "fastq_reads_table_div"][
                                                "id_i"][
                                                "id"]);
    
    let trd_list = stats_data["MapTnSeq_reports_list"];

    for (let i = 0; i < trd_list.length; i++) {
        
        AddFASTQTable(stats_defaults, trd_list[i]["text_report_dict"], fq_reads_table_div);

    }



}


function AddFASTQTable(stats_defaults, trd, fq_tbl_div) {
 /*
  * Args:
  *     trd:
            fastq_fn: (str)
            R_proc: int (reads processed)
            long_enough: (int)
            minRlen: (int) (minimum Read Length)
            tot_BC: (int)
            nTryToMap: (int)
            nMapped: (int)
            Uniquely_Mapped: (int)
            total_hits_pastEnd: (int)
            Hits_pE: (int) Total hits past End - nPastEndIgnored
            nPastEndIgnored: (int)
            nPastEndTrumps: (int)

 * fq_tbl_div: Div containing all the table columns

  *
  * Note: We import the functions FracToPrcString & prepInt from LayoutUtil
  * 
  */

    // Note: Differentiate between title row and content row.

   // We create title row:
   // Note we also need to create table object (?)


    console.log(trd);

    let tbl = document.createElement("TABLE");

    
    LUAddStyleToDOMObj(tbl, stats_defaults["text_display"][
                                                "table_style"])

    // We create the title row
    let row = tbl.insertRow(-1);
    let title_cell = row.insertCell(0);

    LUAddStyleToDOMObj(row, stats_defaults["text_display"][
                                                "row_styles"][
                                                "title_cell"])

    title_cell.innerHTML = "Processing FASTQ file: " + trd["fastq_fn"];

    let r = trd["R_proc"];
    console.log(r);

    let table_list = [
            ['# Reads Processed: ', prepInt(r)],
            ['# Reads that are longer than ' + prepInt(trd['minRlen']) + "bp: ", prepInt(trd['long_enough'])],
            ['# Reads with Barcode: ', prepInt(trd['tot_BC'])],
            ['# Reads with Mapped Insertions: ', prepInt(trd['nMapped'])],
            ['# Reads that Map Uniquely: ', prepInt(trd['Uniquely_Mapped'])],
            ['# Reads that Map to Intact Vector', prepInt(trd['total_hits_pastEnd'])],
            ['% Reads that are longer than ' +  prepInt(trd['minRlen']) + "bp: ", FracToPrcString(trd['long_enough']/r) + "%"],
            ['% Reads with Barcode: ', FracToPrcString(trd['tot_BC']/r) + "%"],
            ['% Reads with Mapped Insertions: ', FracToPrcString(trd['nMapped']/r) + "%"],
            ['% Reads that Map Uniquely: ', FracToPrcString(trd['Uniquely_Mapped']/r) + "%"],
            ['% Reads that Map to Intact Vector: ', FracToPrcString(trd['total_hits_pastEnd']/r) + "%"]
    ]

    for (let j=0; j<table_list.length; j++) {
        
            let row = tbl.insertRow(-1);



            let cell1 = row.insertCell(0);
            let cell2 = row.insertCell(1);

            LUAddStyleToDOMObj(cell1, stats_defaults["text_display"][
                                                "row_styles"][
                                                "basic_row"])

            LUAddStyleToDOMObj(cell2, stats_defaults["text_display"][
                                                "row_styles"][
                                                "basic_row"])
            cell1.innerHTML = table_list[j][0];
            cell2.innerHTML = table_list[j][1];


            
    }



    fq_tbl_div.appendChild(tbl)

    // At the end


    /*

    // We iterate through each scaffold, giving it an entry in the table
    for (let r = sc_l.length-1; r >= 0; r--) {

            // Create an empty <tr> element and add it to the last position of the table:
            let row = tbl.insertRow(-1);

            row.style.border = "1px solid black";
            
            // Insert new cells (<td> elements) at the 1st and 2nd position of the "new" 
            // <tr> element:
            let cell1 = row.insertCell(0);
            let cell2 = row.insertCell(1);
            let cell3 = row.insertCell(2);
            
            // Add scaffold name and then scaffold length
            
            // First the ranking of scaffold in terms of length
            cell1.innerHTML = (r + 1).toString();
            // Then the scaffold name and link
            let scf_name = sc_l[r][0];
            console.log(scf_name);
            let scf_link = document.createElement("a");
            scf_link.innerHTML = scf_name;
            scf_link.style.cursor = "pointer";
            scf_link.style.textDecoration = "underline";
            scf_link.style.color = scf_to_color_obj[scf_name];
            // Here is where we set the on click function to open up that single scaffold's graph
            scf_link.onclick = function() {
                MakeSingleScaffoldGraph(scf_name, MH_data, scf_to_color_obj, sc_l, max_z )
            }
            scf_link.id = ScaffoldNameToValidHTMLID(scf_name) + "-link";
            cell2.appendChild(scf_link);
            cell3.innerHTML = prep_int(sc_l[r][1]) + " bp";
        }

    */




        


}




