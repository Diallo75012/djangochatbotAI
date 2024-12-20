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

    tokio::spawn(async move {
        if let Err(e) = connection.await {
            eprintln!("Connection error: {}", e);
        }
    });

    let drop_table_query = format!("DROP TABLE IF EXISTS {}", collection_name);
    client
        .execute(&drop_table_query, &[])
        .await
        .map(|_| "Collection deleted successfully".to_string())
        .map_err(|e| format!("Error executing query: {}", e))
}
