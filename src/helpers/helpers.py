from database.crud import add_product


class Helpers:
    """
    Helper functions.
    """
    @staticmethod
    def add_default_product() -> None:
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
            add_product(product["name"], product["sku"], product["id"])
