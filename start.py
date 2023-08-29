from app import main
import os
app = main()
app.run(port=int(os.environ.get("PORT", 8080)),host="0.0.0.0",debug=True)
# os.system('gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app')
