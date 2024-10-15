# ... (previous imports)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# ... (previous code)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# ... (previous code)

@app.route('/test_models', methods=['POST'])
@login_required
@limiter.limit("10 per minute")
def test_models():
    # ... (existing code)

# ... (rest of the code)
