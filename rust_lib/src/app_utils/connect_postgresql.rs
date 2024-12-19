use crate::app_utils::delete_embeddings::delete_embedding_collection;
use crate::app_utils::load_envs::load_env_relative;


#[tokio::main]
async fn main() {
    // Load environment variables
    load_env_relative("../../.env").expect("Failed to load .env file");

    // Define connection string and collection name
    let connection_string = "your_connection_string";
    let collection_name = "test_collection";

    // Call the function to delete the collection
    match delete_embedding_collection(connection_string, collection_name).await {
        Ok(message) => println!("{}", message),
        Err(error) => eprintln!("{}", error),
    }
}
