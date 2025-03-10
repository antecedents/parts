"""Module decompose.py"""
import pandas as pd
import numpy as np

import statsmodels.tsa.seasonal as stsl


class Decompose:
    """
    Notes<br>
    ------<br>

    This class decomposes the <i>natural logarithm of the attendances series</i>, i.e., ln(# of attendances per week).
    """

    def __init__(self, arguments: dict):
        """

        :param arguments: The modelling arguments
        """

        self.__arguments: dict = arguments
        self.__decompose: dict = self.__arguments.get('decompose')

    def __add_components(self, frame: pd.DataFrame) -> pd.DataFrame:
        """

        :param frame:
        :return:
        """

        components: stsl.DecomposeResult = stsl.STL(
            frame['ln'], period=self.__arguments.get('seasons'),
            seasonal=self.__decompose.get('smoother_seasonal'),
            trend_deg=self.__decompose.get('degree_trend'),
            seasonal_deg=self.__decompose.get('degree_seasonal'),
            robust=True).fit()

        frame['trend'] = components.trend
        frame['residue'] = components.resid
        frame['seasonal'] = components.seasonal

        return frame

    def exc(self, data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data: The data set consisting of the attendance numbers of <b>an</b> institution/hospital.
        :return:
        """

        frame = data.copy()

        # Natural Logarithm
        frame['ln'] = np.log(frame['n_attendances'])

        # Decomposition Components
        frame = self.__add_components(frame=frame.copy())

        return frame
