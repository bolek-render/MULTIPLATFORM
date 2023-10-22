# UNLOADED / UNFINISHED VIDS
# check on start if videos exist in folders
# if exist move to video error folder


import os
import shutil
import DATA.globals as cg


def move_videos():

    vids_src = f'{cg.PATH}{cg.SS}VIDS'
    err_folder = f'{cg.PATH}{cg.SS}ERROR'
    empty_folders = []
    files_found = []

    if os.path.isdir(vids_src):
        vids_folders = os.listdir(vids_src)
        for vids_folder in vids_folders:
            files = os.listdir(f'{vids_src}{cg.SS}{vids_folder}')
            if len(files) == 0:
                empty_folders.append(vids_folder)

        for vids_folder in vids_folders:
            if vids_folder not in empty_folders:
                src = f'{vids_src}{cg.SS}{vids_folder}'
                print(src)
                shutil.move(src, f'{err_folder}{cg.SS}{vids_folder}')

        print(empty_folders)




        # print(vids_folders)
