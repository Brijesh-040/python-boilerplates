
1. Build the docker
    * `docker build -t fast-api .`
2. Run the docker
    * `docker run -d -p 8001:80 fast-api`
--------------------------------------------------------------------------------
1. Install dep
    * `pip install -r requirements.txt`

3. Run in local
    * `uvicorn main:app --reload`
    * `uvicorn main:app --reload --port 8001`       // specific port

4. Create env
    * `python311 -m venv modules`

5. Activate env [From cmd in windows]
    * `modules\Scripts\activate`

5. Activate env [From MAC or linux]
    * `source modules/bin/activate`

6. Deactivate env
    * `deactivate`


python version = 3.11.6#   p y t h o n - b o i l e r p l a t e s 
 
 