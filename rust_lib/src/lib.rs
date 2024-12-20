mod app_utils;

use pyo3::prelude::*; 
use pyo3::exceptions::PyValueError;

use reqwest::blocking::Client;

use serde::{Serialize};

use std::fs::OpenOptions;
use std::io::Write;
use std::collections::HashMap;

use app_utils::load_envs::load_env_variable;
use app_utils::ai_personality::{string_to_dict, personality_trait_formatting};
//use app_utils::delete_embeddings::delete_embedding_collection;
// the `connect_postgresql::main is calling the delete_emdebbings::delete_embedding_collection under the hood 
use app_utils::connect_postgresql::main as delete_collection_main;
use app_utils::formatters::{string_to_dict as formatter_string_to_dict, collection_normalize_name};
use app_utils::token_count_helper::token_counter;


#[derive(Serialize, Debug)]
struct Message {
    role: String,
    content: String,
}

#[derive(Serialize, Debug)]
struct PayLoad {
    model: String,
    messages: Vec<Message>,
}

/// Utility function to log debug information into a log file for troubleshooting.
fn log_debug_info(info: &str) {

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


/// Function to call LLM API and return the raw response as a String.
#[pyfunction]
fn call_llm_api(api_url: &str, api_key: &str, message_content: &str, model: &str) -> PyResult<String> {
  // Instantiate client
  let client = Client::new();

  // Prepare payload message
  let message = Message {
    role: "user".to_string(),
    content: message_content.to_string(),
  };
  log_debug_info(&format!("Message: {:?}", message));

  // Put message in payload
  let payload = PayLoad {
    model: model.to_string(),
    messages: vec![message],
  };
  log_debug_info(&format!("Payload: {:?}", payload));

  // Serialize payload to JSON
  let payload_json = match serde_json::to_string(&payload) {
    Ok(json) => json,
    Err(err) => {
      return Err(
        pyo3::exceptions::PyRuntimeError::new_err(
          format!("Failed to serialize payload: {}", err)
        )
      );
    }
  };
  log_debug_info(&format!("Payload JSON: {:?}", payload_json));

  // Call API with headers and body payload
  let response = client
    .post(api_url)
    .header("Authorization", format!("Bearer {}", api_key))
    .header("Content-Type", "application/json")
    .body(payload_json)
    .send();
  log_debug_info(&format!("Response: {:?}", response));

  // Use `match` to handle response
  match response {
    Ok(resp) => match resp.text() {
      Ok(text) => Ok(text),
      Err(text_err) => Err(
        pyo3::exceptions::PyRuntimeError::new_err(
          format!("Failed to read response text: {}", text_err)
        )
      ),
    },
    Err(err) => Err(
      pyo3::exceptions::PyRuntimeError::new_err(
        format!("API request failed: {}", err)
      )
    ),
  }
}

#[pyfunction]
fn load_personality(env_var_name: &str, input: &str) -> PyResult<HashMap<String, String>> {
  match string_to_dict(input) {
    Ok(dict) => personality_trait_formatting(dict, env_var_name)
             .map_err(|e| pyo3::exceptions::PyValueError::new_err(e)),
    Err(e) => Err(pyo3::exceptions::PyValueError::new_err(e)),
  }
}

#[pyfunction]
fn delete_collection_py() -> PyResult<()> {
  match delete_collection_main() {
    Ok(_) => Ok(()),
    Err(e) => Err(PyValueError::new_err(format!("Failed to delete collection: {}", e))),
  }
}

#[pyfunction]
fn load_env_variable_py(env_file_path: &str, env_var_name: &str) -> PyResult<String> {
  match load_env_variable(env_file_path, env_var_name) {
    Ok(value) => Ok(value),
    Err(error_message) => Err(PyValueError::new_err(error_message)),
  }
}

#[pyfunction]
fn string_to_dict_py(input: &str) -> PyResult<HashMap<String, String>> {
  match string_to_dict(input) {
    Ok(map) => Ok(map),
    Err(error_message) => Err(PyValueError::new_err(error_message)),
  }
}

#[pyfunction]
fn formatter_string_to_dict_py(input: &str) -> PyResult<HashMap<String, String>> {
  match formatter_string_to_dict(input) {
    Ok(map) => Ok(map),
    Err(error_message) => Err(PyValueError::new_err(error_message)),
  }
}

#[pyfunction]
fn collection_normalize_name_py(collection_name: &str) -> PyResult<String> {
  Ok(collection_normalize_name(collection_name))
}

#[pyfunction]
fn token_counter_py(text_or_string_prompt: &str) -> PyResult<usize> {
  match token_counter(text_or_string_prompt) {
    Ok(count) => Ok(count),
    Err(error_message) => Err(PyValueError::new_err(error_message)),
  }
}

/// A Python module implemented in Rust.
// this module name has to be same as 
// project folder name `my_rust_extension`
#[pymodule]
fn rust_lib(m: &Bound<'_, PyModule>) -> PyResult<()> {
  m.add_function(wrap_pyfunction!(call_llm_api, m)?)?;
  m.add_function(wrap_pyfunction!(load_personality, m)?)?;
  m.add_function(wrap_pyfunction!(delete_collection_py, m)?)?;
  m.add_function(wrap_pyfunction!(load_env_variable_py, m)?)?;
  m.add_function(wrap_pyfunction!(string_to_dict_py, m)?)?;
  m.add_function(wrap_pyfunction!(formatter_string_to_dict_py, m)?)?;
  m.add_function(wrap_pyfunction!(collection_normalize_name_py, m)?)?;
  m.add_function(wrap_pyfunction!(token_counter_py, m)?)?;
  Ok(())
}
