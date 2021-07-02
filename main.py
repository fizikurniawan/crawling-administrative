import requests
import csv
from tqdm import tqdm


def get_provinces():
    response = requests.get("https://sig.bps.go.id/rest-drop-down/getwilayah")

    json_resp = response.json()

    data = []
    for i in json_resp:
        code = i.get("kode")
        name = i.get("nama")

        data.append([code, name])

    with open('provinces.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(["id", "name"])

        # write multiple rows
        writer.writerows(data)


def get_regencies():
    url = "https://sig.bps.go.id/rest-bridging-pos/getwilayah?level=kabupaten&parent="
    data = []

    province_ids = []
    with open("provinces.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for i in csv_reader:
            province_id = i[0]
            if province_id == "id":
                continue

            province_ids.append(province_id)

    for province_id in tqdm(set(province_ids)):
        current_url = url + province_id

        response = requests.get(current_url)
        resp_json = response.json()

        for res in resp_json:
            id = res.get("kode_bps")
            name = res.get("nama_pos")

            if not any(id in x for x in data):
                data.append([id, province_id, name])

    with open('regencies.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(["id", "province_id", "name"])

        # write multiple rows
        writer.writerows(data)


def get_districts():
    url = "https://sig.bps.go.id/rest-bridging-pos/getwilayah?level=kecamatan&parent="
    data = []
    regency_ids = []

    with open("regencies.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for i in csv_reader:
            regency_id = i[0]
            if regency_id == "id":
                continue
            regency_ids.append(regency_id)

    for regency_id in tqdm(set(regency_ids)):
        current_url = url + regency_id

        response = requests.get(current_url)
        resp_json = response.json()

        for res in resp_json:
            id = res.get("kode_bps")
            name = res.get("nama_pos")
            postal_code = res.get("kode_pos")

            if not any(id in x for x in data):
                data.append([id, regency_id, name, postal_code])

    with open('districts.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(["id", "regency_id", "name"])

        # write multiple rows
        writer.writerows(data)


def get_villiages():
    url = "https://sig.bps.go.id/rest-bridging-pos/getwilayah?level=desa&parent="
    data = []

    with open("districts.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        district_ids = []
        for i in csv_reader:
            district_id = i[0]
            if district_id == "id":
                continue
            district_ids.append(district_id)

        for i in tqdm(set(district_ids)):
            current_url = url + i

            response = requests.get(current_url)
            resp_json = response.json()

            for res in resp_json:
                id = res.get("kode_bps")
                name = res.get("nama_pos")
                postal_code = res.get("kode_pos")

                if not any(id in x for x in data):
                    data.append([id, i, name, postal_code])

    with open('villages.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(["id", "district_id", "name", "poostal_code"])

        # write multiple rows
        writer.writerows(data)


if __name__ == "__main__":
    while True:
        print(
            """
            1. Crawling Province
            2. Crawling Regency
            3. Crawling District
            4. Crawling Village
            5. Exit
            """
        )

        choice = input("Input Choice: ")

        if str(choice) == "1":
            get_provinces()
        elif str(choice) == "2":
            get_regencies()
        elif str(choice) == "3":
            get_districts()
        elif str(choice) == "4":
            get_villiages()
        elif str(choice) == "5":
            exit()
