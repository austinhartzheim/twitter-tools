# twitter-tools
Tools for downloading Twitter followers into a CSV spreadsheet.

## Install
```sh
git clone https://github.com/austinhartzheim/twitter-tools.git
cd twitter-tools
sudo pip install -r requirements.txt
```

## Congigure
Copy `config.py.dist` to `config.py` and edit `config.py` with your API key information (obtained from the Twitter interface).

## Run
```sh
# Download a spreadsheet of twitter followers
./download-followers.py username output-filename.csv

# Filter spreadsheet to only verified followers
./filter-to-verified.py input-filename.csv output-filename.csv

# Trim extra columns from the spreadsheet
./convert-to-basic.py input-filename.csv output-filename.csv
```