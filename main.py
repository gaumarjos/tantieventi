import datetime
import os
import shutil

# Unused fields
# UID:
# LOCATION:
# DESCRIPTION:

FOLDER = "generated_events/"


def empty_folder(folder=FOLDER):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def weekly(summary_s, start_year, start_month, start_day, n, start_at=1, all_day=True, debug=False):
    now = datetime.datetime.now()
    today_s = "{}{:02d}{:02d}T{:02d}{:02d}{:02d}Z".format(now.year, now.month, now.day, now.hour, now.minute,
                                                          now.second)

    start = datetime.date(year=start_year, month=start_month, day=start_day)
    for i in range(n):
        delta = datetime.timedelta(weeks=i)
        day_delta = datetime.timedelta(days=1)
        event_start_date = start + delta
        event_end_date = start + delta + day_delta

        if not all_day:
            start_s = ":{}{:02d}{:02d}T{:02d}{:02d}{:02d}Z".format(event_start_date.year,
                                                                   event_start_date.month,
                                                                   event_start_date.day,
                                                                   0,
                                                                   0,
                                                                   0)
            end_s = ":{}{:02d}{:02d}T{:02d}{:02d}{:02d}Z".format(event_start_date.year,
                                                                 event_start_date.month,
                                                                 event_start_date.day,
                                                                 1,
                                                                 0,
                                                                 0)
        else:
            start_s = ";VALUE=DATE:{}{:02d}{:02d}".format(event_start_date.year,
                                                          event_start_date.month,
                                                          event_start_date.day)
            end_s = ";VALUE=DATE:{}{:02d}{:02d}".format(event_end_date.year,
                                                        event_end_date.month,
                                                        event_end_date.day)

        s = """BEGIN:VCALENDAR
CALSCALE:GREGORIAN
BEGIN:VEVENT
DTSTAMP:{}
DTSTART{}
DTEND{}
SUMMARY:{}
END:VEVENT
END:VCALENDAR""".format(
            today_s,
            start_s,
            end_s,
            summary_s + str(i + start_at),
        )

        if debug:
            print(s)

        f = open(FOLDER + "event {}.ics".format(i + start_at), "w")
        f.write(s)
        f.close()


if __name__ == '__main__':
    empty_folder()
    weekly("Piano - 100K settimana ",
           start_year=2022,
           start_month=10,
           start_day=24,
           n=5,
           start_at=2,
           all_day=True)