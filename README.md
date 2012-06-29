Kokobox
=======

This is the Kokobox, based on the Piratebox principle, but written in Python.

Install
-------

Install flask:
pip install flask

Run
---

python kokobox.py

Then go to localhost:5000 to see the beauty.

If you want to make it public, you can use gunicorn (pip install gunicorn) as
follows :

gunicorn -b ip-address:port kokobox:app (in kokobox folder)

