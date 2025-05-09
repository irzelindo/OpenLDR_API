# OpenLDR API

A RESTful API for managing OpenLDR repository data, providing endpoints for Tuberculosis (TB) GeneXpert, HIV Viral Load, and facility/laboratory information.

## Table of Contents
- [Overview](#overview)
- [API Documentation](#api-documentation)
  - [Tuberculosis GeneXpert Endpoints](#tuberculosis-genexpert-endpoints)
  - [HIV Viral Load Endpoints](#hiv-viral-load-endpoints)
  - [Dictionary Endpoints](#dictionary-endpoints)
- [Common Parameters](#common-parameters)
- [Getting Started](#getting-started)
- [Error Handling](#error-handling)

## Overview

The OpenLDR API provides a comprehensive set of endpoints for accessing and managing laboratory data, particularly focused on Tuberculosis GeneXpert testing and HIV Viral Load monitoring. The API is built using Flask and Flask-RESTful, with Swagger documentation for easy integration.

## API Documentation

### Tuberculosis GeneXpert Endpoints

#### Facilities Endpoints
- `GET /tb/gx/facilities/registered_samples/` - Get total number of samples registered by facility
- `GET /tb/gx/facilities/tested_samples/` - Get total number of samples tested by facility
- `GET /tb/gx/facilities/tested_samples_disaggregated/` - Get tested samples disaggregated by facility
- `GET /tb/gx/facilities/tested_samples_disaggregated_by_gender/` - Get tested samples disaggregated by gender
- `GET /tb/gx/facilities/tested_samples_disaggregated_by_age/` - Get tested samples disaggregated by age
- `GET /tb/gx/facilities/tested_samples_types_disaggregated_by_age/` - Get tested sample types disaggregated by age
- `GET /tb/gx/facilities/tested_samples_disaggregated_by_drug_type/` - Get tested samples disaggregated by drug type
- `GET /tb/gx/facilities/tested_samples_disaggregated_by_drug_type_by_age/` - Get tested samples disaggregated by drug type and age

#### Laboratory Endpoints
- `GET /tb/gx/laboratories/registered_samples/` - Get registered samples by laboratory
- `GET /tb/gx/laboratories/tested_samples/` - Get tested samples by laboratory
- `GET /tb/gx/laboratories/registered_samples_by_month/` - Get registered samples by laboratory by month
- `GET /tb/gx/laboratories/tested_samples_by_month/` - Get tested samples by laboratory by month
- `GET /tb/gx/laboratories/rejected_samples/` - Get rejected samples by laboratory
- `GET /tb/gx/laboratories/rejected_samples_by_month/` - Get rejected samples by laboratory by month
- `GET /tb/gx/laboratories/rejected_samples_by_reason/` - Get rejected samples by reason
- `GET /tb/gx/laboratories/rejected_samples_by_reason_by_month/` - Get rejected samples by reason by month
- `GET /tb/gx/laboratories/tested_samples_by_drug_type/` - Get tested samples by drug type
- `GET /tb/gx/laboratories/tested_samples_by_drug_type_by_month/` - Get tested samples by drug type by month
- `GET /tb/gx/laboratories/trl_samples_by_lab_in_days/` - Get turnaround time samples tested in days
- `GET /tb/gx/laboratories/trl_samples_by_lab_in_days_by_month/` - Get turnaround time samples tested in days by month

#### Summary Endpoints
- `GET /tb/gx/laboratories/summary/summary_header_component/` - Get dashboard header component summary
- `GET /tb/gx/laboratories/summary/positivity_by_month/` - Get positivity rate by month
- `GET /tb/gx/laboratories/summary/positivity_by_lab/` - Get positivity rate by laboratory
- `GET /tb/gx/laboratories/summary/positivity_by_lab_by_age/` - Get positivity rate by laboratory by age

### HIV Viral Load Endpoints
- `GET /hiv/vl/laboratory/registered_samples/` - Get registered samples for HIV viral load testing

### Dictionary Endpoints
- `GET /dict/laboratories/` - Get all laboratories
- `GET /dict/laboratories/provinces/` - Get laboratories by province
- `GET /dict/laboratories/province/districts/` - Get laboratories by district
- `GET /dict/facilities/` - Get all facilities
- `GET /dict/facilities/provinces/` - Get facilities by province
- `GET /dict/facilities/province/districts/` - Get facilities by district

## Common Parameters

The API accepts several common parameters across endpoints:

### Query Parameters
- `interval_dates`: Date range for filtering data (format: ["YYYY-MM-DD", "YYYY-MM-DD"])
- `province`: Filter by province name
- `district`: Filter by district name
- `facility_type`: Type of facility (province, district, health_facility)
- `genexpert_result_type`: Type of GeneXpert result (Ultra 6 Cores, XDR 10 Cores)
- `type_of_laboratory`: Laboratory type
- `disaggregation`: Whether to include disaggregated data (True/False)

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Access the API documentation at: `http://localhost:5000/apidocs/`

## Error Handling

The API uses standard HTTP status codes:
- 200: Success
- 400: Invalid Parameters
- 404: Resource Not Found
- 500: Server Error

Error responses include a message describing the error:
```json
{
    "message": "Error description"
}
```
