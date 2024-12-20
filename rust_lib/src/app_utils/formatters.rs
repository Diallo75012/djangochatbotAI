use std::collections::HashMap;


/// Converts a JSON string to a HashMap with lowercase keys.
pub fn string_to_dict(input: &str) -> Result<HashMap<String, String>, String> {
    serde_json::from_str::<HashMap<String, String>>(input)
        .map(|map| map.into_iter().map(|(k, v)| (k.to_lowercase(), v)).collect())
        .map_err(|e| format!("Error converting string to dictionary: {}", e))
}

/// Normalizes collection names by replacing spaces with dashes and converting to lowercase.
pub fn collection_normalize_name(collection_name: &str) -> String {
    collection_name.trim().replace(' ', "-").to_lowercase()
}
