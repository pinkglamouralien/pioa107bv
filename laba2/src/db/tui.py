from db.backend.memory import Guests, Dishes, Orders

def run():
    while True:
        print("\n===== БАЗА ДАННЫХ РЕСТОРАНА =====")
        print("1. Добавить гостя")
        print("2. Показать гостей (с фильтрацией)")
        print("3. Добавить блюдо")
        print("4. Показать блюда")
        print("5. Добавить заказ")
        print("6. Показать заказы")
        print("7. Обновить гостя")
        print("8. Удалить гостя")
        print("0. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                Guests.create({
                    "guest_id": int(input("ID: ")),
                    "name": input("Имя: "),
                    "phone": input("Телефон: ")
                })
                print("Гость добавлен.")

            elif choice == "2":
                print("Оставьте поле пустым, если фильтр не нужен.")
                name = input("Имя для фильтра: ")
                phone = input("Телефон для фильтра: ")
                
                filters = {}
                if name: filters["name"] = name
                if phone: filters["phone"] = phone
                
                for guest in Guests.read(**filters):
                    print(guest)

            elif choice == "3":
                Dishes.create({
                    "dish_id": int(input("ID: ")),
                    "name": input("Название: "),
                    "price": float(input("Цена: "))
                })
                print("Блюдо добавлено.")

            elif choice == "4":
                for dish in Dishes.read():
                    print(dish)

            elif choice == "5":
                Orders.create({
                    "order_id": int(input("ID заказа: ")),
                    "guest_id": int(input("ID гостя: ")),
                    "dish_id": int(input("ID блюда: ")),
                    "quantity": int(input("Количество: "))
                })
                print("Заказ добавлен.")

            elif choice == "6":
                for order in Orders.read():
                    print(order)

            elif choice == "7":
                Guests.update(
                    int(input("ID гостя: ")),
                    name=input("Новое имя: "),
                    phone=input("Новый телефон: ")
                )
                print("Гость обновлён.")

            elif choice == "8":
                Guests.delete(int(input("ID гостя: ")))
                print("Гость удалён.")

            elif choice == "0":
                break

            else:
                print("Неверный пункт меню.")

        except ValueError as error:
            print("Ошибка:", error)