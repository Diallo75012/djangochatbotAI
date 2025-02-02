use dotenv::from_path;
use std::env;
use std::path::Path;
use std::error::Error;

/// Loads the `.env` file using a relative path. This is for when need to load the file entirely
pub fn load_env_relative(var_file_dotted_path: &str) -> Result<(), Box<dyn Error>> {
  let current_dir = env::current_dir()?;
  let relative_path = Path::new(var_file_dotted_path); // Adjust this as needed
  let env_file_path = current_dir.join(relative_path);

  if env_file_path.exists() {
    from_path(&env_file_path)?;
    println!("Environment variables loaded from: {:?}", env_file_path);
    Ok(())
  } else {
    Err(format!("Could not find .env file at {:?}", env_file_path).into())
  }
}

// this is used when need to load an env file and get specific env var value
pub fn load_env_variable(env_file_path: &str, env_var_name: &str) -> Result<String, String> {
    // Load environment variables from the specified file path
    if let Err(e) = load_env_relative(env_file_path) {
        return Err(format!("Failed to load .env file from path '{}': {e}", env_file_path));
    }

    // Retrieve the specified environment variable
    match std::env::var(env_var_name) {
        Ok(value) => Ok(value),
        Err(_) => Err(format!("Environment variable '{}' is not set or accessible.", env_var_name)),
    }
}
