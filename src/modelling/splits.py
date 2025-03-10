"""Module splits.py"""
import logging
import os
import sys

import pandas as pd

import config
import src.elements.master as mr
import src.functions.streams


class Splits:
    """
    The training & testing splits.
    """

    def __init__(self, arguments: dict):
        """

        :param arguments: Modelling arguments.
        """

        self.__arguments = arguments
        self.__configurations = config.Config()
        self.__streams = src.functions.streams.Streams()
        self.__root = os.path.join(self.__configurations.artefacts_, 'data')

    def __include(self, blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        return blob.copy()[:-self.__arguments.get('ahead')]

    def __exclude(self, blob: pd.DataFrame) -> pd.DataFrame:
        """
        Excludes instances that will be predicted

        :param blob:
        :return:
        """

        return blob.copy()[-self.__arguments.get('ahead'):]

    def __persist(self, blob: pd.DataFrame, pathstr: str) -> None:
        """

        :param blob:
        :param pathstr:
        :return:
        """

        message = self.__streams.write(blob=blob, path=os.path.join(self.__root, pathstr))
        logging.info(message)

    def exc(self, data: pd.DataFrame, code: str, success: bool) -> mr.Master:
        """

        :param data: The data set consisting of the attendance numbers of <b>an</b> institution/hospital.
        :param code: An institution's identification code
        :param success: Directories creation success?
        :return:
        """

        frame = data.copy()

        # Split
        training = self.__include(blob=frame)
        testing = self.__exclude(blob=frame)

        # Persist
        if success:
            for instances, name in zip([frame, training, testing], ['data.csv', 'training.csv', 'testing.csv']):
                self.__persist(blob=instances, pathstr=os.path.join(code, name))
        else:
            sys.exit(f'Data and/or models directories unavailable: {code}')

        return mr.Master(training=training, testing=testing)
