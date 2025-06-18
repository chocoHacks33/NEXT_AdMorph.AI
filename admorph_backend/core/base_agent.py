"""
Base agent classes for AdMorph.AI agentic framework
"""

import asyncio
import json
import os
import requests
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime


class BaseAgent(ABC):
    """Base class for all AdMorph agents"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.created_at = datetime.now().isoformat()
        self.execution_history = []
    
    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main functionality"""
        pass
    
    def log_execution(self, context: Dict[str, Any], result: Dict[str, Any]):
        """Log agent execution for monitoring"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_name": self.agent_name,
            "context_keys": list(context.keys()) if context else [],
            "result_keys": list(result.keys()) if result else [],
            "success": result.get("success", True)
        }
        self.execution_history.append(log_entry)
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """Get agent execution statistics"""
        total_executions = len(self.execution_history)
        successful_executions = sum(1 for entry in self.execution_history if entry["success"])
        
        return {
            "agent_name": self.agent_name,
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "success_rate": successful_executions / total_executions if total_executions > 0 else 0,
            "created_at": self.created_at,
            "last_execution": self.execution_history[-1]["timestamp"] if self.execution_history else None
        }


class OpenAIAgent(BaseAgent):
    """Base agent with OpenAI integration"""
    
    def __init__(self, agent_name: str, model: str = "gpt-4"):
        super().__init__(agent_name)
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.base_url = "https://api.openai.com/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
    
    async def _call_openai(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        timeout: int = 30
    ) -> str:
        """Make async call to OpenAI API"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }
        
        if max_tokens:
            data["max_tokens"] = max_tokens
        
        try:
            # Use requests for now, can be replaced with aiohttp for true async
            response = requests.post(
                self.base_url, 
                headers=headers, 
                json=data, 
                timeout=timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                error_msg = f"OpenAI API error: {response.status_code} - {response.text}"
                raise Exception(error_msg)
                
        except requests.exceptions.Timeout:
            raise Exception("OpenAI API request timed out")
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenAI API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error calling OpenAI: {str(e)}")
    
    def _create_system_message(self, system_prompt: str) -> Dict[str, str]:
        """Create system message for OpenAI"""
        return {"role": "system", "content": system_prompt}
    
    def _create_user_message(self, user_prompt: str) -> Dict[str, str]:
        """Create user message for OpenAI"""
        return {"role": "user", "content": user_prompt}
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON response from OpenAI"""
        try:
            # Try to find JSON in the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # If no JSON found, try parsing the entire response
                return json.loads(response)
                
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON response: {str(e)}\nResponse: {response}")
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Base execute method - should be overridden by subclasses"""
        result = {"success": False, "error": "execute method not implemented"}
        self.log_execution(context, result)
        return result
