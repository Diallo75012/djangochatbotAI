use std::sync::Mutex;
use std::collections::HashMap;
use tiktoken_rs::get_encoding;


lazy_static::lazy_static! {
    static ref ENCODER_CACHE: Mutex<HashMap<&'static str, Result<tiktoken_rs::Encoding, String>>> = Mutex::new(HashMap::new());
}

/// Counts the number of tokens in a given text using a specific encoding.
pub fn token_counter(text_or_string_prompt: &str) -> Result<usize, String> {
    let encoding_name = "cl100k_base";

    let cache = match ENCODER_CACHE.lock() {
        Ok(c) => c,
        Err(_) => return Err("Failed to lock encoder cache".to_string()),
    };

    let encoder = cache
        .entry(encoding_name)
        .or_insert_with(|| get_encoding(encoding_name).map_err(|e| format!("Failed to get encoding: {}", e)));

    match encoder {
        Ok(encoder) => Ok(encoder.encode_ordinary(text_or_string_prompt).len()),
        Err(e) => Err(e.clone()),
    }
}
