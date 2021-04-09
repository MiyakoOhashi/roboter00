import csv
import os
import pathlib
import string
from termcolor import colored


ROBOT_NAME = 'Roboko'

# ROBOTERデータ処理
class RoboterDataOperation():

    #ROBOTERのおすすめレストランを検出
    def detection_most_favourite(self, csv_data):
        # おすすめデータを格納する辞書を設定
        most_popular = {'Name': None, 'Count': 0}
        second_popular = {'Name': None, 'Count': 0}

        for row in csv_data:
            if int(most_popular['Count']) < int(row['Count']):
                # 2番人気を設定
                second_popular = most_popular.copy()
                # 1番人気を設定
                most_popular = row.copy()
            elif int(second_popular['Count']) < int(row['Count']):
                second_popular = row.copy()

        return most_popular, second_popular


#CSVデータ操作
class RoboterCSV():

    #CSVファイル作成
    def create_csv(self):
        pathlib.Path('recommend.csv').touch()

    #CSVファイルを開き、データを作業用リストに格納する
    def open_csv(self):
        #csvデータ受けリスト
        csv_data = []

        #ファイルがすでにある時
        if os.path.exists('recommend.csv'):
            with open('recommend.csv', 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    csv_data.append(row)

        #ファイル未作成時
        else:
            self.create_csv()

        return csv_data

    # レストランをCSVファイルに保存
    def save_csv(self, restaurant, csv_data):
        #print(restaurant)
        # すでにデータがある時
        if csv_data:
            with open('recommend.csv', 'w') as csv_file:
                fieldnames = ['Name', 'Count']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                coincide = False
                for row in csv_data:
                    #csvデータ内に合致するレストランがある時
                    if row['Name'] == restaurant:
                        coincide = True
                        count = int(row['Count']) + 1
                        writer.writerow({'Name': '{}'.format(row['Name']), 'Count': count})
                    #合致データ以外のcsvデータを元どおり書き込む
                    else:
                        writer.writerow({'Name': '{}'.format(row['Name']) , 'Count': int(row['Count'])})
                #csvデータ内に合致するレストランがなかった時（書き足し）
                if not coincide:
                    writer.writerow({'Name': '{}'.format(restaurant), 'Count': 1})
        # まだデータが1つもない時
        else:
            with open('recommend.csv', 'w') as csv_file:
                fieldnames = ['Name', 'Count']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'Name': '{}'.format(restaurant), 'Count': 1})



#Roboterインターフェース
class RoboterCommunication(RoboterDataOperation, RoboterCSV):

    # 利用者の名前を聞く
    def ask_name(self):
        while True:
            with open('template/greeting.txt', 'r') as f:
                t = string.Template(f.read())
            content = t.substitute(robot_name=ROBOT_NAME)
            name = input(colored(content, 'green'))
            if name:
                break
        return name

    # ROBOTERのおすすめレストランを紹介
    def recommend_restaurant(self, csv_data):
        #1番人気と2番人気のレストランを検出
        most_popular, second_popular = self.detection_most_favourite(csv_data)

        # 1番人気のレストラン名をセット
        restaurant = most_popular['Name']

        if not restaurant:
            return restaurant

        else:
            # 1番人気と2番人気を順に勧める
            while True:
                with open('template/recommend.txt', 'r') as f:
                    t = string.Template(f.read())
                content = t.substitute(restaurant=restaurant)
                answer = input(colored(content, 'green')).lower()
                # 気に入った時
                if answer == 'yes' or answer == 'y':
                    return restaurant
                # 気に入らなかった時
                elif answer == 'no' or answer == 'n':
                    if second_popular['Name']:
                        # 2番が残っている時
                        restaurant = second_popular['Name']
                        second_popular['Name'] = None
                    else:
                        # 残っていない時
                        restaurant = None
                        return restaurant
                else:
                    print('あなたがこのレストランを好きかどうかわかりません。もう一度お答えください。')

    # 利用者の好きなレストランを聞く
    def ask_restaurant(self, name):
        while True:
            with open('template/query.txt', 'r') as f:
                t = string.Template(f.read())
            content = t.substitute(name=name)
            restaurant = input(colored(content, 'green')).capitalize()
            if restaurant:
                break
        return restaurant

    # 利用終了の挨拶
    def closing(self, name):
        with open('template/closing.txt', 'r') as f:
            t = string.Template(f.read())
        content = t.substitute(name=name)
        print(colored(content, 'green'))



# Robokoインスタンス生成
roboter_run = RoboterCommunication()
name = roboter_run.ask_name()

csv_data = roboter_run.open_csv()
restaurant = roboter_run.recommend_restaurant(csv_data)
if restaurant:
    roboter_run.save_csv(restaurant, csv_data)

csv_data = roboter_run.open_csv()
restaurant = roboter_run.ask_restaurant(name)
roboter_run.save_csv(restaurant, csv_data)

roboter_run.closing(name)

