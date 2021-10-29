/*
A KBase module: rbts_mts_visualize_pool
*/

module rbts_mts_visualize_pool {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_rbts_mts_visualize_pool(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

};
