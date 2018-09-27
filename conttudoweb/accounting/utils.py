import enum
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class AccountFrequencys(enum.Enum):
    weekly = 'weekly'
    biweekly = 'biweekly'
    monthly = 'monthly'
    bimonthly = 'bimonthly'
    quarterly = 'quarterly'
    semiannual = 'semiannual'
    annual = 'annual'


def get_due_date(due_date, frequency, parcel):
    if frequency == AccountFrequencys.weekly.value:
        return due_date + timedelta(days=7 * (parcel - 1))
    elif frequency == AccountFrequencys.biweekly.value:
        return due_date + timedelta(days=14 * (parcel - 1))
    elif frequency == AccountFrequencys.monthly.value:
        return due_date + relativedelta(months=+(parcel - 1))
    elif frequency == AccountFrequencys.bimonthly.value:
        return due_date + relativedelta(months=+((parcel - 1)*2))
    elif frequency == AccountFrequencys.quarterly.value:
        return due_date + relativedelta(months=+((parcel - 1)*3))
    elif frequency == AccountFrequencys.semiannual.value:
        return due_date + relativedelta(months=+((parcel - 1)*6))
    elif frequency == AccountFrequencys.annual.value:
        return due_date + relativedelta(years=+(parcel - 1))
