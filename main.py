from roboter.roboter import RoboterCommunication

# Robokoインスタンス生成
roboter_run = RoboterCommunication()

name = roboter_run.ask_name()
csv_data = roboter_run.open_csv()
restaurant = roboter_run.recommend_restaurant(csv_data)

if not restaurant:
    restaurant = roboter_run.ask_restaurant(name)

roboter_run.save_csv(restaurant, csv_data)
roboter_run.closing(name)


