from controller import report
import datetime, time
import os


def file_is_closed(year, week):
    filename = get_filename(year, week)
    print(filename)
    if os.path.exists(filename):
        try:
            os.rename(filename, filename)
            return True
        except OSError as e:
            print(e)
            return False
    return True


def delete_report(year, week):
    week = int(week)
    year = int(year)
    try:
        os.remove(get_filename(year, week))
        return True
    except(PermissionError):
        return False


def run_report(year, week):
    base = 'model/'
    print(file_is_closed(year, week))
    if file_is_closed(year, week):
        report.create_report(year, week, base)
        return True
    return False


def get_current_year_week():
    d = report.get_current_week()
    return {'year': d[0], 'week': d[1]}


def get_week_dates(year, week):
    sunday = report.get_date_sunday(year, week)
    saturday = sunday + datetime.timedelta(days=6)
    return {
        'sunday': sunday.strftime("%d/%m/%Y"),
        'saturday': saturday.strftime("%d/%m/%Y"),
    }


def open_file(year, week):
    os.startfile((get_filename(year, week)))


def fileexits(year, week):
    """(int, int) -> bool
    checks if ile exists
    """
    return os.path.isfile(get_filename(year, week))


def get_filename(year, week):
    directory = 'model/'
    return report.get_filename(directory, year, week)

    # return f"{base}/{year}/week {week}/week {week} orders.xlsx"


def last_modified(year, week):
    if fileexits(year, week):
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(get_filename(year, week))
        return "last modified: %s" % time.ctime(mtime)
    else:
        return "Still Need to run report"
