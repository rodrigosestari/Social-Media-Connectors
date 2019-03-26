import pprint
import apiclient

from googleapiclient.discovery import build


def main():
    service = apiclient.discovery.build("customsearch", "v1",
                    developerKey="AIzaSyDRRpR3GS1F1_jKNNM9HCNd2wJQyPG3oN0")

    res = service.cse().list(
        q='lectures',
        cx='017576662512468239146:omuauf_lfve',
    ).execute()
    pprint.pprint(res)


if __name__ == '__main__':
    main()
