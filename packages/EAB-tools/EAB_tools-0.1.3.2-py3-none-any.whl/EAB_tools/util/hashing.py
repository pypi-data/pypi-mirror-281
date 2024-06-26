"""Utilities for hashing objects."""

from __future__ import annotations

import hashlib
from typing import cast

from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas.io.formats.style

from EAB_tools.eab_rc import eab_rc


def hash_df(
    df: pd.DataFrame | pd.Series | pd.Index | pd.MultiIndex,
    styler: pd.io.formats.style.Styler | None = None,
    max_len: int | None = eab_rc["hash_len"],
    usedforsecurity: bool = False,
) -> str:
    """
    Create a unique hash for a pandas object.

    Parameters
    ----------
    df : pd.DataFrame, pd.Series, pd.Index, or pd.MultiIndex
    styler : pd.io.formats.style.Styler, optional
        A pandas Styler object to include in the hash.
    max_len : int, default eab_rc['hash_len'] (default 7)
        Truncate the hash to a specified length.
    usedforsecurity : bool, default False

    Returns
    -------
    str
        Hash of the object.

    Examples
    --------
    >>> df = pd.DataFrame({'foo': list('foo'), 'bar': range(3)})
    >>> hash_df(df, max_len=None)
    'a52342e5da59276dd7107d750e86049108d83d2f'
    >>> df = df.rename(columns={'foo': 'spam'})
    >>> hash_df(df, max_len=10)
    'c6213b58f2'
    """
    if not isinstance(df, pd.DataFrame):
        try:
            # Series, Index, and MultiIndex can be converted to
            # pd.DataFrame
            df = df.to_frame()
        except AttributeError as exp:
            raise TypeError(f"df is {type(df)}, not DataFrame") from exp

    h = hashlib.sha1(usedforsecurity=usedforsecurity)
    h.update(pd.util.hash_pandas_object(df).values)
    h.update(pd.util.hash_pandas_object(df.columns).values)
    if styler is not None:
        h.update(styler.to_html().encode("UTF8"))

    return h.hexdigest()[:max_len]


def hash_mpl_fig(
    fig: plt.Figure | plt.Axes,
    max_len: int | None = eab_rc["hash_len"],
    usedforsecurity: bool = False,
) -> str:
    """Hash a matplotlib figure."""
    figure = fig.get_figure() if isinstance(fig, plt.Axes) else fig
    assert figure is not None

    canvas: FigureCanvasAgg = cast(FigureCanvasAgg, figure.canvas)
    canvas.draw()
    buf = canvas.buffer_rgba()
    X = np.asarray(buf).tobytes()

    h = hashlib.sha1(usedforsecurity=usedforsecurity)
    h.update(X)
    return h.hexdigest()[:max_len]
