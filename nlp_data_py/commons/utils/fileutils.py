from pathlib import Path
import pickle
import os
from nlp_data_py.commons.utils.logging import Logging
from logging import Logger


class FileUtils:
    """Simple util to quickly read and write files.
    Nothing much here

    """

    logger: Logger = Logging.get_logger("FileUtils")

    def __init__(self):
        pass

    @staticmethod
    def write_content_tofile(content, file, mode='a'):
        """Write content to file. By default it writes in append mode

        Args:
            content: str: Contents to write to file
            file: str: Path where to write
            mode: str: Mode in which to write. Default
                       is append mode

        Returns:
             Nothing

        Raises:
            Usual file handling exceptions

        """
        try:
            FileUtils.logger.debug(f"Writing to : {file}")
            Path(file).open(mode).write(content)
        except Exception as e:
            FileUtils.logger.error(f"Exception while writing to file : {e}")
            raise

    @staticmethod
    def read_file(file):
        """Read contents from file.

        Args:
            file: str: Path of file to read

        Returns:
            contents of file as strin

        Raises:
            Usual file handling exceptions

        """
        try:
            FileUtils.logger.debug(f"Reading file : {file}")
            return Path(file).read_text()
        except Exception as e:
            FileUtils.logger.error(f"Exception while reading file : {e}")
            raise

    @staticmethod
    def read_pickle(path):
        """Read Pickled file and return read object

        Args:
            path:str: Path to Pickle file

        Raises:
            Usual file ops and pickle Exceptions

        """
        try:
            FileUtils.logger.debug(f"Reading pickle from : {path}")
            return pickle.load(Path(path).open('rb'))
        except Exception as e:
            FileUtils.logger.error(f"Failed to read pickle file {path} {e}")
            raise

    @staticmethod
    def write_pickle(obj, path):
        """Write object as pickle file

        Args:
            obj: Any: Object to write
            path: str: Path to write

        Raises:
            Usual file and pickle exceptions

        """
        try:
            FileUtils.logger.debug(f"Writing pickle to : {path}")
            FileUtils.mkdir(Path(path).parent)
            pickle.dump(obj, open(path, 'wb'))
        except Exception as e:
            FileUtils.logger.error(f"Failed to read picke file {path} {e}")
            raise

    @staticmethod
    def file_exist(path):
        """Checks if file exists

        """
        return Path(path).exists()

    @staticmethod
    def mkdir(path):
        """Make directory if it dose not already exists

        """
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            FileUtils.logger.error(f"Failed to create dirs {path} {e}")
