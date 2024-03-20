# Scraping Server + TELEGRAM BOT + API + trainy Api-Notes

#### Stack:

- [Python](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Django](https://www.djangoproject.com/)
- [BOOTSTRAP](https://getbootstrap.com/docs/4.1/getting-started/introduction/)
- [CSS](https://www.w3schools.com/css/)
- [HTML](https://www.w3schools.com/html/)
- [TELEGRAM-API](https://core.telegram.org/)
- [NGROK](https://ngrok.com/)
  

## Local Developing

All actions should be executed from the source directory of the project and only after installing all requirements.

1. Firstly, create and activate a new virtual environment:
   ```bash
   python3.11 -m venv ../venv
   source ../venv/bin/activate
   ```
   
2. Install packages:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   
3. Run project dependencies, migrations, fill the database with the fixture data etc.:
   ```bash
   ./manage.py migrate
   ./manage.py loaddata <path_to_fixture_files>
   ./manage.py runserver 
   ```
   
4. Start project:
    ```bash
   python manage.py runserver
   ```

5. Install ngrok for create tunneling between telegram-bot and project(webhook):
   ```bash
   pip install 
   ```
   
6. Running ngrok:
    ```bash
    ngrok http 5000(or your IP address(localhost and etc.))
    ```
   Copy this address:
   ![ngrok](https://github.com/IlyaKavaleu/api_notes/assets/97099564/f891abb1-8983-4cc1-a144-a254a8aa0ad5)

   Open browser and enter:
   ```bash
   https://api.telegram.org/bot[YOUR BOT TOKEN]/setWebhook?url=[NGROK ADDRESS]
   ```
   If you see: {"ok":true,"result":true,"description":"Webhook was set"}, you all made good.
   If {"ok":true,"result":true,"description":"Not found"} and another mistakes, repeat all process!
   

8. Go to the scraping_service application(src/.../scraping_service) and enter:
   ```bash
   python manage.py runserver
   ```
