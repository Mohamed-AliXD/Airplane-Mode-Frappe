# Airplane Mode

A Frappe app (v16) for airplane ticket management and airport shop management.

## Features

- **Flights and tickets:** flights with gate and crew; tickets pick up the flight's gate number.
- **Airport shops:** Shop, Shop Type, Shop Tenant, Shop Contract, Shop Settings, Shop Lead and Rent Payment doctypes. An active contract marks a shop as Occupied.
- **Monthly rent reminders:** a scheduled job (`tasks.send_rent_reminders`, 9:00 on the 1st) creates a Rent Payment and emails the tenant for each active contract.
- **Reports and print format:** Airport Shop Occupancy report and Rent Receipt print format.
- **Website:** public `/shops` and `/shops/<name>` pages, plus a Shop Lead web form.
- **REST API:** use `/api/resource/Shop` with a `token key:secret` header.

## Install

```bash
cd ~/frappe/frappe-bench
bench get-app /path/to/airplane_mode
bench --site site1.local install-app airplane_mode
bench --site site1.local migrate
```

## Run the reminder job manually

```bash
bench --site site1.local execute airplane_mode.airport_shop_management.tasks.send_rent_reminders
```

## License

MIT
