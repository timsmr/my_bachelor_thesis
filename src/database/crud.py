from datetime import datetime

from sqlalchemy import desc, func

from database import model
from database.database import session as db


class Crud:

    @staticmethod
    def add_product(name: str, sku: int, id: int) -> None:
        order_obj = db.query(model.Product).filter_by(sku=sku).first()
        if order_obj is None:
            obj_product = model.Product(
                name=name,
                sku=sku,
                id=id,
            )
            db.add(obj_product)
            db.commit()

    @staticmethod
    def add_result_detect(content: dict) -> None:
        obj_result = model.Result(
            tray_id=content["tray_id"],
            sku_id=content["sku_id"],
            count_of_loaf=content["count_of_loaf"],
            deviation_detected=content["deviation_detected"],
            last_change_sku_time=content["last_change_sku_time"],
            detected_time=content["detected_time"],
        )
        db.add(obj_result)
        db.commit()

    @staticmethod
    def get_start_data() -> tuple[int, int, datetime]:
        tray_id = db.query(func.max(model.Result.tray_id)).scalar()
        tray_id = tray_id + 1 if tray_id else 1

        last_change_sku_time = (
            db.query(model.Result).order_by(
                desc(model.Result.last_change_sku_time)).first()
        )
        last_change_sku_time = (
            last_change_sku_time.last_change_sku_time
            if last_change_sku_time
            else datetime.now()
        )

        last_change_sku = (
            db.query(model.Result.sku_id)
            .filter(
                model.Result.last_change_sku_time == last_change_sku_time,
            )
            .order_by(desc(model.Result.created))
            .first()
        )

        last_change_sku = last_change_sku.sku_id if last_change_sku else 1

        return tray_id, last_change_sku, last_change_sku_time
