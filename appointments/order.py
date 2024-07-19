ORDER_SESSION_ID = "order"


class Order:
    def __init__(self, request):
        self.session = request.session
        order = self.session.get(ORDER_SESSION_ID)
        if order is None:
            order = self.session[ORDER_SESSION_ID] = {}
        self.order = order

    def add(self, doctor_pk, start_date, price):
        self.order["doctor_pk"] = doctor_pk
        self.order["start_date"] = start_date
        self.order["price"] = price
        self.save()

    def get_doctor_pk(self):
        return self.order["doctor_pk"]

    def get_start_date(self):
        return self.order["start_date"]

    def get_price(self):
        return self.order["price"]

    def set_status(self, status):
        self.order["status"] = status
        self.save()

    def get_status(self):
        return self.order["status"]

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[ORDER_SESSION_ID]
        self.save()
