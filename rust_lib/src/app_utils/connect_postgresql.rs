use crate::app_utils::delete_embeddings::delete_embedding_collection;
use crate::app_utils::load_envs::load_env_relative;

/// Deletes a collection using environment variables and a provided connection string.
#[tokio::main]
pub async fn main() -> Result<(), String> {
  // Load environment variables
  load_env_relative("../../.env").map_err(|e| format!("Failed to load .env file: {}", e))?;

  // Define connection string and collection name
  let connection_string = "your_connection_string";
  let collection_name = "test_collection";

  // Call the function to delete the collection
  delete_embedding_collection(connection_string, collection_name)
    .await
    .map(|message| {
      println!("{}", message);
    })
    .map_err(|error| format!("Failed to delete collection: {}", error))
}
