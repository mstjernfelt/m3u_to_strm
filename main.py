
# -*- coding: utf-8 -*-

import sys
import argparse
from controllers.M3uManagement import M3uManagement
from utils.PushoverManagement import Pushover

num_new_movies = 0
num_new_series = 0
share_user_name = ''
num_titles_skipped = 0
share_password = ''

if __name__ == '__main__':
    num_new_groups = 0
    
    parser = argparse.ArgumentParser(description='Converts an m3u file to STRM files for Kodi.')
    parser.add_argument('--m3u_file', type=str, help='Input m3u file (either a URL or a local path)')
    parser.add_argument('--output_dir', type=str, help='Output directory for STRM files')
    parser.add_argument('--provider', help='Spefifies your IPTV provider name')
    parser.add_argument('--generate_groups', action='store_true', help='Generate groups from VOD entries')
    parser.add_argument('--preview', action='store_true', help='Do not create files')
    parser.add_argument('--verbose', action='store_true', help='output to terminal')
    parser.add_argument('--cleanrun', action='store_true', help='remove playlist and start from scratch')
    args = parser.parse_args()

    m3u_url = args.m3u_file
    output_path = args.output_dir
    provider = args.provider
    generate_groups = args.generate_groups
    preview = args.preview
    verbose = args.verbose
    cleanrun = args.cleanrun

    if not m3u_url or not output_path or not provider:
        parser.print_help()
        sys.exit(1)

    if not output_path.endswith("/"):
        output_path += "/"

    if output_path[-1] == '/':
        output_path = output_path[:-1]  

    m3u_manager = M3uManagement(in_provider=provider, in_generate_groups=generate_groups, in_m3u_url=m3u_url, in_verbose = verbose, in_preview=preview, in_cleanrun=cleanrun)
    m3u_manager.parse(output_path)