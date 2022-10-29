Python 3.9.7 (tags/v3.9.7:1016ef3, Aug 30 2021, 20:19:38) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import emoji
>>> print(emoji.emojize('Python is :thumbs_up:'))
Python is 👍
>>> print(emoji.emojize('Python is :thumbsup:', language='alias'))
Python is 👍
>>> print(emoji.emojize("Python is fun :red_heart:"))
Python is fun ❤️
>>> print(emoji.emojize('Python es :pulgar_hacia_arriba:', language='es'))
Python es 👍
>>> print(emoji.emojize("Python é :polegar_para_cima:", language='pt'))
Python é 👍
>>> 