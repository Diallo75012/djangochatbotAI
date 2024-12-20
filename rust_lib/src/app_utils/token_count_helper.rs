use std::sync::Mutex;
use std::collections::HashMap;
use tiktoken_rs::cl100k_base;
use tiktoken_rs::CoreBPE; // Import the correct encoder type
use lazy_static::lazy_static;

lazy_static! {
    // Global encoder cache with thread safety, shared across calls
    static ref ENCODER_CACHE: Mutex<HashMap<&'static str, Result<CoreBPE, String>>> = Mutex::new(HashMap::new());
}

/// Counts the number of tokens in a given text using a specific encoding.
pub fn token_counter(text_or_string_prompt: &str) -> Result<usize, String> {
    let encoding_name = "cl100k_base";

    // Safely lock the cache to ensure thread safety
    let mut cache = match ENCODER_CACHE.lock() {
        Ok(c) => c,
        Err(_) => return Err("Failed to lock encoder cache".to_string()),
    };

    // Retrieve or initialize the encoder for the given encoding name
    let encoder = cache.entry(encoding_name).or_insert_with(|| {
        // Attempt to initialize the encoder; use match to handle errors explicitly
        match cl100k_base() {
            Ok(encoder) => Ok(encoder),
            Err(e) => Err(format!("Failed to initialize encoder: {}", e)),
        }
    });

    // Use the encoder to count tokens, or propagate the error
    match encoder {
        Ok(encoder) => Ok(encoder.encode_ordinary(text_or_string_prompt).len()),
        Err(e) => Err(e.clone()), // Clone the error to ensure it’s properly returned
    }
}
