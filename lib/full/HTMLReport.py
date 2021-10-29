#!python3

# This file is a baseline python file

import os
import sys
import logging
import json
import shutil



def CreateHTMLdir(tmp_dir, html_display_files_dir):
    """
    We create the HTML directory in the tmp dir.
    We need to copy baseline files from html_display_files_dir to this directory
    This is where the information for the HTML directory is decided (no config)
    Args:
        both are paths to directories
    """
    html_dir = os.path.join(tmp_dir, "HTML")
    os.mkdir(html_dir)
    JS_dir = os.path.join(html_dir, "JS")
    os.mkdir(JS_dir)
    MH_dir = os.path.join(JS_dir, "MH")
    os.mkdir(MH_dir)
    EBC_dir = os.path.join(JS_dir, "EBC")
    os.mkdir(EBC_dir)
    stats_dir = os.path.join(JS_dir, "StatsDisplay")
    os.mkdir(stats_dir)

    shutil.copyfile(os.path.join(html_display_files_dir, "FullDisplay_index.html"),
        os.path.join(html_dir, "FullDisplay_index.html"))
    shutil.copyfile(os.path.join(html_display_files_dir, "FullDisplay_Defaults.js"),
        os.path.join(JS_dir, "FullDisplay_Defaults.js"))
    shutil.copyfile(os.path.join(html_display_files_dir, "FullDisplayFuncs.js"),
        os.path.join(JS_dir, "FullDisplayFuncs.js"))
    shutil.copyfile(os.path.join(html_display_files_dir, "LayoutUtil.js"),
        os.path.join(JS_dir, "LayoutUtil.js"))
    shutil.copyfile(os.path.join(html_display_files_dir, "d3-zoom.min.js"),
        os.path.join(JS_dir, "d3-zoom.min.js"))
    shutil.copyfile(os.path.join(html_display_files_dir, "d3.min.js"),
        os.path.join(JS_dir, "d3.min.js"))
    shutil.copyfile(os.path.join(html_display_files_dir, "BCExpandingBarChartFuncs.js"),
        os.path.join(EBC_dir, "BCExpandingBarChartFuncs.js"))
    shutil.copyfile(os.path.join(html_display_files_dir, "BCDefaults.js"),
        os.path.join(EBC_dir, "BCDefaults.js"))
    shutil.copyfile(os.path.join(html_display_files_dir, "MakeStatsDiv.js"),
        os.path.join(stats_dir, "MakeStatsDiv.js"))
    shutil.copyfile(os.path.join(html_display_files_dir, "StatsDefaults.js"),
        os.path.join(stats_dir, "StatsDefaults.js"))
    shutil.copyfile(os.path.join(html_display_files_dir, "MhtnDefaults.js"),
        os.path.join(MH_dir, "MhtnDefaults.js"))
    shutil.copyfile(os.path.join(html_display_files_dir, "MhtnPlotExpandFuncs.js"),
        os.path.join(MH_dir, "MhtnPlotExpandFuncs.js"))

    return [stats_dir, EBC_dir, MH_dir]
    



def main():
    
    args = sys.argv
    if args[1] == "how":
        print("python3 HTMLReport.py HTML_d.json op_fp.html")
        sys.exit(0)
    
    with open(args[1], "r") as f:
        html_d = json.loads(f.read())

    HTML_str = CreateHTMLString(html_d)

    with open(args[2], "w") as f:
        f.write(HTML_str)

    print("Wrote HTML file to " + args[2])



    return None

if __name__ == "__main__":
    main()
