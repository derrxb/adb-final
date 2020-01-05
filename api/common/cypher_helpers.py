from flask import request


def page():
    """Returns the page size for queries"""
    page = int(request.args.get('page') or 0)
    adjusted_page = page - 1

    return adjusted_page if adjusted_page >= 1 else 0


def page_size():
    """Returns the page size for queries"""
    page_size = int(request.args.get('page_size') or 30)

    return page_size if page_size >= 1 else 10


def page_number():
    """Determines the `skip` criteria for Cypher queries"""
    return 0 if page() == 0 else page() * page_size()
