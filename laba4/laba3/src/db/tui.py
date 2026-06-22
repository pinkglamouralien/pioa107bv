from db.backend.memory import RestaurantDB
from db.backend.errors import DatabaseError


class RestaurantUI:

    def __init__(self):
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

                elif choice == "2":
                    guests = self.db.read_guests()

                    for guest in guests:
                        print(guest)

                elif choice == "3":
                    self.db.create_dish(
                        int(input("ID: ")),
                        input("Название: "),
                        float(input("Цена: "))
                    )

                elif choice == "4":
                    for dish in self.db.read_dishes():
                        print(dish)

                elif choice == "5":
                    self.db.create_order(
                        int(input("ID заказа: ")),
                        int(input("ID гостя: ")),
                        int(input("ID блюда: ")),
                        int(input("Количество: "))
                    )

                elif choice == "6":
                    for order in self.db.read_orders():
                        print(order)

                elif choice == "7":
                    guests = self.db.sort_guests("name")

                    for guest in guests:
                        print(guest)

                elif choice == "0":
                    break

                else:
                    print("Неверный пункт меню.")

            except DatabaseError as error:
                print(error)

            except ValueError as error:
                print(error)