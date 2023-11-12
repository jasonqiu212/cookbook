from download import download
from extract import extract


def main():
    recipe = download()
    results = extract(recipe)
    print(results)


if __name__ == '__main__':
    main()
