use pyo3::prelude::*;
use reqwest::blocking::Client;
use serde::{Deserialize, Serialize};
//use std::error::Error;


// we could use struct to serialize and deserialize
// and get JSON responses which is easier to send and work in Python side
// eg.:
#[derive(Serialize, Deserialize, Debug)]
struct ApiResponse {
  message: String,
  status: u64,
}

/// function to parse a response into `ApiResponse` struct
fn parse_response(
  response: &str
) -> Result<ApiResponse, serde_json::Error> {
  // here the type is the one of the struct ApiResponse
  let parsed: ApiResponse = serde_json::from_str(
    response
  )?;
  Ok(parsed)
}

/// Function to call groq/ollama or any llm api
#[pyfunction]
fn call_llm_api(
  api_url: &str, api_key: &str, payload: &str
) -> PyResult<String> {
  // instantiate client
  let client = Client::new();

  // convert payload to owned String to avoid lifetime issues
  let payload_owned = payload.to_string();

  // call api with header, body payload
  let response = client
    .post(api_url)
    .header("Authorization", format!("Bearer {}", api_key))
    .header("Content-Type", "application/json")
    .body(payload_owned)
    .send();

  // use `match` statement to handle response `no unwrap()` to not crash app
  match response {
    Ok(resp) => {
      match resp.text() {
        Ok(text) => {
          // parse the response using serde
          match parse_response(&text) {
            Ok(parsed_response) => {
              Ok(
                format!(
                  "Message: {}m status: {}",
                  parsed_response.message,
                  parsed_response.status
                )
              )
            },
            Err(parse_err) => Err(
              pyo3::exceptions::PyRuntimeError::new_err(
                format!(
                  "Failed to parse response: {}",
                  parse_err
                )
              )
            ),
          }
        },
        Err(text_err) => Err(
          pyo3::exceptions::PyRuntimeError::new_err(
            format!(
              "Failed to read response text: {}",
              text_err
            ) 
          )
        ),
      }
    },
    Err(err) => Err(
      pyo3::exceptions::PyRuntimeError::new_err(
        format!(
          "API request failed: {}",
          err
        )
      )
    ),    
  }
}


/// A Python module implemented in Rust.
// this module name has to be same as 
// project folder name `my_rust_extension`
#[pymodule]
fn rust_lib(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(call_llm_api, m)?)?;
    Ok(())
}
