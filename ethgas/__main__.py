"""Entry point for running ethgas as a module."""
import asyncio
from ethgas.main import main

if __name__ == "__main__":
    asyncio.run(main())
