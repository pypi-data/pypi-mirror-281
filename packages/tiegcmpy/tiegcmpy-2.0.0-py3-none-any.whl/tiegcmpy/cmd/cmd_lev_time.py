#!/usr/bin/env python3
from ..plot_gen import plt_lev_time
from ..io import load_datasets, save_output
import argparse

def cmd_parser():
    parser = argparse.ArgumentParser(description="Main parser")
    subparsers = parser.add_subparsers()

    args_load_datasets = subparsers.add_parser('load', help='Load datasets from a directory')
    args_load_datasets.add_argument('-dir','--directory', type=str, help='Path to the directory containing the datasets')
    args_load_datasets.add_argument('-dsf','--dataset_filter', type=str, help='Filter for the dataset file names', default=None)
    
    args_save_output= subparsers.add_parser('save', help='Save plot to a directroy')
    args_save_output.add_argument('-o_dir','--output_directory', type=str, required=True, help='Directory where the plot will be saved.')
    args_save_output.add_argument('-o_file','--filename', type=str, required=True, help='Filename for the saved plot.')
    args_save_output.add_argument('-o_format','--output_format', type=str, required=True, help='Format of the output plot, e.g., "png", "pdf".')

    args_plot= subparsers.add_parser('plot', help='Plotting parameters')
    args_plot.add_argument('-var','--variable_name', type=str, help="The name of the variable with latitude, longitude, time, and ilev dimensions.")
    args_plot.add_argument('-lat','--latitude', type=float, help="The specific latitude value for the plot.")
    args_plot.add_argument('-lon','--longitude', type=float, help="The specific longitude value for the plot.", default=None)
    args_plot.add_argument('--localtime', type=float, help="The specific local time value for the plot.", default=None)
    args_plot.add_argument('-unit','--variable_unit', type=str, help="The desired unit of the variable.", default=None)
    args_plot.add_argument('-ci','--contour_intervals', type=int, help="The number of contour intervals. Defaults to 10.", default=10)
    args_plot.add_argument('-cv','--contour_value', type=int, help="The value between each contour interval.", default=None)
    args_plot.add_argument('-si','--symmetric_interval', action='store_true', help="If True, the contour intervals will be symmetric around zero. Defaults to False.")
    args_plot.add_argument('-cmc','--cmap_color', type=str, help="The color map of the contour. Defaults to 'viridis' for Density, 'inferno' for Temp, 'bwr' for Wind, 'viridis' for undefined.", default=None)
    args_plot.add_argument('-lc','--line_color', type=str, help="The color for all lines in the plot. Defaults to 'white'.", default='white')
    args_plot.add_argument('-lvl_min','--level_minimum', type=float, help="Minimum level value for the plot. Defaults to None.", default=None)
    args_plot.add_argument('-lvl_max','--level_maximum', type=float, help="Maximum level value for the plot. Defaults to None.", default=None)
    args_plot.add_argument('--mtime_minimum', type=float, help="Minimum time value for the plot. Defaults to None.", default=None)
    args_plot.add_argument('--mtime_maximum', type=float, help="Maximum time value for the plot. Defaults to None.", default=None)
    return (parser)




def cmd_plt_lev_time():
    parser = cmd_parser()
    args = parser.parse_args()
    datasets = load_datasets(args.directory,args.dataset_filter)
    plot = plt_lev_time(datasets, variable_name=args.variable_name, latitude=args.latitude, longitude=args.longitude, localtime=args.localtime, variable_unit=args.variable_unit, contour_intervals=args.contour_intervals, contour_value=args.contour_value, symmetric_interval=args.symmetric_interval, cmap_color=args.cmap_color, line_color=args.line_color, level_minimum=args.level_minimum, level_maximum=args.level_maximum, mtime_minimum=args.mtime_minimum, mtime_maximum=args.mtime_maximum)
    save_output(args.output_directory,args.filename,args.output_format,plot)


