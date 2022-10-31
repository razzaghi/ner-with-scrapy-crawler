import requests


def send_request():
    url = "https://es.quora.com/graphql/gql_para_POST?q=MultifeedQuery"
    payload = {"queryName": "MultifeedQuery",
               "variables": {"first": 10, "multifeedAfter": "9094554532397534981", "multifeedNumBundlesOnClient": 10,
                             "injectionType": None, "injectionData": None, "filterStoryType": None,
                             "filterStoryOid": None, "multifeedPage": "topic", "pageData": 1772334,
                             "showLiveBanner": False},
               "extensions": {"hash": "e3d4233a48fcf75eac56c8f07961ed49b43479c847c39053e503e949bec442f9"}}

    response = requests.post(
        url=url,json=payload
    )

    print(response)

send_request()