![flexihome-logo](docs/logo/flexihome-logo.png)

---

# FlexiHome: A Home Energy Management System 🔌<br><br>Statistics Manager

## Description

This repository contains the Statistics Manager Service, a core component of the Home Energy Management System (HEMS). The Statistics Manager Service is responsible for processing energy data and providing users with useful statistics, such as energy cost for the day, monthly injection, yearly consumption, and CO2 footprint. It exposes a REST API for querying statistics and producing events for data storage.

## Table of Contents

- [FlexiHome: A Home Energy Management System 🔌Statistics Manager](#flexihome-a-home-energy-management-system-statistics-manager)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [HEMS Overview](#hems-overview)
    - [Visit all the FlexiHome micro-services:](#visit-all-the-flexihome-micro-services)
  - [Project details](#project-details)
    - [Repository Structure](#repository-structure)
    - [Project Status](#project-status)
    - [Technology Stack](#technology-stack)
    - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Known Issues](#known-issues)
  - [Open Source Licensing Info](#open-source-licensing-info)
  - [OpenAPI Documentation](#openapi-documentation)
    - [Contacts](#contacts)

## HEMS Overview

EMSs (Energy Management Systems) play a key role in the flexibility enablement of consumers, residential and tertiary, which is paramount to accessing the previously untapped flexibility potential of residential DERs (Distributed Energy Resources). These resources, under the form of energy assets, are usually household appliances like heat pumps, EV chargers, dishwashers, PV inverts, batteries, etc. This is where the FlexiHome (Home Energy Management System) comes in. 

The goal of this system is to facilitate the user’s participation in the flexibility value chain, while providing them with incentives in a clear, explainable way.

To fulfill this goal in an effective and scalable way, the FlexiHome is designed with a micro-services architecture (below), orchestrated in a Kubernetes environment, where each micro-service is modular and can be replaced or expanded, without breaking the remaining logic.

![FlexiHome Architecture](docs/diagrams/hems-architecture-diagram.svg)

FlexiHome utilizes an IoT interoperable gateway (FlexiHome Hub) to connect to the end users DERs via interoperable protocols like OCPP and Modbus, which connects with the cloud system (FlexiHome Cloud) via an MQTT message broker.

The cloud operations are done via micro-services, where the flexibility optimization algorithms run. To complement these micro-services, support applications like postgres (database), elasticsearch (log database), prometheus (performance metrics) and grafana (metrics dashboard) are used.

Lastly, the user can view the information regarding their devices and flexibility on a user interface provided by the mobile app, which accesses the FlexiHome microservices using a REST API Gateway for additional security measures and routing of requests.

### Visit all the FlexiHome micro-services:
- [FlexiHome Account Manager](https://github.com/INESCTEC/hems-account-manager) - Manages user accounts, authentication, and implements cybersecurity measures within the FlexiHome ecosystem
- [FlexiHome Statistics Manager](https://github.com/INESCTEC/hems-statistics-manager) - Collects and processes data gathered from IoT devices connected to the FlexiHome ecosystem
- [FlexiHome Device Manager](https://github.com/INESCTEC/hems-device-manager) - Responsible for the integration and management of IoT devices to the FlexiHome ecosystem
- [FlexiHome Energy Manager](https://github.com/INESCTEC/hems-energy-manager) - Receives grid needs inputs from system operators and user comfort inputs to optimized the flexibility bids taken to market 
- [FlexiHome Hub](https://github.com/INESCTEC/hems-hub) - IoT interoperable gateway that implements the communication, using MQTT protocol, between the DERs and the FlexiHome services on the cloud
- [FlexiHome Mobile App](https://github.com/INESCTEC/hems-app) - mobile application targetted for residential end consumers to manage their flexible DERs. Available in Android and iOS

## Project details

### Repository Structure

```bash
.                      # Root directory of the repository
├── statistics_manager_service/  # Main source code for the Statistics Manager Service
│   ├── controllers/    # API controllers for statistics queries
│   ├── event_consumer/ # Kafka consumer and event processing
│   ├── event_producers/ # Kafka producers for statistics events
│   ├── exception_handling_utils/ # Exception handling utilities
│   ├── models/         # Data models and schemas
│   ├── openapi/        # OpenAPI specification
│   ├── test/           # Unit and integration tests
│   └── ...             # Other supporting modules
├── Dockerfile          # Docker configuration for containerization
├── requirements.txt    # Python dependencies
├── service-specific-requirements.txt # Additional dependencies
├── test-requirements.txt # Testing dependencies
├── setup.py            # Python package setup
├── Docker-compose/     # Docker Compose files and monitoring configs
├── statistics-manager-openapi.yaml # OpenAPI specification (root)
├── README.md           # Main documentation
```

### Project Status

- 🚧 In Progress: Actively being developed; features and structure may change.

### Technology Stack

- **Programming Language:** Python 3.8+
- **Frameworks/Libraries:** Flask, Connexion, SQLAlchemy, Marshmallow, Kafka-Python, Pandas, Numpy
- **Containerization:** Docker, Docker Compose
- **Orchestration:** Kubernetes (recommended for deployment)
- **Other Tools:** Prometheus, pytest

### Dependencies

All required Python packages are listed in `requirements.txt` and `service-specific-requirements.txt`. For testing, see `test-requirements.txt`. Docker and Docker Compose are required for containerized deployments.

## Installation

Follow these steps to install and set up the Statistics Manager Service:

1. **Clone the repository:**

```bash
git clone https://github.com/INESCTEC/hems-statistics-manager.git
cd statistics-manager-service
```

2. **Create and activate a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
   Edit your environment variables as needed for database and Kafka configuration. See `statistics_manager_service/config.py` for available options.

5. **(Optional) Build and run with Docker:**

```bash
docker-compose up --build
```

## Usage

To start the Statistics Manager Service:

```bash
source venv/bin/activate
python -m statistics_manager_service
```

Or, if using Docker Compose:

```bash
cd Docker-compose
docker-compose up
```

Access the API documentation and endpoints as defined in the OpenAPI spec (`statistics-manager-openapi.yaml` or `statistics_manager_service/openapi/openapi.yaml`), which can be opened using [Swagger Editor](https://editor.swagger.io/).

## Known Issues

- No major issues reported. Please use GitHub Issues to report bugs or request features.

## Open Source Licensing Info

See [`LICENSE`](LICENSE) for details on usage rights and licensing.

## OpenAPI Documentation

See [`statistics-manager-openapi.yaml`](statistics-manager-openapi.yaml) for the OpenAPI specification. You can view and test endpoints using [Swagger Editor](https://editor.swagger.io/).

### Contacts

For questions or support, contact:

- Vasco Manuel Campos: vasco.m.campos@inesctec.pt
- Daniel Barros: daniel.barros@inesctec.pt
