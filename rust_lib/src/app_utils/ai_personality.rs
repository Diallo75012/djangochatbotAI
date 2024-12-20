use std::collections::HashMap;
use std::env;

/// Converts a string to a HashMap with lowercase keys.
pub fn string_to_dict(input: &str) -> Result<HashMap<String, String>, String> {
    serde_json::from_str::<HashMap<String, String>>(input)
        .map(|map| map.into_iter().map(|(k, v)| (k.to_lowercase(), v)).collect())
        .map_err(|e| format!("Error converting string to dictionary: {}", e))
}

/// Fills missing personality traits with default values.
pub fn personality_trait_formatting(
    trait_dict: HashMap<String, String>,
    default_env_var: &str,
) -> Result<HashMap<String, String>, String> {
    let default_traits = env::var(default_env_var)
        .map_err(|_| "Environment variable DEFAULT_AI_PERSONALITY_TRAIT not found".to_string())?;
    let default_traits_map = string_to_dict(&default_traits)?;

    let mut updated_traits = trait_dict.clone();
    for (key, value) in default_traits_map.iter() {
        if !updated_traits.contains_key(key) || updated_traits[key].is_empty() {
            updated_traits.insert(key.clone(), value.clone());
        }
    }
    Ok(updated_traits)
}
