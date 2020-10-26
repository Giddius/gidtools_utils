# region [Imports]

# * Gid Imports -->
import gidlogger as glog

# endregion [Imports]

__updated__ = '2020-10-14 14:39:11'

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]


# region [Functions_1]

def give_std_repr(in_instance, *args):
    # _arg_string = "', '".join(args)
    return f"{in_instance.__class__.__name__}{str(args)}"

# endregion [Functions_1]


# region [Main_Exec]

if __name__ == '__main__':
    pass

# endregion [Main_Exec]
