
# -*- coding: utf-8 -*-

import sys
import argparse
import shutil

from controllers.M3uManagement import M3uManagement


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
    args = parser.parse_args()

    m3u_url = args.m3u_file
    output_path = args.output_dir
    provider = args.provider
    generate_groups = args.generate_groups
    
    if not m3u_url or not output_path or not provider:
        parser.print_help()
        sys.exit(1)

    if not output_path.endswith("/"):
        output_path += "/"

    if output_path[-1] == '/':
        output_path = output_path[:-1]  

    output_path = os.path.join(output_path, provider)

    m3u_manager = M3uManagement(in_provider=provider, in_generate_groups=generate_groups, in_m3u_url=m3u_url)
    m3u_manager.parse(output_path)

    #shutil.copy(playlistPath, f'.local/{provider}/current_playlist.m3u')

    print("Finished parsing m3u playlist")
    print(f" - {m3u_manager.num_titles_skipped} titles skipped")
    print(f" - {m3u_manager.num_new_movies} new movies were added")
    print(f" - {m3u_manager.num_new_series} new tv show episodes were added")
    print(f" - {m3u_manager.num_errors} errors writing strm file")
    print(f" - {m3u_manager.num_not_in_moviedatabase} Not in movie database search")
    
          
