import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

import asyncio
from app.main import main


if __name__ == '__main__':
    asyncio.run(main())
