# def main():
#     print("Hello from mimicus!")


# if __name__ == "__main__":
#     main()


import asyncio
from fastmcp import Client



# HTTP server
client = Client("http://0.0.0.0:12001/mcp")



async def main():
    async with client:
        # Basic server interaction
        await client.ping()

        # List available operations
        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()

        # Execute operations
        
        print(tools)
        print(resources)
        print(prompts)


asyncio.run(main())