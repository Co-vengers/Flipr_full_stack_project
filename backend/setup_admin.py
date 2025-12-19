# backend/setup_admin.py
#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def create_admin_and_get_token(username='admin', email='admin@example.com', password='admin123'):
    # Check if user exists
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'is_admin': True,
            'is_staff': True,
            'is_superuser': True,
            'is_active': True
        }
    )
    
    if created:
        user.set_password(password)
        user.save()
        print(f"\n✅ Admin user created successfully!")
    else:
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()
        print(f"\n✅ Admin user updated successfully!")
    
    # Generate JWT token
    refresh = RefreshToken.for_user(user)
    
    print(f"\n📋 Admin Credentials:")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    print(f"   Email: {email}")
    
    print(f"\n🔐 JWT Tokens:")
    print(f"   Access Token: {refresh.access_token}")
    print(f"   Refresh Token: {refresh}")
    
    print(f"\n🌐 Login URLs:")
    print(f"   Frontend Dashboard: http://localhost:3000/admin/login")
    print(f"   Django Admin: http://localhost:8000/admin")
    
    print(f"\n📝 Quick Test Command:")
    print(f"   curl -X POST http://localhost:8000/api/auth/login/ \\")
    print(f"     -H 'Content-Type: application/json' \\")
    print(f"     -d '{{\"username\": \"{username}\", \"password\": \"{password}\"}}'")
    
    return {
        'user': user,
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh)
    }

if __name__ == '__main__':
    create_admin_and_get_token()