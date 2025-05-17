def query(
    db,
    table_name,
    columns=None,
    where=None,
    order_by=None,
    limit=None,
):
    """
    Query the database.

    Args:
        db: The database connection.
        table_name: The name of the table to query.
        columns: The columns to select. If None, select all columns.
        where: The WHERE clause. If None, no WHERE clause is added.
        order_by: The ORDER BY clause. If None, no ORDER BY clause is added.
        limit: The LIMIT clause. If None, no LIMIT clause is added.

    Returns:
        A list of rows from the query.
    """
    # Build the SQL query
    sql = f"SELECT {', '.join(columns) if columns else '*'} FROM {table_name}"
    params = []
    if where:
        sql += " WHERE " + where
        params.extend(where or [])
    if order_by:
        sql += f" ORDER BY {order_by}"
    if limit:
        sql += f" LIMIT {limit}"

    with db.cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchall()


def insert(
    db,
    table_name,
    data,
):
    """
    Insert data into the database.

    Args:
        db: The database connection.
        table_name: The name of the table to insert into.
        data: A dictionary of column names and values to insert.

    Returns:
        The ID of the inserted row.
    """
    if not data:
        raise ValueError("Data dictionary cannot be empty")
    # Build the SQL query
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    # Execute the query and commit the changes
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, tuple(data.values()))
            db.commit()
            return cursor.lastrowid
    except Exception as e:
        db.rollback()
        raise ValueError(f"Insert failed: {str(e)}")


def update(
    db,
    table_name,
    data,
    where,
):
    """
    Update data in the database.

    Args:
        db: The database connection.
        table_name: The name of the table to update.
        data: A dictionary of column names and values to update.
        where: The WHERE clause.

    Returns:
        The number of rows affected.
    """
    if not data:
        raise ValueError("Data dictionary cannot be empty")

    set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
    sql = f"UPDATE {table_name} SET {set_clause}"
    params = list(data.values())

    if where:
        sql += f" WHERE {where}"
        params.extend(where or [])

    try:
        with db.cursor() as cursor:
            cursor.execute(sql, params)
            db.commit()
            return cursor.rowcount
    except Exception as e:
        db.rollback()
        raise ValueError(f"Update failed: {str(e)}")


def delete(
    db,
    table_name,
    where,
):
    """
    Delete data from the database.

    Args:
        db: The database connection.
        table_name: The name of the table to delete from.
        where: The WHERE clause.

    Returns:
        The number of rows affected.
    """
    if not where:
        raise ValueError("WHERE clause is required for DELETE")

    sql = f"DELETE FROM {table_name} WHERE {where}"
    params = where or []

    try:
        with db.cursor() as cursor:
            cursor.execute(sql, params)
            db.commit()
            return cursor.rowcount
    except Exception as e:
        db.rollback()
        raise ValueError(f"Delete failed: {str(e)}")
