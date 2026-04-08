Futtatás menete röviden:

Először is, győződjön meg arról, hogy a Python telepítve van a gépen.

A fejlesztői környezet termináljába a következő sorokat írtam:
(ezek akkor kellenek, ha még nincs meg a Playwright)

"pip install playwright" 
"playwright install"


Virtuális környezet létrehozása és aktiválása (nem kötelező, de ajánlom :)):

"py -m venv venv"
".\venv\Scripts\activate"



A kód futtatásához ezt kell a terminálba írni:

"py test_vasarlas.py"  --> Én VSC-t használtam. Más környezetben lehet, hogy py helyett python-t kell írni az elejére.
