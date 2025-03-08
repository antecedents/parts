"""Module page.py"""
import os

import pymc

import config
import src.elements.codes as ce


class Page:

    def __init__(self, model: pymc.model.Model, code: ce.Codes):
        """

        :param model:
        :param code:
        """

        self.__model = model
        self.__code = code

        configurations = config.Config()
        self.__root = os.path.join(configurations.artefacts_, 'models', code.hospital_code)

    def __graph(self):
        """

        :return:
        """

        pathstr = os.path.join(self.__root, 'tcf_algorithm.pdf')

        try:
            pymc.model_graph.model_to_graphviz(
                model=self.__model, figsize=(2, 2), save=pathstr, dpi=1200)
        except IOError as err:
            raise err from err

    def __text(self):
        """

        :return:
        """

        pathstr = os.path.join(self.__root, 'tcf_algorithm.txt')

        try:
            with open(file=pathstr, mode='w', encoding='utf-8', newline='\r\n') as disk:
                disk.write(self.__model.str_repr())
        except IOError as err:
            raise err from err

    def exc(self):
        """

        :return:
        """

        self.__graph()
        self.__text()
