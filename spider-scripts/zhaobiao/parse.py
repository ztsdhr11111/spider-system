from lxml import etree

def parse(html):
    """
    Parse the HTML and return a list of dictionaries containing the title, link, and description of each article.
    """
    # Create an HTML parser
    parser = etree.HTMLParser()

    # Parse the HTML
    tree = etree.parse(html, parser)

    # Find all the articles
    articles = tree.xpath('//article')

    # Create a list to store the results
    results = []
    return results