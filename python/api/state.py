from flask import Response, request
from python.helpers.api import ApiHandler
from python.helpers.state_manager import get_state_manager
import json

class State(ApiHandler):
    async def handle_request(self, request):
        if request.method == "GET":
            return await self.get_gob_state()
        elif request.method == "POST" and request.path.endswith("/connection"):
            return await self.update_connection_status(request)
        else:
            return Response(
                json.dumps({"error": "Method not allowed"}),
                status=405,
                mimetype="application/json"
            )
    
    async def get_gob_state(self):
        """Get current GOB state"""
        try:
            state_manager = get_state_manager()
            state_data = state_manager.get_state_for_ui()
            
            return Response(
                json.dumps(state_data, indent=2),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
                json.dumps({"error": str(e)}),
                status=500,
                mimetype="application/json"
            )
    
    async def update_connection_status(self, request):
        """Update connection status"""
        try:
            data = await request.get_json()
            status = data.get("status")
            
            if status not in ["online", "offline", "away"]:
                return Response(
                    json.dumps({"error": "Invalid status"}),
                    status=400,
                    mimetype="application/json"
                )
            
            state_manager = get_state_manager()
            state_manager.set_connection_status(status)
            
            return Response(
                json.dumps({"success": True, "status": status}),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
                json.dumps({"error": str(e)}),
                status=500,
                mimetype="application/json"
            )
