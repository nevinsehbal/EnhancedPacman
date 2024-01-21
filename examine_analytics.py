from datetime import datetime
import os

def analyze_game_performance(log_data):
    food_eaten = 0
    unnecessary_steps = 0
    start_time = None
    end_time = None

    # Variables to store the values of GHOST_SPAWN_TIME_SEC and SENSITIVITY_DISTANCE
    ghost_spawn_time = None
    sensitivity_distance = None
    pacman_score_numerator = 0
    pacman_score_denominator = 0

    for log_entry in log_data:
        timestamp_str, _, info = log_entry.partition(' - INFO - ')
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

        if 'GHOST_SPAWN_TIME_SEC' in info:
            ghost_spawn_time = int(info.split()[-1])
        elif 'SENSITIVITY_DISTANCE' in info:
            sensitivity_distance = int(info.split()[-1])
        elif 'Pacman ate' in info:
            food_eaten += 1
        elif 'Pacman moved to position' in info:
            unnecessary_steps += 1
        elif 'Pacman score is' in info:
            pacman_score_numerator = int(info.split()[-1].split('/')[0])
            pacman_score_denominator = int(info.split('/')[-1])

        if start_time is None:
            start_time = timestamp
        end_time = timestamp

    total_game_time = (end_time - start_time).total_seconds()

    return {
        'food_eaten': food_eaten,
        'unnecessary_steps': unnecessary_steps,
        'total_game_time': total_game_time,
        'ghost_spawn_time': ghost_spawn_time,
        'sensitivity_distance': sensitivity_distance,
        'pacman_score': f"{pacman_score_numerator}/{pacman_score_denominator}"
    }

# Function to read game logs from a directory
def read_logs_from_directory(directory_path):
    game_logs = []

    # Iterate through all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".log"):  # assuming log files have a .log extension
            file_path = os.path.join(directory_path, filename)

            with open(file_path, 'r') as file:
                game_logs.append(file.readlines())

    return game_logs

# Replace 'logs' with the actual path to your logs directory
logs_directory_path = 'logs'
game_logs = read_logs_from_directory(logs_directory_path)

for log in game_logs:
    result = analyze_game_performance(log)
    # Displaying the results, including the two variables
    print("---------------- NEW GAME --------------------")
    print(f"Ghost spawn time seconds: {result['ghost_spawn_time']}")
    print(f"Sensitivity distance: {result['sensitivity_distance']}/600 of the maze")
    print(f"Total Game Time: {result['total_game_time']} seconds")
    print(f"Pacman Score: {result['pacman_score']}")
    print(f"Food eat movement: {result['food_eaten']}")
    print(f"Running movement: {result['unnecessary_steps']}")
    print("------------------------------------------------------")
