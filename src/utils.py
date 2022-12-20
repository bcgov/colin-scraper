import datetime

def avg_dates(dates):
    sum = datetime.timedelta()
    for date in dates:
        sum += date
    return sum / len(dates)

def get_pdf_count(pdf_dict, text):
    if text in pdf_dict:
        pdf_dict[text] += 1
        count = pdf_dict[text]
    else:
        pdf_dict[text] = 0
        count = pdf_dict[text]
    return count