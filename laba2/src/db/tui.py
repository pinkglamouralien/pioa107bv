from db.backend.memory import *

def run():

    while True:
        print("\n===== БАЗА ДАННЫХ РЕСТОРАНА =====")
        print("1. Добавить гостя")
        print("2. Показать гостей")
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
                create_guest(
                    int(input("ID: ")),
                    input("Имя: "),
                    input("Телефон: ")
                )

                print("Гость добавлен.")

            elif choice == "2":
                name = input(
                    "Имя для поиска (Enter - все): "
                )

                if name:
                    guests = read_guests(name)
                else:
                    guests = read_guests()

                for guest in guests:
                    print(guest)

            elif choice == "3":
                create_dish(
                    int(input("ID: ")),
                    input("Название: "),
                    float(input("Цена: "))
                )

                print("Блюдо добавлено.")

            elif choice == "4":
                for dish in read_dishes():
                    print(dish)

            elif choice == "5":
                create_order(
                    int(input("ID заказа: ")),
                    int(input("ID гостя: ")),
                    int(input("ID блюда: ")),
                    int(input("Количество: "))
                )

                print("Заказ добавлен.")

            elif choice == "6":
                for order in read_orders():
                    print(order)

            elif choice == "7":
                update_guest(
                    int(input("ID гостя: ")),
                    input("Новое имя: "),
                    input("Новый телефон: ")
                )

                print("Гость обновлён.")

            elif choice == "8":
                delete_guest(
                    int(input("ID гостя: "))
                )

                print("Гость удалён.")

            elif choice == "0":
                break

            else:
                print("Неверный пункт меню.")

        except ValueError as error:
            print("Ошибка:", error)