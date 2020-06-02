import requests
from pprint import pprint
import json
# from Python_Code_Snippets.SqlAlchemyDatabase import Country, Season, Temperature
from bs4 import BeautifulSoup

HOST_URL = "https://www.metoffice.gov.uk/"

data = requests.get("https://www.metoffice.gov.uk/climate/uk/summaries/datasets#yearOrdered")
soup = BeautifulSoup(data.content, 'html.parser')
region_names_list = ['UK', 'England', 'Wales', 'Scotland']
data_option_list = ['Tmax', 'Tmin', 'Tmean', 'Sunshine', 'Rainfall']
data_len = len(data_option_list)
table_data = soup.find("div", {"class": "responsive-table"})
child_tr_data = table_data.findAll("tr")[1:5:]
data_dict = {}
month_names = []
season_names = []


def main():
    for each in child_tr_data:
        region_name = each.find("td").string
        if region_name not in region_names_list:
            break
        td_data = each.findAll("td")[1:6]
        if region_name not in data_dict:
            data_dict[region_name] = {}
        for each_td in td_data[:data_len]:
            href_link = each_td.find('a')['href']
            request_response = requests.get(HOST_URL + href_link)
            if request_response.status_code == 200:
                request_data = request_response.text.strip().split("\n")[5:]
                # pprint(request_data)
                # print(request_data[0].split(" year"))
                split_year_data = request_data[0].split(" year")
                month_names = [each.strip() for each in split_year_data[:-6]]
                season_names = [each.strip() for each in split_year_data[12:-1]]
                print_temp_data(request_data[1:], region_name, href_link.split("/")[-3], month_names, season_names)
            break
        break


def print_temp_data(request_data, region, temp_name, months, seasons):
    for element in request_data:
        if temp_name not in data_dict[region]:
            data_dict[region][temp_name] = {'months': {each: [] for each in months}}
        # for each in seasons:
        if 'season' not in data_dict[region][temp_name]:
            data_dict[region][temp_name]['season'] = {each: [] for each in seasons}
        element_list = [each for each in element.split(" ") if each]
        temperature = [each for each in element_list[0::2]]
        year_list = [each for each in element_list[1::2]]
        mapping_list = list(zip(temperature, year_list))
        month_cnt = season_cnt = 0
        for each in mapping_list:
            if month_cnt <= len(months) - 1:
                data_dict[region][temp_name]['months'][months[month_cnt]].append(each)
                month_cnt += 1
            elif season_cnt <= len(seasons) - 1:
                data_dict[region][temp_name]['season'][seasons[season_cnt]].append(each)
                season_cnt += 1
    pprint(data_dict)


if __name__ == '__main__':
    main()
