import re


def find_to_start(text):
    to = re.compile(r'\bTo\b')
    return to.search(text).start()


def ship_date(text):
    ship_date_regex = re.compile(r'(\d\d)/(\d\d)/(\d\d)')
    ship_se = ship_date_regex.search(text)
    ship_date = ship_se.group()
    ship_date = ship_date.replace("/", "-")
    return ship_date


def ship_date_location(text):
    ship_date_regex = re.compile(r'(\d\d)/(\d\d)/(\d\d)')
    return ship_date_regex.search(text).start()

def ship_date_year(text):
    ship_date_regex = re.compile(r'(\d\d)/(\d\d)/(\d\d)')
    ship_se = ship_date_regex.search(text)
    year = "20" + ship_se.group(3)
    return year


def packing_slip_shipment_no(text):
    to_start = find_to_start(text)
    ship_start = ship_date_location(text)
    ship_date_text = text[to_start:ship_start]
    ship_no_regex = re.compile(r'\b\d{5}\b')
    ship_no = ship_no_regex.findall(ship_date_text)

    if '14600' or '84065' in ship_no:
        ship_no = [x for x in ship_no if x not in ['14600', '84065']]

    return min(ship_no)
    # else:
    #     return ship_no[0]


def company_text(text):
    '''
    Returns the Company Name
    '''
    bill = re.compile(r'\bBill\b')
    bill_end = bill.search(text).end()
    to = re.compile(r'\bTo\b')
    to_start = to.search(text).start()
    ship = re.compile(r'\bShip\b')
    ship_start = ship.search(text).start()

    if to_start > ship_start:
        company_name = text[bill_end:ship_start]
    else:
        company_name = text[bill_end:to_start]
    try:
        n_search_regex = re.compile(r'\n')
        n_search = n_search_regex.search(company_name).start()
        company_name = company_name.strip()
        company_name = company_name[:n_search]
    except Exception:
        pass

    company_name = company_name.strip()

    return company_name


def file_name(text):
    shipment_no = packing_slip_shipment_no(text)
    date = ship_date(text)
    new_pdfname = shipment_no + "_" + date
    return new_pdfname
