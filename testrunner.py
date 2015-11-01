#!/usr/bin/python
import unittest
import sys
import os

GCLOUD_SDK_HOME = os.environ.get('GCLOUD_SDK_HOME')


def main():
    sys.path.insert(0, GCLOUD_SDK_HOME)

    import dev_appserver
    dev_appserver.fix_sys_path()

    suite = unittest.loader.TestLoader().discover('apps')
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    exit_code = 0 if result.wasSuccessful() else 1
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
