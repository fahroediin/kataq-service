# run_web.py
from kataq import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False) # use_reloader=False agar tidak konflik dengan scheduler