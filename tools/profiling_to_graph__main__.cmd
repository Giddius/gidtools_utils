@rem taskarg: ${file}
@Echo off
set OLDHOME_FOLDER=%~dp0
pushd %OLDHOME_FOLDER%
call ..\.venv\Scripts\activate.bat
call profiling_to_graph.cmd D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidtools_utils\gidtools\gidconfig\experimental.py
