import logging
# lab = logging.getLogger("a.b")
# assert lab.parent == logging.root
# la = logging.getLogger("a")
# assert lab.parent == la
#
toto_logger = logging.getLogger("toto")

assert toto_logger.level == logging.NOTSET
assert toto_logger.getEffectiveLevel() == logging.WARN

# console_handler = logging.StreamHandler()
# toto_logger.addHandler(console_handler)
logging.basicConfig(filename="newfile.log",
                    format='"%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s"',
                    filemode='w')
toto_logger.setLevel(logging.DEBUG)
toto_logger.debug("debug")
toto_logger.info("info message")
toto_logger.warning("warning")
toto_logger.error("error")
toto_logger.critical("critical")
