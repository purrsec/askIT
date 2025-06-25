import requests
import json
from .base_provider import AIBaseProvider


class ClaudeProvider(AIBaseProvider):
    """
    Provider implementation for Anthropic Claude.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-3-5-sonnet-20241022"  # Default model
        self.max_tokens = 1024  # Reduced from 4096 to save tokens

    def get_suggestion(self, prompt: str, context: str) -> tuple[str, str, str]:
        """
        Queries the Claude API to get a command suggestion.
        
        Returns:
            tuple: (confidence_level, command, explanation)
        """
        full_prompt = self._prepare_prompt(prompt, context)

        try:
            response = self._call_claude_api(full_prompt)
            return self._parse_response(response)
        except Exception as e:
            return ("LOW", "", f"❌ Error calling Claude API: {str(e)}\n\n💡 Fallback suggestion: Consider checking the command manually.")

    def _parse_response(self, response: str) -> tuple[str, str, str]:
        """
        Parse Claude's structured response to extract confidence, command, and explanation.
        
        Returns:
            tuple: (confidence_level, command, explanation)
        """
        try:
            lines = response.strip().split('\n')
            confidence = "LOW"
            command = ""
            explanation = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith("CONFIDENCE:"):
                    confidence = line.replace("CONFIDENCE:", "").strip().upper()
                elif line.startswith("COMMAND:"):
                    command = line.replace("COMMAND:", "").strip()
                elif line.startswith("EXPLANATION:"):
                    explanation = line.replace("EXPLANATION:", "").strip()
                    # Collect remaining lines as part of explanation
                    idx = lines.index(line)
                    if idx < len(lines) - 1:
                        remaining = '\n'.join(lines[idx+1:]).strip()
                        if remaining:
                            explanation += '\n' + remaining
                    break
            
            # Validate confidence level
            if confidence not in ["HIGH", "MEDIUM", "LOW", "NONE", "AGENT"]:
                confidence = "LOW"
                
            return (confidence, command, explanation)
            
        except Exception:
            # If parsing fails, return the original response as explanation
            return ("LOW", "", response)

    def _call_claude_api(self, prompt: str) -> str:
        """
        Make the actual API call to Claude.
        """
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        
        # Prepare system message for command generation
        system_message = """You are an expert system administrator helping users with command-line tasks. You must provide accurate, executable commands with a confidence assessment.

CRITICAL: You must respond in this EXACT format:

CONFIDENCE: [HIGH|MEDIUM|LOW|NONE|AGENT]
COMMAND: [the exact command to execute, or empty if confidence is NONE or AGENT]
EXPLANATION: [brief explanation, clarifying question, or agent's proposed plan]

CONFIDENCE LEVELS:
- HIGH: You are 100% certain this is the correct, safe command for the user's request
- MEDIUM: You are confident but there might be variations or context-specific considerations  
- LOW: You have suggestions but aren't completely sure or need more context
- NONE: You do not understand the request or cannot provide a useful command. Ask a clarifying question in the EXPLANATION.
- AGENT: The request is complex and requires multiple steps (e.g., file creation, multiple commands). Propose a plan in the EXPLANATION.

RESPONSE RULES:
1. Always start with "CONFIDENCE:" followed by HIGH, MEDIUM, LOW, NONE, or AGENT
2. Follow with "COMMAND:" and the exact command the user should run. If confidence is NONE or AGENT, this should be empty.
3. To request user input for a variable, use the format `{{USER_INPUT:Question for the user}}`. The agent will ask the user for this information.
4. For file creation, use the format `FILE: path/to/your/file.ext` on a new line, immediately followed by a markdown code block with the file's content.
5. End with "EXPLANATION:" and a very concise, one-sentence explanation (under 15 words). If confidence is NONE, ask a question instead.
6. Keep commands simple and directly executable
7. For HIGH confidence: provide ONE clear command
8. For MEDIUM/LOW confidence: you can suggest alternatives
9. Consider the user's shell environment and current directory
10. For system-level directories (e.g., `/etc`, `C:\\Windows`), always use absolute paths.
11. CRITICAL FOR POWERSHELL: Paths with special characters (like `$` or spaces) MUST be in SINGLE QUOTES (`'`) to be treated literally. For example, to access the Recycle Bin, the path MUST be `'C:\\$Recycle.Bin'`. Using double quotes (`"`) is INCORRECT and will cause an error. For hidden files, use the `-Force` flag.
12. Avoid dangerous operations unless explicitly requested
13. The EXPLANATION must be in the same language as the "User Request".

EXAMPLE (Success):
CONFIDENCE: HIGH
COMMAND: ls -la *.txt
EXPLANATION: Lists all .txt files in the current directory with details.

EXAMPLE (French Request):
CONFIDENCE: HIGH
COMMAND: ls -l
EXPLANATION: Liste les fichiers et dossiers du répertoire avec leurs détails.

EXAMPLE (Agent Task):
CONFIDENCE: AGENT
COMMAND:
EXPLANATION: I will create a new Python project. Here is the plan:

First, create the directory structure:
```bash
mkdir -p {{USER_INPUT:Enter the project name}}
```

Next, create the main file.
FILE: {{USER_INPUT:Enter the project name}}/src/main.py
```python
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
```

EXAMPLE (Needs clarification):
CONFIDENCE: NONE
COMMAND:
EXPLANATION: I'm not sure what kind of 'cleanup' you're referring to. Could you please specify if you want to remove temporary files, clear a cache, or something else?

The user is working in their current directory context."""

        data = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "system": system_message,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            # Extract the response content
            if 'content' in response_data and len(response_data['content']) > 0:
                return response_data['content'][0]['text']
            else:
                return "No response received from Claude API."
                
        except requests.exceptions.Timeout:
            raise Exception("Request to Claude API timed out")
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('error', {}).get('message', str(e))
                    raise Exception(f"Claude API error: {error_msg}")
                except:
                    raise Exception(f"Claude API error: {e.response.status_code} - {e.response.text}")
            else:
                raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("Invalid JSON response from Claude API")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")

    def _prepare_prompt(self, prompt: str, context: str) -> str:
        """
        Prepare the full prompt for Claude with context and specific instructions.
        """
        return f"""Context:
{context}

User Request: {prompt}

Please provide the appropriate command(s) to fulfill this request. Consider the context provided above, especially the recent shell history which shows what the user has been working on recently.""" 