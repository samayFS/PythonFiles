import logging

# logging.basicConfig(filename='HelloApp.log',filemode='w',format='%(process)d-%(name)s-%(levelname)s-%(message)s')
# logging.warning('File Got logged')
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

# Test messages
logger.debug("Harmless debug Message")
logger.info("Just an information")
logger.warning('GET WARNING')

#
# FORMAT = '%(asctime)-15s--%(clientip)s--%(user)-8s--%(message)s'
# logging.basicConfig(format=FORMAT)
# d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
# logger = logging.getLogger('tcpserver')
# logger.warning('Protocol problem: %s', 'connection reset', extra=d)