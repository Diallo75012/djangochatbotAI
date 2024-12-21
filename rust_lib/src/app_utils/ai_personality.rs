//just use this version using serde which makes the string_to_dict function redundant
use std::collections::HashMap;
use crate::app_utils::load_envs::load_env_variable;
use crate::logs_writer::log_debug_info;


/// Fills missing personality traits with default values.
/// Loads the default traits from an environment variable file.
pub fn personality_trait_formatting(
    mut trait_dict: HashMap<String, String>,
) -> Result<HashMap<String, String>, String> {
    // Load the default personality traits from the environment variable
    let default_traits = load_env_variable("../../.vars.env", "AI_PERSONALITY_TRAITS")?;
    log_debug_info(&format!("Check env var if loaded - default_traits: {:?}", default_traits));

    // Parse the default traits into a HashMap using serde_json
    let default_traits_map: HashMap<String, String> = serde_json::from_str(&default_traits)
        .map_err(|e| format!("Failed to parse AI_PERSONALITY_TRAITS: {}", e))?;
    log_debug_info(&format!("Default_traits_map: {:?}", default_traits_map));
    
    // Fill in missing or empty fields with default values
    for (key, value) in default_traits_map.iter() {
        if !trait_dict.contains_key(key) || trait_dict[key].is_empty() {
            trait_dict.insert(key.clone(), value.clone());
        }
    }

    Ok(trait_dict)
}
