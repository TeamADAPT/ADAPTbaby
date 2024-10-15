# ... (previous code)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    api_calls_quota = db.Column(db.Integer, default=1000)
    api_calls_count = db.Column(db.Integer, default=0)

# ... (rest of the code)

@app.route('/test_models', methods=['POST'])
@login_required
@limiter.limit("10 per minute")
def test_models():
    if current_user.api_calls_count >= current_user.api_calls_quota:
        return jsonify({"error": "API call quota exceeded"}), 429

    # Increment the API call count
    current_user.api_calls_count += 1
    db.session.commit()

    # ... (rest of the existing code)

# Add an admin route to manage user quotas
@app.route('/admin/manage_quota/<int:user_id>', methods=['POST'])
@login_required
def manage_quota(user_id):
    if not current_user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    user = User.query.get_or_404(user_id)
    new_quota = request.json.get('new_quota')
    
    if new_quota is not None:
        user.api_calls_quota = new_quota
        db.session.commit()
        return jsonify({"message": "Quota updated successfully"})
    else:
        return jsonify({"error": "Invalid quota value"}), 400

# ... (rest of the code)
