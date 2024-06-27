#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /studioai/data/dataset.py                                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday August 10th 2023 08:29:08 pm                                               #
# Modified   : Wednesday June 26th 2024 07:13:44 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from abc import ABC, abstractproperty
import logging
from typing import Callable, Union, List

import pandas as pd

from studioai.analysis.stats.descriptive.summary import SummaryStats
from studioai.analysis.visualize.visualizer import Visualizer, SeabornCanvas

# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------------------------ #
#                                            DATASET                                               #
# ------------------------------------------------------------------------------------------------ #
class Dataset(ABC):
    """Encapsulates numerical and categorical data comprising a set.

    Args:
        df (pd.DataFrame): Pandas DataFrame object.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        self._df = df
        self._visualizer = Visualizer(canvas=SeabornCanvas())

    def __len__(self):
        """Returns the length of the dataset."""
        return len(self._df)

    @abstractproperty
    def summary(self) -> pd.DataFrame:
        """Returns a summary of the dataset contents in DataFrame format"""

    @property
    def columns(self) -> list:
        """Returns a list containing the names of the columns in the dataset."""
        return self._df.columns

    @property
    def shape(self) -> list:
        """Returns the shape of the dataset"""
        return self._df.shape

    @property
    def dtypes(self) -> list:
        """Returns the count of data types in the dataset."""
        dtypes = self._df.dtypes.value_counts().reset_index()
        dtypes.columns = ["Data Type", "Count"]
        dtypes["Data Type"] = dtypes["Data Type"].astype(str)
        dtypes = dtypes.groupby(by="Data Type").sum()
        return dtypes

    @property
    def size(self) -> int:
        """Returns the size of the Dataset in memory in bytes."""
        return self._df.memory_usage(deep=True).sum()

    # ------------------------------------------------------------------------------------------- #
    @property
    def overview(self) -> pd.DataFrame:
        """Returns an overview of the dataset in terms of its shape and size."""

        nvars = self._df.shape[1]
        nrows = self._df.shape[0]
        ncells = nvars * nrows
        size = self._df.memory_usage(deep=True).sum().sum()
        d = {
            "Number of Observations": nrows,
            "Number of Variables": nvars,
            "Number of Cells": ncells,
            "Size (Bytes)": size,
        }
        overview = pd.DataFrame.from_dict(data=d, orient="index").reset_index()
        overview.columns = ["Characteristic", "Total"]
        return self._format(df=overview)

    # ------------------------------------------------------------------------------------------- #
    @property
    def info(self) -> pd.DataFrame:
        """Returns a DataFrame with basic dataset quality statistics"""

        info = self._df.dtypes.to_frame().reset_index()
        info.columns = ["Column", "DataType"]
        info["Valid"] = self._df.count().values
        info["Null"] = self._df.isna().sum().values
        info["Validity"] = info["Valid"] / self._df.shape[0]
        info["Cardinality"] = self._df.nunique().values
        info["Percent Unique"] = self._df.nunique().values / self._df.shape[0]
        info["Size"] = (
            self._df.memory_usage(deep=True, index=False).to_frame().reset_index()[0]
        )
        info = round(info, 2)
        return self._format(df=info)

    # ------------------------------------------------------------------------------------------- #
    def as_df(self) -> pd.DataFrame:
        """Returns the dataset as a pandas DataFrame"""
        return self._df

    # ------------------------------------------------------------------------------------------- #
    def sample(
        self,
        n: int = 5,
        frac: float = None,
        replace: bool = False,
        random_state: int = None,
    ) -> pd.DataFrame:
        """Returns a sample from the FOG Dataset

        Args:
            n (int): Number of items to return. Defaults to five.
            frac (float): Proportion of items to return
            replace (bool): Whether to sample with replacement
            random_state (int): Pseudo random seed.
        """
        df = self._df.sample(n=n, frac=frac, replace=replace, random_state=random_state)
        return self._format(df=df)

    # ------------------------------------------------------------------------------------------- #
    def select(self, include: list = None, exclude: list = None) -> pd.DataFrame:
        """Selects columns of the data to be included or excluded.

        Args:
            include (list[str]): List of columns to include. Only values in the dataset columns
                are include. Values that do not exist in the dataset are ignored. No KeyError
                exception is raised.
            exclude (list[str]): List of columns to exclude. If non-Null, include parameter
                is ignored, and all columns will be returned except those indicated
                here.
        """
        if exclude is not None:
            cols = [col for col in self._df.columns if col not in exclude]
        elif include is not None:
            cols = [col for col in self._df.columns if col in include]
        else:
            cols = self._df.columns
        df = self._df[cols]
        return self._format(df=df)

    # ------------------------------------------------------------------------------------------- #
    def subset(self, condition: Callable) -> pd.DataFrame:
        """Subsets the data according to the stated condition.

        Args:
            condition (Callable): Lambda function that will be used to
                subset the data as a pandas dataframe.
                Example condition = lambda df: df['age'] > 18
        """
        try:
            df = self._df[condition]
            return self._format(df=df)
        except Exception as e:
            msg = f"Exception of type {type(e)} occurred.\n{e}"
            logger.exception(msg)
            raise

    # ------------------------------------------------------------------------------------------- #
    def top_n(self, x: str, n: int = 10) -> pd.DataFrame:
        """Returns the observations with the top n values in the x column.

        Args:
            x (str): Name of a column in the dataset.
            n (int): The top n observations to return.
        """
        try:
            df = self._df.sort_values(by=x, ascending=False, axis=0)
            return df.head(n)
        except KeyError as e:
            msg = f"{x} is not a valid variable in the dataset."
            logger.exception(msg)
            raise KeyError(f"{msg}\n{e}")

    # ------------------------------------------------------------------------------------------- #
    def head(self, n: int = 5) -> pd.DataFrame:
        return self._df.head(n)

    # ------------------------------------------------------------------------------------------- #
    def describe(
        self,
        x: list[str] = None,
        include: list[str] = None,
        exclude: list[str] = None,
        groupby: Union[str, list[str]] = None,
    ) -> SummaryStats:
        """Provides descriptive statistics for the dataset.

        Args:
            x (list[str]): List of variables to incude. If non-Null, include and exclude will be ignored.
            include (list[str]): List of data types to include in the analysis.
            exclude (list[str]): List of data types to exclude from the analysis.
            groupby (str): Column used as a factor variable for descriptive statistics.
        """
        df = self._df
        if x is not None:
            df = df[x]

        stats = SummaryStats()
        stats.describe(data=df, groupby=groupby, include=include, exclude=exclude)
        return stats

    # ------------------------------------------------------------------------------------------- #
    def unique(self, columns: list = None) -> pd.DataFrame:
        """Returns a DataFrame containing the unique values for all or the designated columns.

        Args:
            columns (list): List of columns for which unique values are to be returned.
        """
        if columns is not None:
            df = self._df[columns].drop_duplicates().reset_index(drop=True)
        else:
            df = self._df.drop_duplicates().reset_index(drop=True)
        return self._format(df=df)

    # ------------------------------------------------------------------------------------------- #
    def frequency(
        self,
        x: Union[str, List[str]],
        sort: bool = False,
        bins: int = 4,
        ascending: bool = True,
        formatting: bool = True,
    ) -> pd.DataFrame:
        """Returns a dataframe with proportional and cumulative counts of one or more categorical variables.

        Args:
            x (Union[str,List[str]]): A string or list of strings indicating the variables included in the count.
            sort (bool): Whether to sort by frequencies. If False, sorting will done by label.
            ascending (bool): Whether to sort ascending.
            formatting (bool): Whether to format the DataFrame for presentation.
            bins (int): Rather than count values, group them into half-open bins, only works with numeric data.

        """

        if isinstance(self._df[x], pd.Series):
            abs = (
                self._df[x]
                .value_counts(
                    normalize=False, sort=sort, bins=bins, ascending=ascending
                )
                .to_frame()
            )
            rel = (
                self._df[x]
                .value_counts(normalize=True, sort=sort, bins=bins, ascending=ascending)
                .to_frame()
            )
        else:
            abs = (
                self._df[x]
                .value_counts(normalize=False, sort=sort, ascending=ascending)
                .to_frame()
            )
            rel = (
                self._df[x]
                .value_counts(normalize=True, sort=sort, ascending=ascending)
                .to_frame()
            )
        freq = abs.join(rel, on=x)
        freq.loc["Total"] = freq.sum()
        freq["cumulative"] = freq["proportion"].cumsum()
        freq.loc[freq.index[-1], freq.columns[-1]] = " "
        if formatting:
            freq = self._format(freq)
        return freq

    # ------------------------------------------------------------------------------------------- #
    @property
    def plot(self) -> Visualizer:  # pragma: no cover
        self._visualizer.data = self._df
        return self._visualizer

    # ------------------------------------------------------------------------------------------- #
    #                                PRIVATE METHODS                                              #
    # ------------------------------------------------------------------------------------------- #
    def _format(self, df: pd.DataFrame) -> pd.DataFrame:
        """Returns the resulting dataframe with capitalized column names."""
        # df.columns = [col.capitalize() for col in df.columns]
        df = df.apply(self._show_thousands_separator)
        return df

    def _show_thousands_separator(self, x):  # pragma: no cover
        """Formats an numbers with thousands separator."""
        try:
            if self._is_numeric(x):
                return f"{x:,}"
            else:
                return x
        except Exception:
            return x

    def _is_numeric(self, x) -> bool:
        try:
            pd.to_numeric(x, errors="raise")
            return True
        except Exception:
            return False
