#!/usr/bin/env python3
"""
Скрипт для очистки всех тестовых данных

Использование:
    python scripts/cleanup_all_tests.py

Очищает:
- Все тестовые пользователи
- Все тестовые предметы и материалы
- Все orphaned записи
- Временные файлы
"""

import sys
import os
from pathlib import Path

# Добавляем корневую директорию проекта в путь
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.test_utils import global_cleanup


def main():
    """Главная функция"""
    print("🧹 ОЧИСТКА ВСЕХ ТЕСТОВЫХ ДАННЫХ CYSU")
    print("=" * 60)
    print("⚠️  ВНИМАНИЕ: Этот скрипт удалит ВСЕ тестовые данные!")
    print("   Убедитесь, что вы хотите это сделать.")
    print()
    
    # Запрашиваем подтверждение
    confirm = input("Продолжить очистку? (y/N): ").strip().lower()
    
    if confirm not in ['y', 'yes', 'да']:
        print("❌ Очистка отменена.")
        return
    
    print()
    print("🚀 Начинаем очистку...")
    
    try:
        global_cleanup()
        print("\n🎉 Очистка завершена успешно!")
        
    except Exception as e:
        print(f"\n❌ Ошибка при очистке: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
