# region [Imports]

# * Third Party Imports -->
import wmi

# endregion [Imports]

__updated__ = '2020-11-26 22:08:06'


# region [Functions_1]

def get_drives():
    _out = []
    c = wmi.WMI()
    for drive in c.Win32_LogicalDisk():
        _out.append(drive.Caption)
    return _out


# endregion [Functions_1]

# region [Main_Exec]

if __name__ == '__main__':
    pass


# endregion [Main_Exec]
