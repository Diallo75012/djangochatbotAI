use std::fs::OpenOptions;
use std::io::Write;

/*
  Rust logs are all writen to the root django project directory
  but will not rotate so need to create a cron job to rotate this file: 'logs/rust_logs.log'
  This script creates the file if it doesn't exist but we are going to create it anyways.
*/

/// Utility function to log debug information into a log file for troubleshooting.
pub fn log_debug_info(info: &str) {

  // Attempt to open the file with OpenOptions
  let file = OpenOptions::new()
    .create(true)   // Create the file if it doesn't exist
    .write(true)    // Open for writing
    .append(true)   // Append to the file if it exists
    .open("rust_logs.log");

  // Handle the result of attempting to open the file
  match file {
    Ok(mut log_file) => {
      // If the file opened successfully, attempt to write to it
      match writeln!(log_file, "{}", info) {
        Ok(_) => {
          // Successfully wrote to the file
          println!("Successfully logged information.");
        },
        Err(err) => {
          // Failed to write to the file
          eprintln!("Failed to write to log file: {}", err);
        },
      }
    },
    Err(err) => {
      // Failed to open the file
      eprintln!("An error occurred while trying to open the log file: {}", err);
    },
  }
}
