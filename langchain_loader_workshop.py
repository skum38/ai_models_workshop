import os
from playwright.sync_api import sync_playwright
from langchain_community.document_loaders import TextLoader,PyPDFLoader,WebBaseLoader,PlaywrightURLLoader,WikipediaLoader

# text loader
textLoader=TextLoader("sample.txt")
data=textLoader.load()
print("Text data:", data, "\n")

# pdf loader 
pdfLoader=PyPDFLoader("e-cert.pdf")
pdf_data=pdfLoader.load()
print("PDF data:", pdf_data, "\n")

# web loader plain HTTP fetching
webLoader=WebBaseLoader("https://www.signitysolutions.com/blog/langchain-vs.-transformers-agent")  
web_data=webLoader.load()
#print("Web data:", web_data, "\n")

# web loader with selenium (for dynamic content)
#use a browser-based loader (Playwright or Selenium) that executes JavaScript. Example using PlaywrightURLLoader.
#pip install langchain playwright
#python -m playwright install chromium
#pip install unstructured

#webLoader=PlaywrightURLLoader(["https://medium.com/@shivanishah0218/langchain-or-transformers-knowing-the-right-tool-for-the-job-c284380edc16"])  
#dynamic_web_data=webLoader.load()
#print("Web data:", dynamic_web_data, "\n")



URL = "https://medium.com/@shivanishah0218/langchain-or-transformers-knowing-the-right-tool-for-the-job-c284380edc16"
STATE_FILE = "medium_state.json"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

def create_session(p):
    print("\n🔐 Medium session not found or expired.")
    print("➡ Opening browser ONCE for verification...")

    browser = p.chromium.launch(
        headless=False,
        slow_mo=50,
        args=["--disable-blink-features=AutomationControlled"]
    )

    context = browser.new_context(
        user_agent=USER_AGENT,
        viewport=None
    )

    page = context.new_page()
    page.goto(URL, timeout=60000)

    print("\n👉 Complete the verification in the browser.")
    input("👉 Press ENTER once the article is fully visible...")

    context.storage_state(path=STATE_FILE)
    browser.close()

    print("✅ Session saved. Future runs will be headless.\n")


def scrape_headless(p, url):
    browser = p.chromium.launch(headless=True)

    context = browser.new_context(
        storage_state=STATE_FILE,
        user_agent=USER_AGENT
    )

    page = context.new_page()
    page.goto(url, timeout=60000, wait_until="domcontentloaded")

    # Remove any residual modals
    page.evaluate("""
        document.querySelectorAll('[role="dialog"]').forEach(d => d.remove());
        document.body.style.overflow = 'auto';
    """)

    # Scroll for lazy loading
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(1500)

    page.wait_for_selector("h1", timeout=15000)

    title = page.locator("h1").first.text_content() or ""

    paragraphs = page.evaluate("""
        () => Array.from(document.querySelectorAll("p"))
            .map(p => p.innerText.trim())
            .filter(text => text.length > 40)
    """)

    browser.close()

    return {
        "title": title.strip(),
        "content": "\n".join(paragraphs)
    }


def has_valid_session():
    return os.path.exists(STATE_FILE)


def main():
    with sync_playwright() as p:
        # STEP 1: Create session if needed
        if not has_valid_session():
            create_session(p)

        # STEP 2: Always scrape headless
        article = scrape_headless(p, URL)

        print("\n📄 TITLE:\n", article["title"])
        print("\n📄 CONTENT:\n", article["content"])
        print("\n✅ Done.","\n")
        
       


if __name__ == "__main__":
    main()

#load wikipedia page

wikiloader = WikipediaLoader(
    query="LangChain (software)",
    load_max_docs=2
)
wiki_docs = wikiloader.load()

for i, doc in enumerate(wiki_docs):
    print(f"\nArticle {i+1}", "\n","-" * 20)
    print("Title:", doc.metadata.get("title"))
    print("Wikipedia data:", doc.page_content, "\n")

