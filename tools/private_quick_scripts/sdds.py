

FILE = r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidtools_utils\requirements.txt"


with open(FILE, 'r') as cvf:
    _content = cvf.read()

with open(FILE, 'w') as ncvf:
    for line in _content.splitlines():
        if '==' in line:

            line = line.replace('==', '>=')
        ncvf.write(line + '\n')
