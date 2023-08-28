# National ID number generator and validator

CLI tool to generate and validate Lithuanian Personal Code (National ID number)

## Disclaimer

This tool is intended for educational and testing purposes only. There is always a possibility that the generator will return an already existing personal number. Therefore, the generated number should not be used for malicious purposes. The author of this tool does not claim any responsibility for how it is used.


## Usage

1. Open terminal or command prompt.
2. Navigate to the directory where the script (`main.py`) is located.

### Command: validate

To validate a number use the following command:
```bash
python main.py validate <number>
```

### Command: generate

To generate a number use the following command:
```bash
python main.py generate <gender> <birth_date> <queue_number>
```

## Examples

```bash
python main.py validate 12345678912 # Date 1823-45-67 is incorrect
```

```bash
python main.py generate female 2030-02-15 12 # 63002150128
```

```bash
python main.py validate 63002150128 # National number 63002150128 is valid
```

