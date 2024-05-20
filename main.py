from inverter.service import InverterService

if __name__ == "__main__":
    service = InverterService()
    print(service.fetch_data())
