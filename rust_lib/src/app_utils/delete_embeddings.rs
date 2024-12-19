use tokio_postgres::{Client, NoTls, Error};


pub async fn delete_embedding_collection(connection_string: &str, collection_name: &str) -> Result<String, String> {
  let cleaned_connection_string = connection_string.replace("+psycopg", "");

  // Connect to the PostgreSQL database
  let (client, connection) = match tokio_postgres::connect(&cleaned_connection_string, NoTls).await {
    Ok(conn) => conn,
    Err(e) => return Err(format!("Failed to connect to the database: {e}")),
  };

  // Spawn the connection in the background
  tokio::spawn(async move {
    if let Err(e) = connection.await {
      eprintln!("Database connection error: {e}");
    }
  });

  let drop_table_query = format!("DROP TABLE IF EXISTS \"{}\";", collection_name);

  // Execute the query
  match client.execute(&drop_table_query, &[]).await {
    Ok(_) => {
      println!("Collection '{}' has been deleted successfully.", collection_name);
      Ok("success".to_string())
    }
    Err(e) => {
      println!("An error occurred while deleting the collection: {e}");
      Err(format!("error: {e}"))
    }
  }
}
