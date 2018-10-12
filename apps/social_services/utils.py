def get_date_str_formatted(date):
    """
    Get date str in Ukrainian date format %d.%m.%Y or None.
    """
    return date.strftime('%d.%m.%Y') if date else None
