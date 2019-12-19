#!E:\PyCharm\Flask_MQTT\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'mqtt==0.0.1','console_scripts','frps.py'
__requires__ = 'mqtt==0.0.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('mqtt==0.0.1', 'console_scripts', 'frps.py')()
    )
