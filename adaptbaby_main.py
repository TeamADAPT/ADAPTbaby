# ... (previous imports and configurations)

@app.route('/test_models_ui')
@login_required
def test_models_ui():
    return render_template('test_models.html')

# ... (rest of the existing code)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Create an admin user if it doesn't exist
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_password = os.environ.get('ADMIN_PASSWORD', 'admin_password')
            hashed_password = bcrypt.generate_password_hash(admin_password).decode('utf-8')
            admin_user = User(username='admin', password=hashed_password, is_admin=True)
            db.session.add(admin_user)
            db.session.commit()
    logger.info("ADAPTbaby application created. Starting the server...")
    app.run(host='0.0.0.0', port=8080, debug=True)
