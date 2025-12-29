import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langchain_core.messages import ToolMessage
import json


SERVERS = { 
    "expense": {
        "transport": "stdio",
        "command": "/home/omkar/.local/bin/uv", #using which uv : uv installation full path
        "args": [
            "run",
            "fastmcp",
            "run",
            "/mnt/c/Users/hp/Desktop/MCP/db_server/dbserver_mcp/main.py" # full path
        ]
    }
    
}

async def main():
    
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()


    named_tools = {}
    for tool in tools:
        named_tools[tool.name] = tool

    print("Available tools:", named_tools.keys())

    llm = ChatOllama(model="llama3.2:3b")
    llm_with_tools = llm.bind_tools(tools)
    while True:
        prompt = input("Enter your question") # can u rooll a dice twice or can u add my expense 500 to groceries
        response = await llm_with_tools.ainvoke(prompt) # in this in first call we are getting tool to use with its args and all then we are getting the response in second call

        if not getattr(response, "tool_calls", None):
            print("\nLLM Reply:", response.content)
            return

        tool_messages = []
        for tc in response.tool_calls:
            selected_tool = tc["name"]
            selected_tool_args = tc.get("args") or {}
            selected_tool_id = tc["id"]

            print(f"Tool Called{selected_tool}")
            print(f"Arguments : {json.dumps(selected_tool_args, indent=2)}")

            result = await named_tools[selected_tool].ainvoke(selected_tool_args)
            print(f"Result {json.dumps(result, indent=2)}")
            tool_messages.append(ToolMessage(tool_call_id=selected_tool_id, content=json.dumps(result)))
        

        final_response = await llm_with_tools.ainvoke([prompt, response, *tool_messages])
        print(f"Final response: {final_response.content}")


if __name__ == '__main__':
    asyncio.run(main())
