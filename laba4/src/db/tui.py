from src.db.backend.memory import RestaurantDB
from src.db.backend.json_db import JSONRestaurantDB
from src.db.backend.csv_db import CSVRestaurantDB
from src.db.backend.errors import DatabaseError

class RestaurantUI:

    def __init__(self):
        print("Выберите тип базы данных:")
        print("1. In-memory (без сохранения)")
        print("2. Файловая БД (JSON)")
        print("3. Файловая БД (CSV)")

        choice = input("Введите номер: ").strip()

        if choice == "2":
            self.db = JSONRestaurantDB()
        elif choice == "3":
            self.db = CSVRestaurantDB()
        else:
            self.db = RestaurantDB()

    def run(self):
        while True:
            print("\n===== БАЗА ДАННЫХ РЕСТОРАНА =====")
            print("1. Добавить гостя")
            print("2. Показать гостей")
            print("3. Добавить блюдо")
            print("4. Показать блюда")
            print("5. Добавить заказ")
            print("6. Показать заказы")
            print("7. Сортировать гостей")
            print("0. Выход")

            choice = input("Выберите действие: ")

            try:
                if choice == "1":
                    self.db.create_guest(
                        int(input("ID: ")),
                        input("Имя: "),
                        input("Телефон: ")
                    )
                    print("-> Гость успешно добавлен.")

                elif choice == "2":
                    guests = self.db.read_guests()
                    if not guests:
                        print("-> Список гостей пуст.")
                    else:
                        for guest in guests:
                            print(guest)

                elif choice == "3":
                    self.db.create_dish(
                        int(input("ID: ")),
                        input("Название: "),
                        float(input("Цена: "))
                    )
                    print("-> Блюдо успешно добавлено.")

                elif choice == "4":
                    dishes = self.db.read_dishes()
                    if not dishes:
                        print("-> Меню пусто.")
                    else:
                        for dish in dishes:
                            print(dish)

                elif choice == "5":
                    self.db.create_order(
                        int(input("ID заказа: ")),
                        int(input("ID гостя: ")),
                        int(input("ID блюда: ")),
                        int(input("Количество: "))
                    )
                    print("-> Заказ успешно создан.")

                elif choice == "6":
                    orders = self.db.read_orders()
                    if not orders:
                        print("-> Список заказов пуст.")
                    else:
                        for order in orders:
                            print(order)

                elif choice == "7":
                    guests = self.db.sort_guests("name")
                    if not guests:
                        print("-> Список гостей пуст.")
                    else:
                        for guest in guests:
                            print(guest)

                elif choice == "0":
                    print("-> Завершение работы.")
                    break

                else:
                    print("-> Неверный пункт меню.")

            except DatabaseError as error:
                print(f"-> Ошибка базы данных: {error}")

            except ValueError as error:
                print(f"-> Ошибка ввода: {error}")