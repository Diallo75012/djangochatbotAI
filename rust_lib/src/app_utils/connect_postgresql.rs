use crate::app_utils::delete_embeddings::delete_embedding_collection;
//use crate::app_utils::load_envs::load_env_relative;

/// Deletes a collection using environment variables and a provided connection string.
#[tokio::main]
pub async fn db_connect(connection_string: &str, collection_name: &str) -> Result<String, String> {
  // Load environment variables
  //load_env_relative("../../.env").map_err(|e| format!("Failed to load .env file: {}", e))?;

  // Call the function to delete the collection
  delete_embedding_collection(connection_string, collection_name)
    .await
    .map(|message| {
      println!("{}", message);
      message.to_string()
    })
    .map_err(|error| {
      println!("Failed to delete collection: {}", error); 
      error.to_string()
    })
}
