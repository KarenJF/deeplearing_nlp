import datetime

# helper function
def check_date(val):
    month, day, year = val.split('/')
    
    isValidDate = True
    try:
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        isValidDate = False

    if(isValidDate == False):
        raise KeyError(f"Your most recent DACA expiration date {val} is not valid.")