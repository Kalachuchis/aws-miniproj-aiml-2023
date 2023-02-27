import logging

log = logging.getLogger()
log.setLevel(logging.INFO)


class Employee:
    def __init__(self, **kwargs):
        try:
            self.first_name = kwargs["first_name"]
            self.last_name = kwargs["last_name"]
            self.employee_number = kwargs["employee_number"]
            self.role = kwargs["position"]
        except KeyError as e:
            log.error(
                f"Missing parameters: {str(e)}",
            )
