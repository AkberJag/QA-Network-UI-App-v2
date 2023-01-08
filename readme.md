Install the requirements by running

```
pip3 install requirements.txt
```

Then make migrations by running the three commands:
```
flask db init
```
```
flask db migrate -m "Initial migration."
```
```
flask db upgrade
```
