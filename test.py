import datetime
from dateutil.relativedelta import relativedelta
a = datetime.datetime.now()
print(a.year, type(a.year))

date_time_str = '2018-06-29 08:15:27.243860'
date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
new = date_time_obj + relativedelta(years=1)
print(date_time_obj.year, "-", new, "-", type(new))























#
