# Innovation Lab Newsletter Project

## Before running the program
- Fork the repository
- On your local system, run
  ```shell
    $ git clone https://github.com/<Your_Username_Here>/Innovation-Lab-Newsletter.git
  ```
- Move into the directory
  ```shell
    $ cd Innovation-Lab-Project-2
  ```
- On your terminal, run
  ```sh
    $ pip install -r requirements.txt
  ```
- Make a file named `.env` in the root folder, with the following contents:
  ```env
  LOGIN_EMAIL="<email id of test email>"
  LOGIN_PASSWORD="<password of the test email>"
  
  EMAIL_STORE_PATH="data/emails.txt"
  ```

## How to Run
- To run the application:
  ```shell
    $ cd src
    $ streamlit run app.py  
  ```
