from .generate_state import generate_state


Start = generate_state("Start", ("group", "custom"))
Profile = generate_state("Profile", ("choose", "group", "custom"))
Timetable = generate_state("Timetable", ("choose", "another_group", "weekday"))
Koryavov = generate_state(
    "Koryavov", ("sem_num_state", "task_num_state", "finish_state")
)
Custom = generate_state(
    "Custom", ("existing", "new", "weekday", "time", "edit", "again")
)
Exam = generate_state("Exam", ("another_group", "choose"))
Plots = generate_state(
    "Plots", ("title_state", "mnk_state", "error_bars_state", "plot_state")
)
Stat = generate_state("Stat", ("choice", "unique", "frequency"))
Mailing = generate_state("Mailing", ("mailing",))
