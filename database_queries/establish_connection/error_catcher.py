import sys


def print_psycopg2_exception(err, file_path, func_name):
    """
    Функция, печатающая информацию об ошибке.
    """
    # get details about the exception
    err_type, _, traceback = sys.exc_info()

    # get the line number when exception occurred
    line_num = traceback.tb_lineno

    # print the poolect() error
    print(
        "\n\n\npsycopg2 ERROR:",
        err,
        "on line number:",
        line_num,
        "in package:",
        file_path,
        "in function:",
        func_name,
    )
    print("psycopg2 traceback:", traceback, "-- type:", err_type)
