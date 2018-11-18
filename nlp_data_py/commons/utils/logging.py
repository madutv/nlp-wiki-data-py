import logging
import sys
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(funcName)s - %(levelname)s — %(message)s")


class Logging:
    """Generic Logging with logging module.
    This class has a property: DEFAULT_LEVEL.
    which is a Log Level variable. Global level will be used
    when no specific log levels are specified with get_logger.
    Default global level is DEBUG. This can be overridden

    """

    DEFAULT_LEVEL = logging.WARNING
    DEFAULT_HANDLERS = [logging.StreamHandler]
    DEFAULT_STREAM = sys.stdout

    @staticmethod
    def get_logger(name: str, level=None, propagate=False,  handlers=DEFAULT_HANDLERS, args=[[DEFAULT_STREAM]]):
        """ Returns a logger of the name provided.

        Args:
            name (str): Name of the logger to be created.
            level (int): Level at which logs should be
                written. (same as logging.Levels) default
                value is None. If None, Logging.global_level
                be used
            propagate (Boolean): Propagate logs to parent.
                Default value is False
            handlers (List of functions): Function that
                returns a logging handler. These
                functions will be called with logger.addHandler.
                default value is [logging.StreamHandler].
            args (List[List]):  List of parameters for the handlers.
                It should match with the number of handlers.
                If the function takes no parameters leave an empty
                list. default value: empty list of empty list.
                default value is args=[[DEFAULT_STREAM]]

        Returns: logger

        """

        logger = logging.getLogger(name)
        if level is None:
            logger.setLevel(Logging.DEFAULT_LEVEL)
        else:
            logger.setLevel(level)

        for func, arg in zip(handlers, args):
            logger.addHandler(func(*arg))

        for handler in logger.handlers:
            handler.setFormatter(FORMATTER)

        logger.propagate = propagate
        return logger

