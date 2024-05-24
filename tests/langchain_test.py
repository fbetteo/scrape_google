from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

# Load HTML
loader = AsyncChromiumLoader(
    [
        "https://www.google.com/travel/flights?hl=en&q=Flights%20to%20JED%20from%20CAI%20on%202024-05-25%20oneway%20&curr=USD"
    ]
)
html = loader.load()

bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["span"])
docs_transformed[0].page_content[0:500]
####

from bs4 import BeautifulSoup
from langchain_community.document_loaders import AsyncHtmlLoader

urls = [
    "https://www.google.com/travel/flights?hl=en&q=Flights%20to%20JED%20from%20CAI%20on%202024-05-25%20oneway%20&curr=USD"
]
loader = AsyncHtmlLoader(urls)
docs = loader.load()

soup_list = [BeautifulSoup(doc.page_content, "html.parser") for doc in docs]


body_element = soup_list[0].find("body", id="yDmH0d")

# Extract the text and split it by new lines
text_lines = body_element.text.split("\n")
text_lines
from langchain_community.document_transformers import Html2TextTransformer


html2text = Html2TextTransformer()
docs_transformed = html2text.transform_documents(docs)
