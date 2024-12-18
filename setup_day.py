import requests
import os

# Set up variables
YEAR = 2024
DAY = 1
SESSION_COOKIE = '53616c7465645f5f3896026f975f804a3cd5240f00abb7344fb14502218194ab62f408d544b2c305a9625e43491df47e32b2a42f13aac0ad97bde6c6f37e24a1'

# URLs for downloading
input_url = f'https://adventofcode.com/{YEAR}/day/{DAY}/input'
description_url = f'https://adventofcode.com/{YEAR}/day/{DAY}'

# Headers for authentication
headers = {
    'Cookie': f'session={SESSION_COOKIE}',
    'User-Agent': 'advent-of-code-data-downloader'
}

# Directory setup
directory = f'./AdventOfCode{YEAR}/Day{DAY:02d}'
os.makedirs(directory, exist_ok=True)

# Download the input data
response = requests.get(input_url, headers=headers)
if response.status_code == 200:
    with open(f'{directory}/input.txt', 'w') as file:
        file.write(response.text)
    print(f'Input data downloaded for Day {DAY}, {YEAR}.')
else:
    print(f'Failed to download input data: {response.status_code}')

# Create the template Python script
template_py = f"""
# Advent of Code {YEAR} - Day {DAY}
# https://adventofcode.com/{YEAR}/day/{DAY}

def solve(input_data):
    # Your code here
    pass

if __name__ == "__main__":
    with open("input.txt") as f:
        input_data = f.read().strip()
    solve(input_data)
"""

with open(f'{directory}/day{DAY:02d}.py', 'w') as file:
    file.write(template_py)
print(f'Template Python script created for Day {DAY}, {YEAR}.')

# Create the .bat file to run the Python script
bat_content = f"""
@echo off
python day{DAY:02d}.py
pause
"""

with open(f'{directory}/run_day{DAY:02d}.bat', 'w') as file:
    file.write(bat_content)
print(f'Batch file created for running Day {DAY}, {YEAR} script.')
