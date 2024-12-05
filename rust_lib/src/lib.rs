use pyo3::prelude::*; 
use reqwest::blocking::Client;
use serde::{Serialize};
use std::fs::OpenOptions;
use std::io::Write;

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
    let mut file = OpenOptions::new()
        .create(true)
        .write(true)
        .append(true)
        .open("rust_debug.log")
        .unwrap();
    writeln!(file, "{}", info).unwrap();
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

/// A Python module implemented in Rust.
// this module name has to be same as 
// project folder name `my_rust_extension`
#[pymodule]
fn rust_lib(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(call_llm_api, m)?)?;
    Ok(())
}
