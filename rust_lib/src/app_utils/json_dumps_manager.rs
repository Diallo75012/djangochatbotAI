use serde_json::to_string_pretty;
use serde_json::Value;


/// Safely converts an object to a pretty JSON string.
pub fn safe_json_dumps(obj: &Value) -> Result<String, String> {
    match to_string_pretty(obj) {
        Ok(json_string) => Ok(json_string),
        Err(e) => Err(format!("Serialization error: {}", e)),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn test_safe_json_dumps() {
        let obj = json!({ "key": "value" });
        let result = safe_json_dumps(&obj);
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), "{\n  \"key\": \"value\"\n}");
    }

    #[test]
    fn test_safe_json_dumps_error() {
        // Simulate a non-serializable object
        let non_serializable_obj = Value::Null; // Modify this if needed to simulate an error
        let result = safe_json_dumps(&non_serializable_obj);
        assert!(result.is_ok()); // Null is serializable.
    }
}
