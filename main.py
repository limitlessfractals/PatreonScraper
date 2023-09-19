from getlinks import main as getlinks_main
from createHtml import main as createHtml_main
from consolidatehtml import main as consolidatehtml_main

def main():
    getlinks_main()
    html_directory = createHtml_main()
    consolidatehtml_main(html_directory)

if __name__ == "__main__":
    main()
