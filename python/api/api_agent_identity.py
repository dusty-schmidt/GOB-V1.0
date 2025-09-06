"""
API endpoint for agent identity and naming information
"""

import json
from datetime import datetime, date
from flask import Request, Response
from python.helpers.api import ApiHandler
from python.helpers.naming_service import get_naming_service


class api_agent_identity(ApiHandler):
    """API handler for agent identity and naming"""
    
    @staticmethod
    def requires_auth():
        return True  # Require authentication for this endpoint
    
    @staticmethod
    def requires_loopback():
        return False  # Allow external access if authenticated
    
    @staticmethod 
    def requires_api_key():
        return False  # Use standard auth instead of API key
    
    @staticmethod
    def requires_csrf():
        return True  # Require CSRF protection
    
    @staticmethod
    def get_methods():
        return ["GET", "POST"]
    
    async def handle_request(self, request: Request) -> Response:
        """Handle agent identity requests"""
        try:
            naming_service = get_naming_service()
            
            if request.method == "GET":
                # GET request - return current main agent identity
                identity = naming_service.get_full_agent_identity("main")
                
                response_data = {
                    "status": "success",
                    "agent_identity": identity,
                    "timestamp": datetime.now().isoformat()
                }
                
                return Response(
                    json.dumps(response_data, indent=2),
                    content_type="application/json",
                    status=200
                )
            
            elif request.method == "POST":
                # POST request - allow querying specific agent types or dates
                data = request.get_json() or {}
                
                agent_type = data.get("agent_type", "main")
                context_id = data.get("context_id")
                date_str = data.get("date")
                
                # Parse date if provided
                query_date = None
                if date_str:
                    try:
                        query_date = datetime.fromisoformat(date_str.replace("Z", "+00:00")).date()
                    except (ValueError, AttributeError):
                        try:
                            query_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                        except ValueError:
                            return Response(
                                json.dumps({
                                    "status": "error",
                                    "message": "Invalid date format. Use ISO format or YYYY-MM-DD"
                                }),
                                content_type="application/json",
                                status=400
                            )
                
                # Get identity information
                if agent_type.lower() == "main":
                    identity = naming_service.get_full_agent_identity("main", date=query_date)
                else:
                    identity = naming_service.get_full_agent_identity(agent_type, context_id=context_id)
                
                # For batch requests, allow multiple agent queries
                if "agents" in data:
                    identities = []
                    for agent_request in data["agents"]:
                        agent_type = agent_request.get("type", "main")
                        context_id = agent_request.get("context_id")
                        agent_date = agent_request.get("date")
                        
                        # Parse agent-specific date
                        agent_query_date = None
                        if agent_date:
                            try:
                                agent_query_date = datetime.fromisoformat(agent_date.replace("Z", "+00:00")).date()
                            except (ValueError, AttributeError):
                                try:
                                    agent_query_date = datetime.strptime(agent_date, "%Y-%m-%d").date()
                                except ValueError:
                                    continue  # Skip invalid date entries
                        
                        if agent_type.lower() == "main":
                            agent_identity = naming_service.get_full_agent_identity("main", date=agent_query_date)
                        else:
                            agent_identity = naming_service.get_full_agent_identity(agent_type, context_id=context_id)
                        
                        identities.append(agent_identity)
                    
                    response_data = {
                        "status": "success",
                        "agent_identities": identities,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    response_data = {
                        "status": "success", 
                        "agent_identity": identity,
                        "timestamp": datetime.now().isoformat()
                    }
                
                return Response(
                    json.dumps(response_data, indent=2),
                    content_type="application/json",
                    status=200
                )
        
        except Exception as e:
            return Response(
                json.dumps({
                    "status": "error",
                    "message": f"Failed to get agent identity: {str(e)}"
                }),
                content_type="application/json",
                status=500
            )
