from langchain_community.document_loaders import PyPDFLoader,WikipediaLoader
from numpy import inf

def wiki_loader():
   
    wikiloader = WikipediaLoader(
        query="LangChain (software)",
        load_max_docs=5
    )
    wiki_docs = wikiloader.load()
    full_text="\n".join([doc.page_content for doc in wiki_docs])

    return full_text
    


def split_wiki_char_text_splitter():

    full_text=wiki_loader()
   
    # text splitter with chunk size and overlap
    from langchain_text_splitters import CharacterTextSplitter

    char_text_splitter =  CharacterTextSplitter.from_tiktoken_encoder(
     chunk_size=500, chunk_overlap=50
   )
    texts = char_text_splitter.split_text(full_text)
    print(f"Number of chunks: {len(texts)}")
    print ("Char Splitter:", texts, "\n")


def split_wiki_recursive_text_splitter():

    full_text=wiki_loader()
   
    # text splitter with chunk size and overlap
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    rec_text_splitter =  RecursiveCharacterTextSplitter.from_tiktoken_encoder(
     chunk_size=500, chunk_overlap=50
   )
    texts = rec_text_splitter.split_text(full_text)
    print(f"Number of chunks: {len(texts)}")
    print ("Char Splitter:", texts, "\n")




if __name__ == "__main__":
    print("Select a text splitter method:")
    print("1. Character Text Splitter")
    print("2. Recursive Character Text Splitter")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        split_wiki_char_text_splitter()
    elif choice == "2":
        split_wiki_recursive_text_splitter()
    else:
        print("Invalid choice. Please enter 1 or 2.")
   