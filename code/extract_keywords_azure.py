#Extract key phrase using Text Analytics SDK 

from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import pandas as pd

credential = AzureKeyCredential("API KEY")
endpoint="https://southeastasia.api.cognitive.microsoft.com/"

text_analytics_client = TextAnalyticsClient(endpoint, credential)

df_jd = pd.read_csv('jd_combine.csv')

documents = [
    "Redmond is a city in King County, Washington, United States, located 15 miles east of Seattle.",
    """
    I need to take my cat to the veterinarian. He has been sick recently, and I need to take him
    before I travel to South America for the summer.
    """,
]

response = text_analytics_client.extract_key_phrases(documents, language="en")
result = [doc for doc in response if not doc.is_error]

for doc in result:
    print(doc.key_phrases)
