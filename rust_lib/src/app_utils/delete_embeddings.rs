use tokio_postgres::NoTls;


/// Deletes the specified table (collection) from PostgreSQL.
pub async fn delete_embedding_collection(
    connection_string: &str,
    collection_name: &str,
) -> Result<String, String> {
    let connection_string = connection_string.replace("postgresql+psycopg", "postgresql");

    let (client, connection) = tokio_postgres::connect(&connection_string, NoTls)
        .await
        .map_err(|e| format!("Connection error: {}", e))?;
    // so here we spawn the connection to have it running
    tokio::spawn(async move {
        if let Err(e) = connection.await {
            eprintln!("Connection error: {}", e);
        }
    });

    // now that connection is running we can try to drop the collection by creating the sql query
    // we will use the semi-colon `;` even if our friend told us that it is not required
    // ChatGPT: "Database Drivers (like tokio-postgres): A semicolon is not required.
    // The query string is sent directly to the database server, which can process it without the semicolon."
    /*
    let drop_table_query = format!("DELETE FROM langchain_pg_collection where name='{}';", collection_name);
    client
        .execute(&drop_table_query, &[])
        .await
        .map(|_| "Collection deleted successfully".to_string())
        .map_err(|e| format!("Error executing query: {}", e))
    */
    // We use parameterized Queries (Recommended): For better security (to avoid SQL injection) and efficiency
    let delete_collection_query = "DELETE FROM langchain_pg_collection WHERE name = $1;";
    client
      .execute(delete_collection_query, &[&collection_name])
      .await
      .map(|_| "success".to_string())
      .map_err(|e| format!("Error executing query: {}", e))

}
