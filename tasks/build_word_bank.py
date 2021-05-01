import json

with open("../resources/currencies_200.json") as data:
    data_json = json.load(data).get("data")
word_bank = []
structured_work_bank = []
for item in data_json:

    word_bank.append(item["name"].lower())
    word_bank.append(item["symbol"])
    structured_work_bank.append([item["name"].lower(), item["symbol"]])

with open("../resources/word_bank.json", "w") as file:
    json.dump(word_bank, file)

with open("../resources/structured_word_bank.json", "w") as file:
    json.dump(structured_work_bank, file)
