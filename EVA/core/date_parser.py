import datetime

def extract_due_date(text):
    today = datetime.date.today()

    if "tomorrow" in text:
        return (
            text.replace("tomorrow", "").strip(),
            str(today + datetime.timedelta(days=1))
        )

    elif "today" in text:
        return (
            text.replace("today", "").strip(),
            str(today)
        )

    return text.strip(), "no date"