from database.crud import Crud


class Helpers:
    """
    Helper functions.
    """

    def __init__(self) -> None:
        self.crud = Crud()

    def add_default_product(self) -> None:
        """
        Add default product data to the DB.
        """
        products = [
            {
                "name": "Селяночка",
                "sku": 1052,
                "id": 1,
            },
            {
                "name": "Красная птица",
                "sku": 1128,
                "id": 2,
            },
            {
                "name": "Лента",
                "sku": 1729,
                "id": 3,
            },
            {
                "name": "Батон нарезной ВС",
                "sku": 288,
                "id": 4,
            },
            {
                "name": "Дедовский хлеб",
                "sku": 421,
                "id": 5,
            },
            {
                "name": "Щедрый год",
                "sku": 4369,
                "id": 6,
            },
            {
                "name": "Магнит",
                "sku": 588,
                "id": 7,
            },
            {
                "name": "Батон нарезной",
                "sku": 90060,
                "id": 8,
            },
            {
                "name": "Магнит ВП",
                "sku": 91952,
                "id": 9,
            },
            {
                "name": "К&Б",
                "sku": 1249,
                "id": 10,
            },
        ]

        for product in products:
            self.crud.add_product(product["name"], product["sku"], product["id"])
