
def clear_db(driver):
    """Removes all the records from the database to give you a clean slate"""
    session = driver.session()

    session.run("MATCH(n) OPTIONAL MATCH(n)-[r]-() DELETE n, r")

    session.close()

    print("Successfully removed Data and Relationships from database")
