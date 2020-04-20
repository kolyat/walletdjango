import logging


LOG_OPTIONS = {
    'filemode': 'a',
    'format': '%(asctime)s [%(module)33s] %(levelname)7s - %(funcName)s'
              ' - %(message)s',
    'level': logging.INFO
}
