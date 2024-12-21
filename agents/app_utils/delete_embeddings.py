import psycopg
from rust_lib import delete_collection_py

# using rust counterpart to do the job of deleting collection
def delete_embedding_collection(connection_string: str, collection_name: str):
  try:
    rust_delete_collection = delete_collection_py(connection_string, collection_name)
    print(f"Collection '{collection_name}' has been deleted successfully. Rust response: {rust_delete_collection}")
    return "success"
  except Exception as e:
    print(f"An error occurred while deleting the collection: {e}")
    return f"error: {e}"

'''
def delete_embedding_collection(connection_string: str, collection_name: str):
  """
  Deletes the specified embedding collection (table) from the PostgreSQL database.

  Parameters:
  - connection_string (str): The connection string for the PostgreSQL database.
  - collection_name (str): The name of the collection (table) to delete.
  """
  drop_table_query = f"DROP TABLE IF EXISTS {collection_name};"

  # Remove "+driver" if present in the connection string
  connection_string = connection_string.replace("postgresql+psycopg", "postgresql")

  try:
    with psycopg.connect(connection_string) as conn:
      with conn.cursor() as cur:
        cur.execute(drop_table_query)
        conn.commit()
    print(f"Collection '{collection_name}' has been deleted successfully.")
    return "success"
  except Exception as e:
    print(f"An error occurred while deleting the collection: {e}")
    return f"error: {e}"
'''
