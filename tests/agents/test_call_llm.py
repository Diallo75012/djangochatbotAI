import pytest                                                                                                                                                                       
from unittest.mock import MagicMock, patch                                                                                                                                          
import os                                                                                                                                                                           
from dotenv import load_dotenv                                                                                                                                                      
from agents.app_utils.call_llm import call_llm                                                                                                                                      
from langchain_core.messages import AIMessage                                                                                                                                       
from agents.llms.llms import groq_llm_mixtral_7b                                                                                                                                    
from agents.structured_output.structured_output import analyse_user_query_safety_schema                                                                                             
from agents.prompts.prompts import answer_to_user_prompt, analyse_user_query_safety_prompt                                                                                          
from agents.app_utils.ai_personality import personality_trait_formatting                                                                                                            
                                                                                                                                                                                     
                                                                                                                                                                                     
# load env vars                                                                                                                                                                     
load_dotenv(dotenv_path='.env', override=False)                                                                                                                                     
load_dotenv(dotenv_path=".vars.env", override=True)                                                                                                                                 
                                                                                                                                                                                     
def _test_call_llm(query, prompt_template_part, schema, expected_keys=None, expected_values=None):                                                                                  
    try:                                                                                                                                                                            
        result = call_llm(query, prompt_template_part, schema, groq_llm_mixtral_7b)                                                                                                 
        assert isinstance(result, (dict, str))                                                                                                                                      
        if isinstance(result, dict):                                                                                                                                                
            if expected_keys:                                                                                                                                                       
                for key in expected_keys:                                                                                                                                           
                    assert key in result                                                                                                                                            
            if expected_values:                                                                                                                                                     
                for key, value in expected_values.items():                                                                                                                          
                    assert key in result                                                                                                                                            
                    assert result[key] == value                                                                                                                                     
    except Exception as e:                                                                                                                                                          
        pytest.fail(f"Test failed with exception: {e}")                                                                                                                             
                                                                                                                                                                                     
def test_call_llm_successful_response():                                                                                                                                            
    query = "This is a test query to check safety."                                                                                                                                 
    prompt_template_part = analyse_user_query_safety_prompt["system"]["template"]                                                                                                   
    schema = analyse_user_query_safety_schema                                                                                                                                       
    _test_call_llm(query, prompt_template_part, schema, expected_keys=["safe", "unsafe"])                                                                                           
                                                                                                                                                                                     
def test_call_llm_safety_schema_valid_response():                                                                                                                                   
    query = "This is a test query to check safety."                                                                                                                                 
    prompt_template_part = analyse_user_query_safety_prompt["system"]["template"]                                                                                                   
    schema = analyse_user_query_safety_schema                                                                                                                                       
    _test_call_llm(query, prompt_template_part, schema, expected_values={"safe": "valid"})                                                                                          
                                                                                                                                                                                    
def test_call_llm_answer_prompt_valid_response():                                                                                                                                   
    query = "test query"                                                                                                                                                            
    prompt_template_part = answer_to_user_prompt["system"]["template"]                                                                                                                                                                                                                        
    ai_personality_traits = {"chatbot_name": "test", "chatbot_description": "test", "chatbot_age": "test", "chatbot_origin": "test", "chatbot_dream": "test", "chatbot_tone": "test", "chatbot_expertise": "test"}                                                                                                                                                        
    # formatted_ai_personality_traits = personality_trait_formatting(ai_personality_traits) # need to check why can't fetch env var in helper function when it working when printing using subprocess...                                                                                                                                                                 
    formatted_ai_personality_traits = {"chatbot_name": "test", "chatbot_description": "test", "chatbot_age": "test", "chatbot_origin": "test", "chatbot_dream": "test", "chatbot_tone": "test", "chatbot_expertise": "test"}
    prompt = answer_to_user_prompt["system"]["template"].format(**{"ai_personality_traits": formatted_ai_personality_traits})                                                       
    _test_call_llm(query, prompt, analyse_user_query_safety_schema, expected_keys=["safe","unsafe"],)                                                                                                                
                                                                                                                                                                                     
def test_call_llm_error_handling():                                                                                                                                                 
    query = "test query"                                                                                                                                                            
    prompt_template_part = "test prompt"                                                                                                                                            
    schema = analyse_user_query_safety_schema # this will cause an error as it is not a valid prompt                                                                                
    with pytest.raises(Exception, match="An error occured while calling llm: Error converting string to dictionary: expected value at line 1 column 1"):                            
        call_llm(query, prompt_template_part, schema, groq_llm_mixtral_7b) 
