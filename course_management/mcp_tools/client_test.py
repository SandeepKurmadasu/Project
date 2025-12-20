import asyncio
import json
import sys
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

project_root = "/home/hr/FSD/hive_edu_verse"
sys.path.insert(0, project_root)
SERVER_PATH = "course_management/mcp_tools/server.py"


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=[SERVER_PATH],
        env={
            "PYTHONPATH": project_root,
            "PATH": os.environ.get("PATH", ""),
        },
        cwd=project_root,
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools_result = await session.list_tools()
            tools = tools_result.tools

            print("== AVAILABLE TOOLS ==")
            for idx, t in enumerate(tools, start=1):
                print(f"{idx}. {t.name} - {t.description}")

            name_to_tool = {t.name: t for t in tools}
            index_to_tool = {str(i): t for i, t in enumerate(tools, start=1)}

            while True:
                choice = input(
                    "\nType tool number/name to run it, or 'q' to quit: "
                ).strip()

                if choice.lower() in {"q", "quit", "exit"}:
                    print("Bye Baba.")
                    break

                tool = index_to_tool.get(choice) or name_to_tool.get(choice)
                if not tool:
                    print("Unknown tool, try again.")
                    continue

                schema = tool.inputSchema or {}
                props = schema.get("properties", {})
                required = set(schema.get("required", []))

                args = {}
                if props:
                    print("\nProvide arguments (press Enter to skip optional ones):")
                    for arg_name, meta in props.items():
                        desc = meta.get("description", "")
                        prompt = f"- {arg_name}"
                        if desc:
                            prompt += f" ({desc})"
                        if arg_name in required:
                            prompt += " [required]"
                        prompt += ": "

                        while True:
                            val = input(prompt).strip()
                            if val == "" and arg_name in required:
                                print("  This field is required.")
                                continue
                            if val == "":
                                break
                            try:
                                args[arg_name] = json.loads(val)
                            except json.JSONDecodeError:
                                args[arg_name] = val
                            break

                print(f"\n== CALL {tool.name} ==")
                try:
                    result = await session.call_tool(
                        name=tool.name,
                        arguments=args,
                    )
                    for item in result.content:
                        if item.type == "text":
                            print("\n--- TOOL RESULT ---")
                            print(item.text)
                        else:
                            print(f"\n[non-text content] {item}")
                except Exception as e:
                    print(f"Error calling tool: {e}")


if __name__ == "__main__":
    asyncio.run(main())