import unittest
import datetime as dt
from collections import OrderedDict

from toggl.format import (format_time, format_min,
                          get_dayily_report, get_monthly_report,
                          DailyReport)


class TestFormat(unittest.TestCase):
    def test_format_time(self):
        res1 = format_time(dt.time(hour=10, minute=37, second=43))
        res2 = format_time(dt.time(hour=10, minute=37, second=13))
        res3 = format_time(dt.time(hour=10, minute=54, second=29))
        self.assertEqual(res1, dt.time(hour=10, minute=45))
        self.assertEqual(res2, dt.time(hour=10, minute=30))
        self.assertEqual(res3, dt.time(hour=11, minute=0))

    def test_format_min(self):
        res1 = format_min(137)
        res2 = format_min(180 + 32)
        self.assertEqual(res1, dt.time(hour=2, minute=15))
        self.assertEqual(res2, dt.time(hour=3, minute=30))

    def test_get_daily_report(self):
        times = [
            (dt.datetime.strptime('19:03:12', '%H:%M:%S'),
             dt.datetime.strptime('19:10:42', '%H:%M:%S')),
            (dt.datetime.strptime('20:43:54', '%H:%M:%S'),
             dt.datetime.strptime('21:21:00', '%H:%M:%S')),
            (dt.datetime.strptime('21:46:00', '%H:%M:%S'),
             dt.datetime.strptime('23:23:49', '%H:%M:%S'))
        ]
        report = get_dayily_report('2019-10-01', times)
        self.assertEqual(report, DailyReport(
            date=dt.date(year=2019, month=10, day=1),
            start=dt.time(hour=19),
            end=dt.time(hour=23, minute=30),
            rest=dt.time(hour=2)))

    def test_get_monthly_report(self):
        rows = [
            OrderedDict([('Start date', '2019-10-1'),
                        ('Start time', '19:03:12'),
                        ('End time', '19:10:42')]),
            OrderedDict([('Start date', '2019-10-1'),
                        ('Start time', '20:43:54'),
                        ('End time', '21:21:00')]),
            OrderedDict([('Start date', '2019-10-3'),
                        ('Start time', '10:00:55'),
                        ('End time', '14:23:12')])
        ]
        report = get_monthly_report(rows)
        expected = [
            DailyReport(
                date=dt.date(year=2019, month=10, day=1),
                start=dt.time(hour=19),
                end=dt.time(hour=21, minute=15),
                rest=dt.time(hour=1, minute=30)),
            DailyReport(
                date=dt.date(year=2019, month=10, day=3),
                start=dt.time(hour=10),
                end=dt.time(hour=14, minute=30),
                rest=dt.time(hour=0))
        ]
        self.assertEqual(report, expected)
