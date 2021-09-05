from .error_handlers import title_invalid, mnk_invalid, error_bars_invalid, plot_invalid
from .step_handlers import (
    initiate,
    title_proceed,
    mnk_proceed,
    error_bars_proceed,
    plot_finish,
)

from create_env import dp
from ..states import Plots

from aiogram import types
from aiogram.dispatcher.filters import Text

initiate = dp.message_handler(commands="plot")(initiate)

title_proceed = dp.message_handler(
    lambda message: message.content_type == types.message.ContentType.TEXT,
    state=Plots.title_state,
)(title_proceed)
title_invalid = dp.message_handler(
    state=Plots.title_state, content_types=types.message.ContentType.ANY
)(title_invalid)

mnk_proceed = dp.message_handler(Text(equals=["✅", "❌"]), state=Plots.mnk_state)(
    mnk_proceed
)
mnk_invalid = dp.message_handler(
    state=Plots.mnk_state, content_types=types.message.ContentType.ANY
)(mnk_invalid)

error_bars_proceed = dp.message_handler(
    lambda message: message.content_type == types.message.ContentType.TEXT,
    state=Plots.error_bars_state,
)(error_bars_proceed)
error_bars_invalid = dp.message_handler(
    state=Plots.error_bars_state, content_types=types.message.ContentType.ANY
)(error_bars_invalid)

plot_finish = dp.message_handler(
    content_types=types.message.ContentTypes.DOCUMENT, state=Plots.plot_state
)(plot_finish)
plot_invalid = dp.message_handler(
    content_types=types.message.ContentType.ANY, state=Plots.plot_state
)(plot_invalid)
