from db.backend.memory import Guests, Dishes, Orders
from db.backend.errors import DBError

class RestaurantUI:
    def run(self):
        while True:
            self.show_menu()
            choice = input("Выберите действие: ")
            
            if choice == "0":
                break
                
            try:
                self.handle_choice(choice)
            except DBError as error:
                print(f"Ошибка базы данных: {error}")
            except ValueError:
                print("Ошибка ввода: проверьте типы данных (ожидалось число).")
            except Exception as e:
                print(f"Неизвестная ошибка: {e}")

    def show_menu(self):
        print("\n===== БАЗА ДАННЫХ РЕСТОРАНА =====")
        print("1. Добавить гостя")
        print("2. Показать гостей (с фильтром и сортировкой)")
        print("3. Добавить блюдо")
        print("4. Показать блюда")
        print("5. Добавить заказ")
        print("6. Показать заказы")
        print("7. Обновить гостя")
        print("8. Удалить гостя")
        print("0. Выход")

    def get_sort_params(self):
        sort_by = input("Сортировать по полю (Enter - пропустить): ")
        if not sort_by:
            return None, False
        reverse_ans = input("По убыванию? (y/n): ").lower()
        return sort_by, reverse_ans == 'y'

    def handle_choice(self, choice):
        if choice == "1":
            Guests.create({
                "guest_id": int(input("ID: ")),
                "name": input("Имя: "),
                "phone": input("Телефон: ")
            })
            print("Гость добавлен.")

        elif choice == "2":
            name = input("Имя для фильтра (Enter - пропустить): ")
            filters = {}
            if name: filters["name"] = name
            
            sort_by, reverse = self.get_sort_params()
            
            for guest in Guests.read(sort_by=sort_by, reverse=reverse, **filters):
                print(guest)

        elif choice == "3":
            Dishes.create({
                "dish_id": int(input("ID: ")),
                "name": input("Название: "),
                "price": float(input("Цена: "))
            })
            print("Блюдо добавлено.")

        elif choice == "4":
            sort_by, reverse = self.get_sort_params()
            for dish in Dishes.read(sort_by=sort_by, reverse=reverse):
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
            guest_id = int(input("ID гостя: "))
            new_name = input("Новое имя (Enter - оставить старое): ")
            new_phone = input("Новый телефон (Enter - оставить старое): ")
            
            updates = {}
            if new_name: updates["name"] = new_name
            if new_phone: updates["phone"] = new_phone
            
            if updates:
                Guests.update(guest_id, **updates)
                print("Гость обновлён.")
            else:
                print("Нет данных для обновления.")

        elif choice == "8":
            Guests.delete(int(input("ID гостя: ")))
            print("Гость удалён.")