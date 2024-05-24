from charging.service import ChargingService

if __name__ == "__main__":
    service = ChargingService(dry_run=True)
    service.smart_charge()
