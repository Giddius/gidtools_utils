import os


FILE = r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\PyQt_Socius\tools\create_venv.cmd"

with open(FILE, 'r') as cvf:
    _content = cvf.read()

with open(FILE, 'w') as ncvf:
    for line in _content.splitlines():
        if 'call pip' in line:
            _std, _name = line.rsplit(' ', 1)
            line = _std + ' --upgrade --pre ' + _name
        ncvf.write(line + '\n')
