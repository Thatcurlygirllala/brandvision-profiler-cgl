import os
from dotenv import load_dotenv

load_dotenv()

print("OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))
print("BASE_ID =", os.getenv("BASE_ID"))
print("OFFER_GENERATOR_TABLE =", os.getenv("OFFER_GENERATOR_TABLE"))
