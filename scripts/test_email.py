# cysu v1.5.1 - Тестирование сайта
#!/usr/bin/env python3
"""
Скрипт для тестирования email функциональности cysu

Использование:
    python scripts/test_email.py

Тестирует:
- Отправку email уведомлений
- Подтверждение email
- Сброс пароля
- Конфигурацию SMTP
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, EmailVerification, PasswordReset
from app.utils.email_service import EmailService
from datetime import datetime, timedelta
import random
import string

def test_email_service():
    """Тестирует email сервис"""
    app = create_app()
    
    with app.app_context():
        print("📧 Тестирование email функциональности cysu")
        print("=" * 60)
        
        # Создаем тестового пользователя
        test_user = create_test_user()
        
        # Тестируем email сервис
        email_service = EmailService()
        
        print(f"\n📋 Конфигурация email сервиса:")
        from flask import current_app
        print(f"   - SMTP сервер: {current_app.config.get('MAIL_SERVER')}")
        print(f"   - Порт: {current_app.config.get('MAIL_PORT')}")
        print(f"   - TLS: {current_app.config.get('MAIL_USE_TLS')}")
        print(f"   - Пользователь: {current_app.config.get('MAIL_USERNAME')}")
        
        # Тест 1: Отправка email подтверждения
        print(f"\n🔧 Тест 1: Отправка email подтверждения")
        test_email_verification(email_service, test_user)
        
        # Тест 2: Отправка сброса пароля
        print(f"\n🔑 Тест 2: Отправка сброса пароля")
        test_password_reset(email_service, test_user)
        
        # Тест 3: Проверка кодов подтверждения
        print(f"\n🔍 Тест 3: Проверка кодов подтверждения")
        test_verification_codes(test_user)
        
        # Тест 4: Проверка кодов сброса пароля
        print(f"\n🔐 Тест 4: Проверка кодов сброса пароля")
        test_reset_codes(test_user)
        
        # Очистка тестовых данных
        cleanup_test_data(test_user)
        
        print(f"\n🎉 Тестирование email завершено!")

def create_test_user():
    """Создает тестового пользователя"""
    username = f"test_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    email = f"{username}@test.com"
    
    # Проверяем, существует ли пользователь
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return existing_user
    
    user = User(
        username=username,
        email=email,
        password="test_password",
        is_verified=False,
        is_subscribed=False
    )
    
    db.session.add(user)
    db.session.commit()
    
    print(f"   ✅ Создан тестовый пользователь: {username}")
    return user

def test_email_verification(email_service, user):
    """Тестирует отправку email подтверждения"""
    try:
        print(f"   📧 Отправка email подтверждения для {user.email}")
        
        # Создаем код подтверждения
        verification_code = ''.join(random.choices(string.digits, k=6))
        
        # Создаем запись в базе данных
        verification = EmailVerification(
            user_id=user.id,
            email=user.email,
            code=verification_code,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        db.session.add(verification)
        db.session.commit()
        
        print(f"      ✅ Код подтверждения создан: {verification_code}")
        print(f"      📅 Истекает: {verification.expires_at}")
        
        # В реальном проекте здесь была бы отправка email
        print(f"      📤 Email отправлен (симуляция)")
        
    except Exception as e:
        print(f"   ❌ Ошибка при отправке email подтверждения: {e}")

def test_password_reset(email_service, user):
    """Тестирует отправку сброса пароля"""
    try:
        print(f"   🔑 Отправка сброса пароля для {user.email}")
        
        # Создаем код сброса
        reset_code = ''.join(random.choices(string.digits, k=6))
        
        # Создаем запись в базе данных
        reset = PasswordReset(
            email=user.email,
            code=reset_code,
            expires_at=datetime.utcnow() + timedelta(hours=1)
        )
        db.session.add(reset)
        db.session.commit()
        
        print(f"      ✅ Код сброса создан: {reset_code}")
        print(f"      📅 Истекает: {reset.expires_at}")
        
        # В реальном проекте здесь была бы отправка email
        print(f"      📤 Email отправлен (симуляция)")
        
    except Exception as e:
        print(f"   ❌ Ошибка при отправке сброса пароля: {e}")

def test_verification_codes(user):
    """Тестирует проверку кодов подтверждения"""
    try:
        print(f"   🔍 Проверка кодов подтверждения для {user.username}")
        
        verifications = EmailVerification.query.filter_by(user_id=user.id).all()
        
        if not verifications:
            print("      ⚠️  Коды подтверждения не найдены")
            return
        
        print(f"      📊 Найдено кодов: {len(verifications)}")
        
        for i, verification in enumerate(verifications, 1):
            is_expired = verification.expires_at < datetime.utcnow()
            status = "Истек" if is_expired else "Действителен"
            
            print(f"      {i}. Код: {verification.code}")
            print(f"         Email: {verification.email}")
            print(f"         Статус: {status}")
            print(f"         Истекает: {verification.expires_at}")
        
    except Exception as e:
        print(f"   ❌ Ошибка при проверке кодов подтверждения: {e}")

def test_reset_codes(user):
    """Тестирует проверку кодов сброса пароля"""
    try:
        print(f"   🔐 Проверка кодов сброса пароля для {user.username}")
        
        resets = PasswordReset.query.filter_by(email=user.email).all()
        
        if not resets:
            print("      ⚠️  Коды сброса не найдены")
            return
        
        print(f"      📊 Найдено кодов: {len(resets)}")
        
        for i, reset in enumerate(resets, 1):
            is_expired = reset.expires_at < datetime.utcnow()
            status = "Истек" if is_expired else "Действителен"
            
            print(f"      {i}. Код: {reset.code}")
            print(f"         Email: {reset.email}")
            print(f"         Статус: {status}")
            print(f"         Истекает: {reset.expires_at}")
        
    except Exception as e:
        print(f"   ❌ Ошибка при проверке кодов сброса: {e}")

def cleanup_test_data(user):
    """Очищает тестовые данные"""
    try:
        print(f"\n🧹 Очистка тестовых данных...")
        
        # Удаляем коды подтверждения
        verifications_count = EmailVerification.query.filter_by(user_id=user.id).count()
        EmailVerification.query.filter_by(user_id=user.id).delete()
        
        # Удаляем коды сброса пароля
        resets_count = PasswordReset.query.filter_by(email=user.email).count()
        PasswordReset.query.filter_by(email=user.email).delete()
        
        # Удаляем пользователя
        db.session.delete(user)
        db.session.commit()
        
        print(f"   ✅ Удалено {verifications_count} кодов подтверждения")
        print(f"   ✅ Удалено {resets_count} кодов сброса")
        print(f"   ✅ Удален тестовый пользователь: {user.username}")
        
    except Exception as e:
        print(f"   ❌ Ошибка при очистке: {e}")

def main():
    """Основная функция"""
    try:
        test_email_service()
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
