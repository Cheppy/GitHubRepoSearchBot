from bs4 import BeautifulSoup
import requests as req


def get_repos(base_url):
    repo_dicts = []
    resp = req.get(base_url)
    soup = BeautifulSoup(resp.text, 'lxml')

    repo_lis = soup.find_all("li", class_="repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source")
    for x in repo_lis:
        repo_dict_son = {
                         'stars': parse_element(x, "a", class_name="muted-link"),
                         'tags': parse_element(x, "a", class_name="topic-tag topic-tag-link f6 px-2 mx-0"),
                         'languages': parse_element(x, "span", itprop="programmingLanguage")}

        for repo in x.findChildren("a", class_="v-align-middle", href=True):
            repo_dict_son["link"] = repo['href']

        repo_dicts.append(repo_dict_son)
    print(repo_dicts)
    return repo_dicts


def parse_element(repo, tag, class_name=None, itprop=None):
    for x in repo.findChildren(tag, class_=class_name, itemprop=itprop):
        return x.text


def format_data(data: dict):
    """
    :param data:
    :return:  formatted data
    """

    lang = data['languages']
    splitter = "/"
    if data['languages'] is None:
        data['languages'] = ""
    if data['stars'] is None:
        data['stars'] = "0"
    return f"Author: <a href =\"https://github.com/{data['link'].split(splitter)[1]}\">" \
           f"{data['link'].split(splitter)[1]}</a>;" \
           f"  Rep: <a href =\"https://github.com/{data['link']}\">{data['link'].split(splitter)[2]}</a> " \
           f"({data['stars'].split()[0]} ⭐️" \
           f"{data['languages']})\n" \
           f"      tags: {data['tags']}"


def get_search_url(search_string, page):
    """
    :param search_string:
    :param page:
    :return:
    """
    return f"https://github.com/search?p={page}&q={search_string}"


def github_search(search_string, results_page="1"):
    """
    :param search_string:
    :param results_page:
    :return:
    """
    search_url = get_search_url(search_string, results_page)
    ready_text = f"Page: {results_page}\n"
    repos_list = get_repos(search_url)
    counter = 0
    for x in repos_list:
        counter += 1
        ready_text += f"{counter}. " + format_data(x) + "\n"
    return ready_text