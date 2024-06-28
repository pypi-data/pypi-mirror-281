# from typing import Optional
# import os
# import bindfiles.filesync.settings as settings
# from filesync.interface import FileWidget
# from filesync.engine import FileApp
# __all__ = ['FileWidget']


#settings.PROJ__NAME_ = __name__
#from filesync.cproj import block_build








# def local_drive(path:str, id_folder: str, cred : str) -> None:
#     fapp = FileApp()
#     fapp.pa.local(path)
#     fapp.pb.gdrive(id=id_folder, cred = cred)

#     settings.RUNNING_DATA[fapp.INST] = fapp


# def local_local(path_left:str, path_right:str, *,  exclude_folder : list[str] = [] ) -> None:
#     fapp = FileApp()
#     fapp.pa.local(path_left)
#     fapp.pb.local(path_right)
#     if exclude_folder:
#         fapp.opt['exclude_folder'] = exclude_folder

#     settings.RUNNING_DATA[fapp.INST] = fapp








