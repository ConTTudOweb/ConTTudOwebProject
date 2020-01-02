import enum
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta


# TODO: Mudar para 5 anos quando for pra produção.
years_in_future_for_recurrence = 1


class AccountFrequencys(enum.Enum):
    weekly = 'weekly'
    biweekly = 'biweekly'
    monthly = 'monthly'
    bimonthly = 'bimonthly'
    quarterly = 'quarterly'
    semiannual = 'semiannual'
    annual = 'annual'


def get_due_date(due_date, frequency, parcel=None, day=None):
    if parcel == None:
        parcel = 1
    else:
        parcel -= 1

    if frequency == AccountFrequencys.weekly.value:
        return due_date + timedelta(days=7 * (parcel))
    elif frequency == AccountFrequencys.biweekly.value:
        return due_date + timedelta(days=14 * (parcel))

    # Mensal
    elif frequency == AccountFrequencys.monthly.value:
        _due_date = due_date + relativedelta(months=+parcel)
        _day = day
        while True:
            try:
                _due_date = datetime.date(year=_due_date.year, day=_day, month=_due_date.month)
                break
            except ValueError:
                if _day <= 28:
                    break
                else:
                    _day -= 1
        return _due_date

    elif frequency == AccountFrequencys.bimonthly.value:
        return due_date + relativedelta(months=+((parcel)*2))
    elif frequency == AccountFrequencys.quarterly.value:
        return due_date + relativedelta(months=+((parcel)*3))
    elif frequency == AccountFrequencys.semiannual.value:
        return due_date + relativedelta(months=+((parcel)*6))
    elif frequency == AccountFrequencys.annual.value:
        return due_date + relativedelta(years=+(parcel))


# def get_due_date(due_date, frequency, parcel):
#     if frequency == AccountFrequencys.weekly.value:
#         return due_date + timedelta(days=7 * (parcel - 1))
#     elif frequency == AccountFrequencys.biweekly.value:
#         return due_date + timedelta(days=14 * (parcel - 1))
#     elif frequency == AccountFrequencys.monthly.value:
#         return due_date + relativedelta(months=+(parcel - 1))
#     elif frequency == AccountFrequencys.bimonthly.value:
#         return due_date + relativedelta(months=+((parcel - 1)*2))
#     elif frequency == AccountFrequencys.quarterly.value:
#         return due_date + relativedelta(months=+((parcel - 1)*3))
#     elif frequency == AccountFrequencys.semiannual.value:
#         return due_date + relativedelta(months=+((parcel - 1)*6))
#     elif frequency == AccountFrequencys.annual.value:
#         return due_date + relativedelta(years=+(parcel - 1))
