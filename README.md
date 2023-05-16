# django_with_selinium

sudo apt-get update

sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3

sudo pip3 install virtualenv

mkdir django

cd django

virtualenv myprojectenv

git clone https://github.com/kvsnrkolapalli/django_with_selinium/

source myprojectenv/bin/activate

cd django_with_selinium

sudo vi WebApp/settings.py

Note: Add instance’s DNS name/IP to “Allowed Hosts” in settings.py
ALLOWED_HOSTS=['EC2_DNS_NAME']

pip install -r requirements.txt

sudo apt-get install chromium-chromedriver

python manage.py runserver 0.0.0.0:8000

