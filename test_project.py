from project import parsing, calculate, end, store, main, backup
from pytest import MonkeyPatch
import pytest
from bs4 import BeautifulSoup
import requests
import csv

def delete():
    with open("backup_storage.csv", mode='r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    with open("storage.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

delete()

@pytest.fixture
def parsed_price():
    url = f"https://oldschool.runescape.wiki/Rune_scimitar"
    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
            }
    result = requests.get(url, headers=headers)
    doc = BeautifulSoup(result.text, "html.parser")
    return int(doc.find("span", class_="infobox-quantity-replace").text.strip().replace(",", ""))


def test_parsing(monkeypatch, parsed_price):
    
    mock_input = lambda prompt: "Rune scimitar"

    monkeypatch.setattr("builtins.input", mock_input)
    
    item, price = parsing()
    assert item == "rune scimitar"
    assert price == parsed_price


def test_calculate(monkeypatch, parsed_price):
    mock_input = lambda prompt: 1
    monkeypatch.setattr("builtins.input", mock_input)
    
    cart = calculate("rune scimitar", parsed_price)
    assert cart == [{'Item': 'rune scimitar', 'Price': f"{parsed_price:,} coins" , 'Quantity': 1, 'Total': f"{(parsed_price*1):,} coins"}]


def test_end(parsed_price):
    cart, total = end()
    assert cart == [{'Item': 'rune scimitar', 'Price': f"{parsed_price:,} coins" , 'Quantity': 1, 'Total': f"{(parsed_price*1):,} coins"}]
    assert total == parsed_price*1



def test_store():
    headers=["Item","Price","Quantity","Total", "Final Total"]
    separator = {"Item": "---------------------------------------------------", "Price": "", "Quantity": "", "Final Total":""}
    cart = [{'Item': 'yellow party hat', 'Price': '6,359 coins', 'Quantity': 1, 'Total': '6,359 coins'}, {'Item': '', 'Price': '', 'Quantity': '', 'Total': '', 'Final Total': 6359}]
    
    with open("storage.csv", mode="a", newline='') as file:

        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writerows(cart)
        writer.writerow(separator)

    with open("storage.csv", mode="r", newline='') as file:
        reader = csv.reader(file)
        row = list(reader)
        separator = ['---------------------------------------------------', '', '', '', '']
        position_list = []
        final_list = []

        for position, item in enumerate(row):
            if item == separator:
                position_list.append(position)
        position_list.remove(max(position_list))
        separator_position = max(position_list)

        for values in row:
            if row.index(values) > separator_position:
                final = dict(zip(headers, values))
                final_list.append(final)
        
        for inputs in final_list:
            for key, value in inputs.items():
                if value.isdigit():
                    inputs[key] = int(value)
        
        for index, items in enumerate(final_list):
            if index != len(final_list) - 1:
                if "Final Total" in items:
                    del items["Final Total"]
    
    assert final_list == cart
    delete()

def test_backup():
    with open("storage.csv", "r", newline='') as file1, open("backup_storage.csv", "r", newline='') as file2:
        file1_reader = csv.reader(file1)
        file2_reader = csv.reader(file2)

        rows1 = list(file1_reader)
        rows2 = list(file2_reader)

    assert rows1 == rows2



    





            
