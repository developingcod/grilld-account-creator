# Automated Account Creator for Grill'd Mad Bunday Promotion

This Python script automates the process of creating and verifying accounts on `digital.grilld.com.au`. It includes functionalities for generating possible email variations, verifying their existence through the Grill'd API, and then registering accounts with those emails. Successfully registered accounts are saved in a CSV file.

This is for their current AFL promotion Mad Bunday ([Mad Bunday](https://cloud.email.grilld.com.au/mad-bunday?utm_source=google&utm_medium=paid&utm_campaign=mad_bunday_2024&utm_content=Search&gad_source=1&gclid=Cj0KCQjw_qexBhCoARIsAFgBleu5bo7GXRejCoNNtVlRxw7caiB_BX2vFojR0BM-jmjeVErNxZbjyzIaAnrIEALw_wcB))

Once the promotion is over this will be a useless script, as its intent is to exploit the 2 for 1 burger along with the free chips during your birthday month.

## Features

- **Email Generation**: Generates possible email variations based on a provided base email.
- **Email Verification**: Verifies each generated email through the Grill'd API.
- **Account Registration**: Registers accounts using the verified emails and saves the successful registrations.
- **Multi-threading**: Utilizes threading to speed up the process of email verification and account registration.
- **Data Persistence**: Outputs the registered account details into a CSV file for later use.

## Prerequisites

Before running the script, make sure you have Python 3 installed on your system. Python 3.6 or higher is required due to the use of f-strings and other newer Python features.

## Setup and Installation

1. **Install Python 3**
   - If you do not have Python installed, you can download it from the official Python website ([python.org](https://python.org)) or install it via a package manager on your operating system.

2. **Clone the Repository**
   ```bash
   git clone https://github.com/developingcod/grilld-account-creator.git
   cd grilld-account-creator
   ```

3. **Install Required Python Modules**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Prepare the Data File**
   - Create a JSON file named `data.json` in the root directory of the project.
   - The JSON file should contain the following keys:
   ```json
   {
    "email": "testemail@gmail.com",
    "firstName": "TestFirstName",
    "lastName": "TestLastName",
    "mobileNumber": "0400123456",
    "birthYear": "1990"
  }
   ```
   This file includes the base details used for account creation.
   
   - **Email**: Your Gmail address.
    - **firstName**: Your First Name.
    - **lastName**: Your Last Name.
    - **mobileNumber**: Your Mobile Number.
    - **birthYear**: Your Birth Yeart.
   
   NOTE: Gmail is to be only used in the "email" section of `data.json`



## Usage

To run the script, simply execute the main Python file from your terminal:

```bash
python account_creator.py
```

The script will perform the following steps:
- Load the user data from `data.json`.
- Generate email variations and verify their existence using the Grill'd API.
- Register accounts with verified emails.
- Save successful registrations to `accounts.csv`.

## Output

After running the script, check the `accounts.csv` file in the project directory. This file contains the details of successfully registered accounts, formatted as follows:
- **Email**: The registered email address.
- **Password**: The generated password for the account.
- **Birth Date**: The randomly selected birth date used for registration.
- **AFL Team**: The AFL team associated with the account (used in some promotions).

## Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your changes or improvements.

## License

This project is released under the MIT License. See the LICENSE file in the repository for full details.

```
