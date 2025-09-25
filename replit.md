# SaberAngola Backend Documentation

## Overview

SaberAngola is a comprehensive Django-based document generation and management platform designed for the Angolan market. The system provides document creation, user management, subscription handling, and payment processing capabilities. Built with Django 5.0 and Django REST Framework, it follows a modular architecture with separate apps for authentication, user management, document processing, payments, and health monitoring.

The platform integrates with local Angolan payment gateways (Multicaixa, EMIS) and provides asynchronous document generation using Celery for improved performance and scalability.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Framework and Structure
- **Django 5.0** with Django REST Framework for API development
- **Modular app structure** with dedicated apps for authentication, users, documents, payments, and health monitoring
- **Custom user model** with email-based authentication instead of username
- **Environment-based settings** with separate configurations for development and production

### Authentication and Authorization
- **JWT Authentication** using django-rest-framework-simplejwt for stateless authentication
- **Custom user model** with email as primary identifier and premium status tracking
- **Permission system** with custom permissions for ownership validation and subscription checks
- **Security middleware** implementing security headers and API request logging

### Database and Data Management
- **PostgreSQL** as the primary database with proper schema design
- **UUID fields** for documents and transactions to ensure uniqueness and security
- **JSON fields** for flexible data storage (template fields, features, activity details)
- **Proper relationships** with foreign keys and cascading delete policies

### Document Generation System
- **Multi-format support** for PDF (ReportLab), DOCX (python-docx), and XLSX (openpyxl) generation
- **Template-based system** with configurable fields and dynamic content generation
- **Asynchronous processing** using Celery for handling large document generation tasks
- **File storage integration** ready for AWS S3 implementation

### Payment Processing
- **Multi-gateway support** for Angolan payment systems (Multicaixa, EMIS)
- **Subscription management** with different plan types (Free, Basic, Premium)
- **Transaction tracking** with status monitoring and webhook handling
- **Currency support** configured for AOA (Angolan Kwanza)

### Asynchronous Task Processing
- **Celery integration** for background task processing
- **Redis** as message broker and result backend
- **Task types** including document generation, email sending, and payment processing
- **Error handling and retry mechanisms** for failed tasks

### API Design and Communication
- **RESTful API structure** with consistent endpoint naming and HTTP methods
- **Standardized serializers** for data validation and transformation
- **CORS configuration** for frontend integration
- **Rate limiting and security** middleware for API protection

### Storage and File Management
- **AWS S3 integration** configured for file storage with proper access controls
- **Media file handling** with support for user avatars and document uploads
- **Environment-based storage** configuration for development and production

### Monitoring and Health Checks
- **Health check endpoints** for system monitoring
- **Structured logging** with different levels for development and production
- **Security headers** middleware for enhanced security
- **API request logging** for monitoring and debugging

## External Dependencies

### Core Framework Dependencies
- **Django 5.0** - Web framework
- **Django REST Framework** - API development
- **django-rest-framework-simplejwt** - JWT authentication
- **django-cors-headers** - CORS handling
- **django-filter** - API filtering capabilities

### Document Generation Libraries
- **ReportLab** - PDF generation and manipulation
- **python-docx** - Microsoft Word document creation
- **openpyxl** - Excel spreadsheet generation and editing

### Database and Caching
- **PostgreSQL** - Primary database (configured but not explicitly in requirements)
- **Redis** - Caching and Celery message broker
- **psycopg2** - PostgreSQL database adapter

### Asynchronous Processing
- **Celery** - Distributed task queue
- **Redis** - Message broker and result backend

### File Storage and Cloud Services
- **boto3** - AWS SDK for S3 integration
- **django-storages** - Django storage backends including S3

### Configuration and Environment Management
- **python-decouple** - Environment variable management
- **django-environ** - Environment-based configuration

### API Documentation and Development Tools
- **drf-yasg** - Swagger/OpenAPI documentation generation

### Payment Gateway Integrations
- **Multicaixa Express (EMIS)** - Local Angolan payment gateway
- **Unitel Money** - Mobile payment integration
- **Custom payment service classes** for handling different payment methods

### Monitoring and Observability
- **Django logging framework** - Application logging
- **Health check system** - Database and service monitoring
- **Custom middleware** - Security headers and request logging