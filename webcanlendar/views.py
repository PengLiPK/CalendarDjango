import time, calendar
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse
from webcanlendar.models import *
from webcanlendar.forms import *

mnames = "January February March April May June July August September October November December"
mnames = mnames.split()


#@login_required
def main(request, year=None):
    """Main listing, years and months; three years per page."""
    # prev / next years
    if year: 
    	year = int(year)
    else:    
    	year = time.localtime()[0]

    nowy, nowm = time.localtime()[:2]
    lst = []

    # create a list of months for each year, indicating ones that contain entries and current
    for y in [year, year+1, year+2]:
        mlst = []
        for n, month in enumerate(mnames):
            entry = current = False   # are there entry(s) for this month; current month?
            entries = Entry.objects.filter(date__year=y, date__month=n+1)

            if entries:
                entry = True
            if y == nowy and n+1 == nowm:
                current = True
            mlst.append(dict(n=n+1, name=month, entry=entry, current=current))
        lst.append((y, mlst))

    return render(request, 'index.html', dict(years=lst, user=request.user, year=year))


#@login_required
def month(request, year, month, change=None):
    """Listing of days in `month`."""
    year, month = int(year), int(month)

    # apply next / previous change
    if change in ("next", "prev"):
        now, mdelta = date(year, month, 15), timedelta(days=31)
        if change == "next":   mod = mdelta
        elif change == "prev": mod = -mdelta

        year, month = (now+mod).timetuple()[:2]

    # init variables
    cal = calendar.Calendar()
    month_days = cal.itermonthdays(year, month)
    nyear, nmonth, nday = time.localtime()[:3]
    lst = [[]]
    week = 0

    # make month lists containing list of days for each week
    # each day tuple will contain list of entries and 'current' indicator
    for day in month_days:
        entries = current = False   # are there entries for this day; current day?
        if day:
            entries = Entry.objects.filter(date__year=year, date__month=month, date__day=day)
            if day == nday and year == nyear and month == nmonth:
                current = True

        lst[week].append((day, entries, current))
        if len(lst[week]) == 7:
            lst.append([])
            week += 1

    return render(request, "month.html", dict(year=year, month=month, user=request.user,
                        month_days=lst, mname=mnames[month-1]))

#@login_required
def day(request, year, month, day):

    if request.method == 'POST':
        formset = EntryForm(request.POST)
        if formset.is_valid():
            # add current user and date to each entry & save
            entry = formset.save(commit=False)
            entry.date = date(int(year), int(month), int(day))
            entry.save()
            return redirect(reverse("month1", args=(year, month)))

    else:
        # display formset for existing enties and one extra form
        formset = Entry.objects.filter(date=date(int(year), int(month), int(day)))
        return render(request, "day.html", {"year":year, "month":month, "day":day,"formset": formset})

def delete_entry(request, year, month, day, entry_id):
    try:
        Entry.objects.get(id=entry_id).delete()
    except:
    	pass
    formset = Entry.objects.filter(date__year=year, date__month=month, date__day=day)
    return render(request, "day.html", {"year":year, "month":month, "day":day,"formset": formset})
