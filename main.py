from charging.service import ChargingService

if __name__ == "__main__":
    service = ChargingService()
    service.run_in_background()
