import csv
import random

def main():
    print('Hello, my name is HelperGames_Bot.')
    fields = load_fields("./games.csv")

    while True:
        filter_fields = input("Print fields that you want to delete (separated by commas, no spaces). If you want to skip, don’t write anything: ")
        if filter_fields != '':
            process_filter(fields, filter_fields)
        else:
            break
    
    while True:
        next_step = input('How can I help you? (type !help for commands):\n')
        if next_step == '!help':
            show_help()
        elif next_step == '!GetGame':
            get_game()
        elif next_step == '!CountOfGamesByRate':
            count_of_games_by_rate()
        elif next_step == '!GiveReviewOf5Games':
            give_review_of_5_games()
        elif next_step == '!quit':
            print('Thanks for your visit!')
            break
        else:
            print('Please type !help to see your commands, or !quit to exit.')

def load_fields(file_path):
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        return reader.fieldnames

def process_filter(fields, filter_fields):
    splited_fields = filter_fields.split(',')
    fieldnames = [field for field in fields if field not in splited_fields]

    if len(fieldnames) == 0:
        print("Please, write correct fields.")
        return

    with open("./filtered.csv", 'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        with open("./games.csv", 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                writer.writerow({field: row[field] for field in fieldnames})

    print("Created file filtered.csv")

def get_game():
    genre = input('Give me genre of your game/s:\n')
    team = input('Give me the team that created game/s:\n')

    filtered_rows = []
    with open("./games.csv", 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if str(team) in row['Team'] and str(genre) in row['Genres']:
                filtered_rows.append(row)

    if len(filtered_rows) == 0:
        print("Games with these filters weren't found.")
        return

    with open("./GetGame.csv", 'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)

    print('Created file GetGame.csv')

def count_of_games_by_rate():
    team = input('Give me the team to check the count of games with your rating:\n')
    
    try:
        rating = float(input('Input rating (in range 0.0-5.0):\n'))
        if rating < 0 or rating > 5:
            print("Please write rating in range 0.0-5.0")
            return
    except ValueError:
        print("Please, write rating like this: 4.3 or 1.1 or 4.4")
        return

    filtered_rows = []
    with open("./games.csv", 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if str(team) in row['Team'] and str(rating) == str(row['Rating']):
                filtered_rows.append(row)

    count_of_rate_games = len(filtered_rows)
    
    if count_of_rate_games <= 0:
        print("Games weren't found.")
        return

    with open('./CountOfGamesByRate.csv', 'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)

    print('Created file CountOfGamesByRate.csv')
    print(f"Count of rated games is {count_of_rate_games}")

def give_review_of_5_games():
    with open("./games.csv", 'r', encoding='utf-8') as csv_file:
        reader = list(csv.DictReader(csv_file))
    
    random_rows = random.sample(reader, 5)

    with open('./GiveReviewOf5Games.csv', 'w', encoding='utf-8') as file:
        fieldnames = ['Title', 'Reviews']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for row in random_rows:
            filtered_row = {field: row[field] for field in fieldnames}
            writer.writerow(filtered_row)

    print('Created file GiveReviewOf5Games.csv')

def show_help():
    print('I can do 4 functions:')
    print('!GetGame - Give you games based on your preferences.')
    print('!CountOfGamesByRate - Provide the count of games by team and rating.')
    print('!GiveReviewOf5Games - Give you reviews on 5 random games.')
    print('!quit - Command to exit from program.')

if __name__ == "__main__":
    main()