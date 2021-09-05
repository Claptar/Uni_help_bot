from .common import exit_user, help_user
from .edit_user import (
    initiate,
    choose_proceed,
    choose_invalid,
    group_proceed,
    group_invalid_type,
    custom_proceed,
    custom_invalid,
)
from .koryavov import (
    initiate,
    semester_number_proceed,
    semester_number_invalid,
    task_number_proceed,
    task_number_invalid,
    finish_proceed,
    finish_invalid,
)
from .new_user import (
    initiate,
    group_proceed,
    group_invalid_format,
    custom_proceed,
    custom_invalid_variant,
)
from .plot import (
    initiate,
    title_proceed,
    title_invalid,
    mnk_proceed,
    mnk_invalid,
    error_bars_proceed,
    error_bars_invalid,
    plot_finish,
    plot_invalid,
)
from .timetable import semester, exam, custom, today_tomorrow

# admin resources
from .admin import mailing, statistics
