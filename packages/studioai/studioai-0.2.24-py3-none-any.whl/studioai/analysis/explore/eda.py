#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /studioai/analysis/explore/eda.py                                                   #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday August 10th 2023 08:29:08 pm                                               #
# Modified   : Friday June 7th 2024 02:16:21 pm                                                    #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Callable, List, Union

import pandas as pd

from studioai.analysis.stats.descriptive.summary import SummaryStats
from studioai.analysis.stats.inferential.test import Inference
from studioai.analysis.visualize.visualizer import SeabornCanvas, Visualizer

# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------------------------ #
#                                           EXPLORER                                               #
# ------------------------------------------------------------------------------------------------ #
class Explorer(ABC):
    """Encapsulates the data and behaviors in support of Exploratory Data Analysis

    Args:
        df (pd.DataFrame): Pandas DataFrame object.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self._visualizer = Visualizer(canvas=SeabornCanvas())
        self._inference = Inference()
        self._tests = {}
        self._overview = None
        self._info = None

    def __len__(self):
        """Returns the length of the dataset."""
        return len(self.df)

    @property
    @abstractmethod
    def summary(self) -> pd.DataFrame:
        """Returns a summary of the dataset contents in DataFrame format"""

    @property
    def plot(self) -> Visualizer:  # pragma: no cover
        self._visualizer.data = self.df
        return self._visualizer

    @property
    def stats(self) -> Inference:  # pragma: no cover
        self._inference.data = self.df
        return self._inference

    @property
    def columns(self) -> list:
        """Returns a list containing the names of the columns in the dataset."""
        return self.df.columns

    @property
    def shape(self) -> list:
        """Returns the shape of the dataset"""
        return self.df.shape

    @property
    def dtypes(self) -> list:
        """Returns the count of data types in the dataset."""
        dtypes = self.df.dtypes.value_counts().reset_index()
        dtypes.columns = ["Data Type", "Count"]
        dtypes["Data Type"] = dtypes["Data Type"].astype(str)
        dtypes = dtypes.groupby(by="Data Type").sum()
        return dtypes

    @property
    def size(self) -> int:
        """Returns the size of the Dataset in memory in bytes."""
        return self.df.memory_usage(deep=True).sum()

    # ------------------------------------------------------------------------------------------- #
    @property
    def overview(self) -> pd.DataFrame:
        """Returns an overview of the dataset in terms of its shape and size."""

        if self._overview is None:
            nvars = self.df.shape[1]
            nrows = self.df.shape[0]
            ncells = nvars * nrows
            size = self.df.memory_usage(deep=True).sum().sum()
            d = {
                "Number of Observations": nrows,
                "Number of Variables": nvars,
                "Number of Cells": ncells,
                "Size (Bytes)": size,
            }
            overview = pd.DataFrame.from_dict(data=d, orient="index").reset_index()
            overview.columns = ["Characteristic", "Total"]
            self._overview = overview.style.format(thousands=",")

        return self._overview

    # ------------------------------------------------------------------------------------------- #
    @property
    def info(self) -> pd.DataFrame:
        """Returns a DataFrame with basic dataset quality statistics"""

        if self._info is None:
            info = self.df.dtypes.to_frame().reset_index()
            info.columns = ["Column", "DataType"]
            info["Complete"] = self.df.count().values
            info["Null"] = self.df.isna().sum().values
            info["Completeness"] = info["Complete"] / self.df.shape[0]
            info["Unique"] = self.df.nunique().values
            info["Duplicate"] = self.df.shape[0] - self.df.nunique().values
            info["Uniqueness"] = self.df.nunique().values / self.df.shape[0]
            info["Size"] = (
                self.df.memory_usage(deep=True, index=False).to_frame().reset_index()[0]
            )
            info = round(info, 2)
            self._info = info.style.format(thousands=",")

        return self._info

    # ------------------------------------------------------------------------------------------- #
    def as_df(self) -> pd.DataFrame:
        """Returns the dataset as a pandas DataFrame"""
        return self.df

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
        df = self.df.sample(n=n, frac=frac, replace=replace, random_state=random_state)
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
            cols = [col for col in self.df.columns if col not in exclude]
        elif include is not None:
            cols = [col for col in self.df.columns if col in include]
        else:
            cols = self.df.columns
        df = self.df[cols]
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
            df = self.df[condition]
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
            df = self.df.sort_values(by=x, ascending=False, axis=0)
            return df.head(n)
        except KeyError as e:
            msg = f"{x} is not a valid variable in the dataset."
            logger.exception(msg)
            raise KeyError(f"{msg}\n{e}")

    # ------------------------------------------------------------------------------------------- #
    def head(self, n: int = 5) -> pd.DataFrame:
        return self.df.head(n)

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
        df = self.df
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
            df = self.df[columns].drop_duplicates().reset_index(drop=True)
        else:
            df = self.df.drop_duplicates().reset_index(drop=True)
        return self._format(df=df)

    # ------------------------------------------------------------------------------------------- #
    def top_n_frequency_analysis(self, x: str, n: int, data: pd.DataFrame = None):
        """Returns a dataframe with proportional and cumulative counts of one or more categorical variables.

        Args:
            x (Union[str,List[str]]): A string or list of strings indicating the variables included in the count.
            n (int): Number of rows to include in top n.
            data (pd.DataFrame). Data to analyze. Optional.

        """

        # Use instance variable df if data is None
        data = data or self.df

        # Calculate frequency distribution
        freq = data[x].value_counts().reset_index()
        freq.columns = [x, "Count"]

        # Calculate cumulative count and proportions
        freq["Cumulative Count"] = freq["Count"].cumsum()
        total_count = freq["Count"].sum()
        freq["Proportion"] = freq["Count"] / total_count
        freq["Cumulative Proportion"] = freq["Proportion"].cumsum()

        # Top N rows
        top_n = freq.head(n).copy()

        # Row for the rest of the dataset
        if len(freq) > n:
            rest_count = freq.iloc[n:]["Count"].sum()
            rest_cumulative_count = top_n["Cumulative Count"].iloc[-1] + rest_count
            rest_proportion = rest_count / total_count
            rest_cumulative_proportion = (
                1.0  # because it's the rest, it covers the remaining percentage
            )
            rest_row = pd.DataFrame(
                {
                    x: [f"Rest of {x}"],
                    "Count": [rest_count],
                    "Cumulative Count": [rest_cumulative_count],
                    "Proportion": [rest_proportion],
                    "Cumulative Proportion": [rest_cumulative_proportion],
                }
            )
            top_n = pd.concat([top_n, rest_row], ignore_index=True)

        # Total row
        total_row = pd.DataFrame(
            {
                x: ["Total"],
                "Count": [total_count],
                "Cumulative Count": [total_count],
                "Proportion": [1.0],
                "Cumulative Proportion": [1.0],
            }
        )
        top_n = pd.concat([top_n, total_row], ignore_index=True)

        return top_n

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

        if isinstance(self.df[x], pd.Series):
            abs = (
                self.df[x]
                .value_counts(
                    normalize=False, sort=sort, bins=bins, ascending=ascending
                )
                .to_frame()
            )
            rel = (
                self.df[x]
                .value_counts(normalize=True, sort=sort, bins=bins, ascending=ascending)
                .to_frame()
            )
        else:
            abs = (
                self.df[x]
                .value_counts(normalize=False, sort=sort, ascending=ascending)
                .to_frame()
            )
            rel = (
                self.df[x]
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
    def countstats(self, x: str, df: pd.DataFrame = None) -> pd.DataFrame:
        """Computes descriptive statistics of counts for a variable.

        The value counts of the x variable are obtained and descriptive statistics are
        computed showing min, max, average, std, and quantiles of counts.

        Args:
            x (str): Name of a variable in the dataset
            df (pd.DataFrame): Optional dataframe from which counts will be taken.

        Returns:
            Value Counts: pd.DataFrame
            Count Statistics: pd.DataFrame

        """
        if df is None:
            counts = self.df[x].value_counts().to_frame().reset_index()
        else:
            counts = df[x].value_counts().to_frame().reset_index()
        stats = counts["count"].describe().to_frame().reset_index()
        stats.columns = [x]
        return counts, stats.T

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
