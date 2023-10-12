import argparse
import re


def calculate_control_sum(personal_num, multiplier):
    control_sum = 0
    for num in personal_num[:10]:
        num = int(num)
        num *= multiplier
        control_sum += num
        multiplier += 1
        if multiplier == 10:
            multiplier = 1
    return control_sum


def generate_control_num(personal_num):
    # control num case 1
    control_sum = calculate_control_sum(personal_num, 1)
    control_num = control_sum % 11
    if control_num != 10:
        return control_num
    else:
        # control num case 2
        control_sum = calculate_control_sum(personal_num, 3)
        control_num = control_sum % 11
        if control_num != 10:
            return control_num
        else:
            return 0


def check_length(personal_num):
    if len(personal_num) == 11:
        return True
    return False


def check_gender_and_century(gender_and_century_num=None, year=None, gender=None):
    result = None
    century_gender_map = {
        (1800, "male"): 1,
        (1800, "female"): 2,
        (1900, "male"): 3,
        (1900, "female"): 4,
        (2000, "male"): 5,
        (2000, "female"): 6,
    }
    if year is None and gender is None:
        for value in century_gender_map.values():
            if gender_and_century_num == value:
                result = value
                break
            else:
                result = gender_and_century_num
    elif gender_and_century_num is None:
        year_century = year // 100 * 100
        keys = [x for x in century_gender_map.keys()]

        for y, g in keys:
            if y == year_century and g == gender:
                # generate the gender/century digit
                pre_result = century_gender_map.get((year_century, gender))
                result = check_gender_and_century(pre_result, None, None)
                break
            else:
                if y == year_century and g != gender:
                    result = (year, g)
                elif y != year_century and g == gender:
                    result = (year_century, gender)
                else:
                    result = (year, gender)
    return result


def check_queue_num(num):
    str(num)
    if len(num) == 1:
        return "00" + num
    elif len(num) == 2:
        return "0" + num
    elif len(num) > 3:
        return False
    return num


def check_birth_month(given_month):
    if int(given_month) in range(1, 13):
        return True
    return False


def check_birth_day(given_day):
    if int(given_day) in range(1, 32) or int(given_day) in range(1, 30):
        return True
    return False


def check_control_num(personal_num, given_control_num):
    if generate_control_num(personal_num) == given_control_num:
        return True
    return False


def check_date_format(date_str):
    date_regex = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    return bool(date_regex.match(date_str))


# function to check if given personal num is valid
def personal_number_check(number):
    personal_num = [int(x) for x in str(number)]
    given_gender_and_century = personal_num[0]
    given_control_num = personal_num[-1]
    given_year = str(personal_num[1]) + str(personal_num[2])
    given_month = int(str(personal_num[3]) + str(personal_num[4]))
    given_day = int(str(personal_num[5]) + str(personal_num[6]))

    if not check_length(personal_num):
        return f"Incorrect number length ({len(personal_num)})"
    if not (
        check_gender_and_century(given_gender_and_century, None, None)
        == given_gender_and_century
    ):
        return f"Incorrect first number ({personal_num[0]})"
    if not (check_birth_month(given_month) and check_birth_day(given_day)):
        match given_gender_and_century:
            case 1 | 2:
                return f"Date 18{given_year}-{given_month}-{given_day} is incorrect"
            case 3 | 4:
                return f"Date 19{given_year}-{given_month}-{given_day} is incorrect"
            case 5 | 6:
                return f"Date 20{given_year}-{given_month}-{given_day} is incorrect"
    if not check_control_num(personal_num, given_control_num):
        return (
            f"Incorrect control number (has to be {generate_control_num(personal_num)})"
        )
    return f"National number {number} is valid"


# function to generate personal num from given gender, date and birth queue
def generate_personal_number(gender, date, queue):
    gender_and_century_digit = str()

    if not check_date_format(date):
        return f"Incorrect date format ({date}), must be YYYY-MM-DD"

    year = int(date.split("-")[0])
    month = date.split("-")[1]
    day = date.split("-")[2]

    if not check_birth_month(month):
        return f"Incorrect month ({month}) in date {date}"
    if not check_birth_day(day):
        return f"Incorrect day ({day}) in date {date}"

    if check_gender_and_century(None, year, gender) in range(1, 7):
        gender_and_century_digit = str(check_gender_and_century(None, year, gender))
    else:
        if check_gender_and_century(None, year, gender)[
            1
        ] != gender and check_gender_and_century(None, year, gender)[0] not in range(
            1800, 2100
        ):
            return f"Incorrect year ({year}) and gender ({gender})"
        if check_gender_and_century(None, year, gender)[0] not in range(1800, 2100):
            return f"Incorrect year ({year})"
        if check_gender_and_century(None, year, gender)[1] != gender:
            return f"Incorrect gender ({gender})"

    year_digits = str(year)[2] + str(year)[3]
    queue_digits = str(queue)
    if not check_queue_num(queue_digits):
        return f"Incorrect queue number ({queue})"
    else:
        queue_digits = check_queue_num(queue_digits)

    ten_digits = gender_and_century_digit + year_digits + month + day + queue_digits
    generated_personal_num = int(ten_digits + str(generate_control_num(ten_digits)))

    return generated_personal_num


def main():
    parser = argparse.ArgumentParser(
        description="Validate or generate Lithuanian National ID number."
    )
    subparsers = parser.add_subparsers(
        title="commands", metavar="command", dest="command"
    )

    validate_parser = subparsers.add_parser(
        "validate", help="Validate National ID number."
    )
    validate_parser.add_argument(
        "number", type=int, help="National ID number to validate."
    )

    generate_parser = subparsers.add_parser(
        "generate", help="Generate National ID number."
    )
    generate_parser.add_argument(
        "gender",
        type=str,
        choices=["female", "male"],
        metavar="female, male",
        help="Gender",
    )
    generate_parser.add_argument("date", type=str, help="Date YYYY-MM-DD")
    generate_parser.add_argument("queue", type=int, help="Queue number, integer")

    args = parser.parse_args()

    if args.command == "validate":
        print(personal_number_check(args.number))
    elif args.command == "generate":
        print(generate_personal_number(args.gender, args.date, args.queue))


if __name__ == "__main__":
    main()
